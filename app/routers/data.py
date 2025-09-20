"""
Data retrieval endpoints for GradeMate application
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..crud import (
    get_pdfs, get_pdf, get_pdf_by_name, delete_pdf,
    get_questions_by_pdf, get_question, delete_question,
    get_answers_by_question, get_answer, delete_answer
)
from ..schemas import (
    PDF, PDFListResponse, Question, QuestionListResponse,
    Answer, AnswerListResponse, HealthResponse
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/data", tags=["data"])

# -------- PDF Endpoints --------
@router.get("/pdfs", response_model=PDFListResponse)
async def get_all_pdfs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all PDFs with pagination"""
    try:
        pdfs = get_pdfs(db, skip=skip, limit=limit)
        total = len(pdfs)  # This is a simplified count, in production you'd want a proper count query
        
        return PDFListResponse(pdfs=pdfs, total=total)
    except Exception as e:
        logger.error(f"Error retrieving PDFs: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving PDFs")

@router.get("/pdfs/{pdf_id}", response_model=PDF)
async def get_pdf_by_id(
    pdf_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific PDF by ID with all questions and answers"""
    try:
        pdf = get_pdf(db, pdf_id)
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")
        return pdf
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving PDF {pdf_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving PDF")

@router.delete("/pdfs/{pdf_id}")
async def delete_pdf_by_id(
    pdf_id: int,
    db: Session = Depends(get_db)
):
    """Delete a PDF and all its questions/answers"""
    try:
        success = delete_pdf(db, pdf_id)
        if not success:
            raise HTTPException(status_code=404, detail="PDF not found")
        return {"message": f"PDF {pdf_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting PDF {pdf_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting PDF")

# -------- Question Endpoints --------
@router.get("/pdfs/{pdf_id}/questions", response_model=QuestionListResponse)
async def get_questions_for_pdf(
    pdf_id: int,
    db: Session = Depends(get_db)
):
    """Get all questions for a specific PDF"""
    try:
        # First check if PDF exists
        pdf = get_pdf(db, pdf_id)
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")
        
        questions = get_questions_by_pdf(db, pdf_id)
        return QuestionListResponse(questions=questions, total=len(questions), pdf_id=pdf_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving questions for PDF {pdf_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving questions")

@router.get("/questions/{question_id}", response_model=Question)
async def get_question_by_id(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific question by ID with all answers"""
    try:
        question = get_question(db, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving question {question_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving question")

@router.delete("/questions/{question_id}")
async def delete_question_by_id(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Delete a question and all its answers"""
    try:
        success = delete_question(db, question_id)
        if not success:
            raise HTTPException(status_code=404, detail="Question not found")
        return {"message": f"Question {question_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting question {question_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting question")

# -------- Answer Endpoints --------
@router.get("/questions/{question_id}/answers", response_model=AnswerListResponse)
async def get_answers_for_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get all answers for a specific question"""
    try:
        # First check if question exists
        question = get_question(db, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        answers = get_answers_by_question(db, question_id)
        return AnswerListResponse(answers=answers, total=len(answers), question_id=question_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving answers for question {question_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving answers")

@router.get("/answers/{answer_id}", response_model=Answer)
async def get_answer_by_id(
    answer_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific answer by ID"""
    try:
        answer = get_answer(db, answer_id)
        if not answer:
            raise HTTPException(status_code=404, detail="Answer not found")
        return answer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving answer {answer_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving answer")

@router.delete("/answers/{answer_id}")
async def delete_answer_by_id(
    answer_id: int,
    db: Session = Depends(get_db)
):
    """Delete an answer"""
    try:
        success = delete_answer(db, answer_id)
        if not success:
            raise HTTPException(status_code=404, detail="Answer not found")
        return {"message": f"Answer {answer_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting answer {answer_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting answer")

# -------- Search Endpoints --------
@router.get("/search/pdf")
async def search_pdf_by_name(
    name: str = Query(..., description="PDF name to search for"),
    db: Session = Depends(get_db)
):
    """Search for a PDF by name"""
    try:
        pdf = get_pdf_by_name(db, name)
        if not pdf:
            raise HTTPException(status_code=404, detail="PDF not found")
        return pdf
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching for PDF {name}: {e}")
        raise HTTPException(status_code=500, detail="Error searching for PDF")
