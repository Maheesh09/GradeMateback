#!/usr/bin/env python3
"""
Test script for database integration
Run this script to test the database functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db_session, test_connection
from app.crud import create_pdf_from_parsed_data, get_pdf, get_pdfs
from app.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_operations():
    """Test basic database operations"""
    logger.info("Testing database operations...")
    
    # Test connection
    if not test_connection():
        logger.error("Database connection failed")
        return False
    
    # Get database session
    db = get_db_session()
    
    try:
        # Test data
        test_pdf_name = "test_sample.pdf"
        test_parsed_questions = {
            "1": {
                "i": "This is the answer for question 1 part i",
                "ii": "This is the answer for question 1 part ii"
            },
            "2": {
                "i": "This is the answer for question 2 part i",
                "ii": "This is the answer for question 2 part ii",
                "iii": "This is the answer for question 2 part iii"
            }
        }
        
        # Test creating a PDF
        logger.info("Creating test PDF...")
        pdf_record = create_pdf_from_parsed_data(
            db=db,
            pdf_name=test_pdf_name,
            parsed_questions=test_parsed_questions
        )
        
        logger.info(f"Created PDF with ID: {pdf_record.pdf_id}")
        
        # Test retrieving the PDF
        logger.info("Retrieving test PDF...")
        retrieved_pdf = get_pdf(db, pdf_record.pdf_id)
        
        if retrieved_pdf:
            logger.info(f"Retrieved PDF: {retrieved_pdf.pdf_name}")
            logger.info(f"Number of questions: {len(retrieved_pdf.questions)}")
            
            for question in retrieved_pdf.questions:
                logger.info(f"Question {question.main_no} has {len(question.answers)} answers")
                for answer in question.answers:
                    logger.info(f"  Part {answer.roman_text}: {answer.answer_text[:50]}...")
        else:
            logger.error("Failed to retrieve PDF")
            return False
        
        # Test getting all PDFs
        logger.info("Getting all PDFs...")
        all_pdfs = get_pdfs(db)
        logger.info(f"Total PDFs in database: {len(all_pdfs)}")
        
        logger.info("Database operations test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error during database operations test: {e}")
        return False
    
    finally:
        db.close()

def main():
    """Main test function"""
    logger.info("Starting database integration test...")
    logger.info(f"Database URL: {settings.database_url}")
    
    success = test_database_operations()
    
    if success:
        logger.info("✅ All tests passed!")
    else:
        logger.error("❌ Tests failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
