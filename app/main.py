from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.settings import settings
from app.db.mongodb import mongo_client
from app.api.auth_routes import router as auth_router
from app.api.document_routes import router as document_router
from app.api.chat_routes import router as chat_router

@asynccontextmanager
async def lifespan(application: FastAPI):
    print("Connected to MongoDB")
    yield
    mongo_client.close()
    print("MongoDB connection closed")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)

@app.get("/")
async def home():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }