from pydantic import BaseModel, Field


class SyllabusSummaryRequest(BaseModel):
    syllabus_text: str = Field(min_length=1)
    course_name: str | None = None


class SyllabusSummaryResponse(BaseModel):
    course_name: str | None
    summary: str
