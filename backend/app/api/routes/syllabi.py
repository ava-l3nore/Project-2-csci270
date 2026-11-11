from io import BytesIO
from pathlib import Path
from zipfile import BadZipFile

from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from docx.table import Table
from docx.text.paragraph import Paragraph
from fastapi import APIRouter, File, HTTPException, UploadFile
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.config import get_settings
from app.models.syllabus import (
    BatchSyllabusSummaryResponse,
    SyllabusFileResult,
    SyllabusSummaryRequest,
    SyllabusSummaryResponse,
)
from app.services.nova_lite import summarize_syllabus


router = APIRouter(prefix="/syllabi", tags=["syllabi"])
MAX_BATCH_FILES = 8
MAX_FILE_BYTES = 15 * 1024 * 1024


@router.post("/summarize", response_model=SyllabusSummaryResponse)
def create_syllabus_summary(
    request: SyllabusSummaryRequest,
) -> SyllabusSummaryResponse:
    settings = get_settings()
    summary = summarize_syllabus(
        syllabus_text=request.syllabus_text,
        model_id=settings.bedrock_model_id,
        region=settings.aws_region,
    )
    if request.course_name is not None:
        summary = summary.model_copy(
            update={
                "course": summary.course.model_copy(
                    update={"name": request.course_name}
                )
            }
        )
    return summary


def extract_syllabus_text(filename: str, data: bytes) -> str:
    extension = Path(filename).suffix.lower()

    if extension == ".txt":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise HTTPException(
                status_code=422,
                detail=f"{filename} is not valid UTF-8 text.",
            ) from error
    elif extension == ".pdf":
        try:
            reader = PdfReader(BytesIO(data))
            text = "\n".join(
                f"Page {number}\n{page.extract_text() or ''}"
                for number, page in enumerate(reader.pages, start=1)
            )
        except PdfReadError as error:
            raise HTTPException(
                status_code=422,
                detail=f"Could not read PDF: {filename}.",
            ) from error
    elif extension == ".docx":
        try:
            document = Document(BytesIO(data))
        except (BadZipFile, PackageNotFoundError) as error:
            raise HTTPException(
                status_code=422,
                detail=f"Could not read DOCX: {filename}.",
            ) from error
        document_parts = []
        for item in document.iter_inner_content():
            if isinstance(item, Paragraph) and item.text:
                document_parts.append(item.text)
            elif isinstance(item, Table):
                document_parts.extend(
                    "\t".join(cell.text for cell in row.cells)
                    for row in item.rows
                )
        text = "\n".join(document_parts)
    else:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type for {filename}; upload .txt, .pdf, or .docx.",
        )

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail=f"No text could be extracted from {filename}.",
        )
    
    return text


@router.post(
    "/summarize-batch",
    response_model=BatchSyllabusSummaryResponse,
)
def summarize_syllabus_batch(
    files: list[UploadFile] = File(...),
) -> BatchSyllabusSummaryResponse:
    if not files:
        raise HTTPException(status_code=422, detail="Upload at least one file.")
    if len(files) > MAX_BATCH_FILES:
        raise HTTPException(
            status_code=413,
            detail=f"Upload no more than {MAX_BATCH_FILES} files at once.",
        )

    settings = get_settings()
    results = []
    for index, file in enumerate(files, start=1):
        filename = file.filename or f"upload-{index}"
        data = file.file.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"{filename} exceeds the 15 MB limit.",
            )

        text = extract_syllabus_text(filename, data)
        summary = summarize_syllabus(
            syllabus_text=text,
            model_id=settings.bedrock_model_id,
            region=settings.aws_region,
        )
        results.append(
            SyllabusFileResult(
                index=index,
                filename=filename,
                summary=summary,
            )
        )
    return BatchSyllabusSummaryResponse(results=results)
