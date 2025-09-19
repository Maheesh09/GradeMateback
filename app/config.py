from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str = "password"
    DB_NAME: str = "hackathon_db"
    
    # Environment
    ENVIRONMENT: str = "development"  # development, production
    
    # CORS settings - can be overridden by environment variable
    CORS_ORIGINS: str = "http://127.0.0.1:3000,http://localhost:3000,https://gradematelk.vercel.app,https://*.vercel.app"
    
    # Render specific settings
    RENDER_EXTERNAL_URL: str = ""  # Will be set by Render automatically
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        
        # Add Render URL if available
        if self.RENDER_EXTERNAL_URL:
            origins.append(self.RENDER_EXTERNAL_URL)
            
        # Add local development origins if in development
        if self.ENVIRONMENT == "development":
            if "http://127.0.0.1:3000" not in origins:
                origins.append("http://127.0.0.1:3000")
            if "http://localhost:3000" not in origins:
                origins.append("http://localhost:3000")
                
        return origins

    class Config:
        env_file = ".env"

settings = Settings()
