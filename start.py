#!/usr/bin/env python3
"""
Startup script for the GradeMate backend API.
This script handles both local development and production deployment.
"""

import uvicorn
import os
from app.config import settings

if __name__ == "__main__":
    # Get port from environment (Render sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    
    # Determine host based on environment
    host = "0.0.0.0" if settings.ENVIRONMENT == "production" else "127.0.0.1"
    
    print(f"Starting GradeMate API in {settings.ENVIRONMENT} mode")
    print(f"Server will be available at: http://{host}:{port}")
    print(f"CORS origins: {settings.cors_origins_list}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )
