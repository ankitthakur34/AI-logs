from fastapi import FastAPI

from app.database.database import Base, engine
from app.api.blocker_routes import router as blocker_router

# Import models so SQLAlchemy knows about them
import app.models


# Create tables if they do not already exist
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="DB Blocker Priority Service",
    version="1.0.0"
)


app.include_router(blocker_router)


@app.get("/")
def root():
    return {
        "message": "DB Blocker Priority Service is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }