from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import upload, data
from .config import settings
from .database import create_tables, test_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GradeMate API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and test connection on startup"""
    try:
        # Test database connection
        if test_connection():
            # Create tables if they don't exist
            create_tables()
            logger.info("Database initialized successfully")
        else:
            logger.error("Failed to connect to database")
    except Exception as e:
        logger.error(f"Error during startup: {e}")

app.include_router(upload.router)
app.include_router(data.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "GradeMate API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if test_connection() else "disconnected"
    return {
        "status": "healthy",
        "service": "GradeMate API",
        "database": db_status,
        "version": "1.0.0"
    }
