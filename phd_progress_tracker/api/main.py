"""
FastAPI application entry point.
"""

from fastapi import FastAPI

from phd_progress_tracker.api.routes import tasks, milestones, dashboard

app = FastAPI(
    title="PhD Progress Tracker API",
    description="REST API for PhD progress tracking application",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include routers
app.include_router(tasks.router)
app.include_router(milestones.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "PhD Progress Tracker API",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
