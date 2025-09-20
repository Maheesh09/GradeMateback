#!/usr/bin/env python3
"""
Database setup script for GradeMate application
Run this script to create the database tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import create_tables, test_connection, engine
from app.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main setup function"""
    logger.info("Starting database setup...")
    logger.info(f"Database URL: {settings.database_url}")
    
    # Test connection
    if not test_connection():
        logger.error("Failed to connect to database. Please check your configuration.")
        logger.error("Make sure MySQL is running and the database exists.")
        logger.error("You can create the database with: CREATE DATABASE grademate;")
        return False
    
    # Create tables
    try:
        create_tables()
        logger.info("Database setup completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Error during database setup: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
