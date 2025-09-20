"""
Database CRUD operations for GradeMate application
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from .models import PDF, Question, Answer
from .schemas import PDFCreate, QuestionCreate, AnswerCreate
from .utils import roman_to_int
import logging

logger = logging.getLogger(__name__)

# -------- PDF Operations --------
def create_pdf(db: Session, pdf_data: PDFCreate) -> PDF:
    """Create a new PDF record with questions and answers"""
    try:
        # Create PDF record
        db_pdf = PDF(pdf_name=pdf_data.pdf_name)
        db.add(db_pdf)
        db.flush()  # Get the PDF ID
        
        # Create questions and answers
        for question_data in pdf_data.questions:
            db_question = Question(
                pdf_id=db_pdf.pdf_id,
                main_no=question_data.main_no
            )
            db.add(db_question)
            db.flush()  # Get the question ID
            
            # Create answers for this question
            for answer_data in question_data.answers:
                db_answer = Answer(
                    question_id=db_question.question_id,
                    roman_text=answer_data.roman_text,
                    part_no=answer_data.part_no,
                    answer_text=answer_data.answer_text
                )
                db.add(db_answer)
        
        db.commit()
        db.refresh(db_pdf)
        logger.info(f"Created PDF: {db_pdf.pdf_name} with ID: {db_pdf.pdf_id}")
        return db_pdf
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating PDF: {e}")
        raise

def get_pdf(db: Session, pdf_id: int) -> Optional[PDF]:
    """Get a PDF by ID with all questions and answers"""
    return db.query(PDF).filter(PDF.pdf_id == pdf_id).first()

def get_pdf_by_name(db: Session, pdf_name: str) -> Optional[PDF]:
    """Get a PDF by name"""
    return db.query(PDF).filter(PDF.pdf_name == pdf_name).first()

def get_pdfs(db: Session, skip: int = 0, limit: int = 100) -> List[PDF]:
    """Get all PDFs with pagination"""
    return db.query(PDF).offset(skip).limit(limit).all()

def delete_pdf(db: Session, pdf_id: int) -> bool:
    """Delete a PDF and all its questions/answers (cascade)"""
    try:
        pdf = db.query(PDF).filter(PDF.pdf_id == pdf_id).first()
        if pdf:
            db.delete(pdf)
            db.commit()
            logger.info(f"Deleted PDF: {pdf.pdf_name} with ID: {pdf_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting PDF: {e}")
        raise

# -------- Question Operations --------
def get_questions_by_pdf(db: Session, pdf_id: int) -> List[Question]:
    """Get all questions for a specific PDF"""
    return db.query(Question).filter(Question.pdf_id == pdf_id).all()

def get_question(db: Session, question_id: int) -> Optional[Question]:
    """Get a question by ID with all answers"""
    return db.query(Question).filter(Question.question_id == question_id).first()

def delete_question(db: Session, question_id: int) -> bool:
    """Delete a question and all its answers (cascade)"""
    try:
        question = db.query(Question).filter(Question.question_id == question_id).first()
        if question:
            db.delete(question)
            db.commit()
            logger.info(f"Deleted question with ID: {question_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting question: {e}")
        raise

# -------- Answer Operations --------
def get_answers_by_question(db: Session, question_id: int) -> List[Answer]:
    """Get all answers for a specific question"""
    return db.query(Answer).filter(Answer.question_id == question_id).all()

def get_answer(db: Session, answer_id: int) -> Optional[Answer]:
    """Get an answer by ID"""
    return db.query(Answer).filter(Answer.answer_id == answer_id).first()

def delete_answer(db: Session, answer_id: int) -> bool:
    """Delete an answer"""
    try:
        answer = db.query(Answer).filter(Answer.answer_id == answer_id).first()
        if answer:
            db.delete(answer)
            db.commit()
            logger.info(f"Deleted answer with ID: {answer_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting answer: {e}")
        raise

# -------- Utility Functions --------
def create_pdf_from_parsed_data(db: Session, pdf_name: str, parsed_questions: dict) -> PDF:
    """
    Create a PDF record from parsed question data
    
    Args:
        db: Database session
        pdf_name: Name of the PDF file
        parsed_questions: Dictionary with question data in format:
            {
                "1": {"i": "answer text", "ii": "answer text"},
                "2": {"i": "answer text", "iii": "answer text"}
            }
    
    Returns:
        Created PDF object
    """
    try:
        # Create PDF record
        db_pdf = PDF(pdf_name=pdf_name)
        db.add(db_pdf)
        db.flush()  # Get the PDF ID
        
        # Process each question
        for question_num_str, answers_dict in parsed_questions.items():
            question_num = int(question_num_str)
            
            # Create question record
            db_question = Question(
                pdf_id=db_pdf.pdf_id,
                main_no=question_num
            )
            db.add(db_question)
            db.flush()  # Get the question ID
            
            # Process each answer for this question
            for roman_text, answer_text in answers_dict.items():
                try:
                    part_no = roman_to_int(roman_text)
                    
                    # Create answer record
                    db_answer = Answer(
                        question_id=db_question.question_id,
                        roman_text=roman_text,
                        part_no=part_no,
                        answer_text=answer_text
                    )
                    db.add(db_answer)
                    
                except ValueError as e:
                    logger.warning(f"Invalid Roman numeral '{roman_text}' in question {question_num}: {e}")
                    continue
        
        db.commit()
        db.refresh(db_pdf)
        logger.info(f"Created PDF from parsed data: {db_pdf.pdf_name} with ID: {db_pdf.pdf_id}")
        return db_pdf
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating PDF from parsed data: {e}")
        raise
