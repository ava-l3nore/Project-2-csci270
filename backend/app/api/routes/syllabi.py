from fastapi import APIRouter

from app.core.config import get_settings
from app.models.syllabus import SyllabusSummaryRequest, SyllabusSummaryResponse
from app.services.nova_lite import summarize_syllabus

router = APIRouter(prefix="/syllabi", tags=["syllabi"])


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
    return SyllabusSummaryResponse(
        course_name=request.course_name,
        summary=summary,
    )
