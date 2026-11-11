from datetime import date as Date
from typing import Literal

from pydantic import BaseModel, Field


class SyllabusSummaryRequest(BaseModel):
    syllabus_text: str = Field(min_length=1)
    course_name: str | None = None
class CourseInfo(BaseModel):
    name: str | None = None
    code: str | None = None
    term: str | None = None
class Instructor(BaseModel):
    name: str | None = None
    email: str | None = None
    office_hours: str | None = None
class CourseOutline(BaseModel):
    topic: str
    week_or_date: str | None = None
    description: str | None = None
    readings_or_assignments: list[str] = Field(default_factory=list)
    evidence: str | None = None
class ImportantDate(BaseModel):
    title: str
    date: Date | None = None
    date_text: str | None = None
    date_precision: Literal["exact", "month", "relative", "unclear"] = "unclear"
    type: Literal[
        "assignment",
        "exam",
        "quiz",
        "presentation",
        "deadline",
        "to_read",
        "final_exam",
        "class_schedule",
        "other",
    ] = "other"
    details: str = ""
    evidence: str | None = None
class CoursePolicy(BaseModel):
    topic: str | None = None
    description: str
    evidence: str | None = None
class Uncertainty(BaseModel):
    topic: str
    explanation: str

class SyllabusSummaryResponse(BaseModel):
    course: CourseInfo = Field(default_factory=CourseInfo)
    summary: str
    instructor: Instructor = Field(default_factory=Instructor)
    course_outline: list[CourseOutline] = Field(default_factory=list)
    important_dates: list[ImportantDate] = Field(default_factory=list)
    policies: list[CoursePolicy] = Field(default_factory=list)
    uncertainties: list[Uncertainty] = Field(default_factory=list)
    