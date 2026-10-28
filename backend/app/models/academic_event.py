from datetime import datetime

from pydantic import BaseModel, Field


class AcademicEvent(BaseModel):
    title: str = Field(min_length=1)
    due_at: datetime
    course_name: str | None = None
    details: str | None = None
