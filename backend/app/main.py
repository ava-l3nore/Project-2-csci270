from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.syllabi import router as syllabi_router

app = FastAPI(
    title="Student Study Planner API",
    description="API for syllabus summaries and academic planning.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(syllabi_router, prefix="/api/v1")
