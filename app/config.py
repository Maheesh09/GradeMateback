from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str = "password"
    DB_NAME: str = "hackathon_db"
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://127.0.0.1:3000",
        "http://localhost:3000", 
        "https://gradematelk.vercel.app",
        "https://*.vercel.app"
    ]
    ENVIRONMENT: str = "development"  # development, production

    class Config:
        env_file = ".env"

settings = Settings()
