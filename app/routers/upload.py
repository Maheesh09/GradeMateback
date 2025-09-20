from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..pdf_extractor import process_pdf
from ..database import get_db
from ..crud import create_pdf_from_parsed_data, get_pdf_by_name
from ..schemas import UploadResponse
import os
import tempfile
import shutil
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/answer-sheet", response_model=UploadResponse)
async def upload_answer_sheet(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload an answer sheet PDF and extract questions and answers using extractInformation2.py
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Create temporary file
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded file to temporary location
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF using new extractor
        result = process_pdf(temp_file_path)
        
        if result["success"]:
            try:
                # Check if PDF already exists
                existing_pdf = get_pdf_by_name(db, file.filename)
                if existing_pdf:
                    logger.warning(f"PDF {file.filename} already exists with ID: {existing_pdf.pdf_id}")
                    return UploadResponse(
                        filename=file.filename,
                        extracted_text=result["extracted_text"],
                        parsed_questions=result["parsed_questions"],
                        question_count=result["question_count"],
                        status="success",
                        pdf_id=existing_pdf.pdf_id
                    )
                
                # Save to database
                pdf_record = create_pdf_from_parsed_data(
                    db=db,
                    pdf_name=file.filename,
                    parsed_questions=result["parsed_questions"]
                )
                
                logger.info(f"Successfully processed and saved PDF: {file.filename} with ID: {pdf_record.pdf_id}")
                
                return UploadResponse(
                    filename=file.filename,
                    extracted_text=result["extracted_text"],
                    parsed_questions=result["parsed_questions"],
                    question_count=result["question_count"],
                    status="success",
                    pdf_id=pdf_record.pdf_id
                )
                
            except Exception as db_error:
                logger.error(f"Database error while saving PDF {file.filename}: {db_error}")
                # Return success but without database save
                return UploadResponse(
                    filename=file.filename,
                    extracted_text=result["extracted_text"],
                    parsed_questions=result["parsed_questions"],
                    question_count=result["question_count"],
                    status="success_no_db",
                    pdf_id=None
                )
        else:
            raise HTTPException(status_code=500, detail=f"PDF processing failed: {result['error']}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

@router.post("/answer-sheet-batch")
async def upload_answer_sheets_batch(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload multiple answer sheet PDFs and extract questions and answers
    """
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No files provided")
    
    results = []
    temp_dir = tempfile.mkdtemp()
    
    try:
        for file in files:
            # Validate file type
            if not file.filename.lower().endswith('.pdf'):
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": "Only PDF files are allowed"
                })
                continue
            
            temp_file_path = os.path.join(temp_dir, file.filename)
            
            try:
                # Save uploaded file to temporary location
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Process PDF using new extractor
                result = process_pdf(temp_file_path)
                
                if result["success"]:
                    try:
                        # Check if PDF already exists
                        existing_pdf = get_pdf_by_name(db, file.filename)
                        if existing_pdf:
                            logger.warning(f"PDF {file.filename} already exists with ID: {existing_pdf.pdf_id}")
                            results.append({
                                "filename": file.filename,
                                "extracted_text": result["extracted_text"],
                                "parsed_questions": result["parsed_questions"],
                                "question_count": result["question_count"],
                                "status": "success",
                                "pdf_id": existing_pdf.pdf_id
                            })
                        else:
                            # Save to database
                            pdf_record = create_pdf_from_parsed_data(
                                db=db,
                                pdf_name=file.filename,
                                parsed_questions=result["parsed_questions"]
                            )
                            
                            logger.info(f"Successfully processed and saved PDF: {file.filename} with ID: {pdf_record.pdf_id}")
                            
                            results.append({
                                "filename": file.filename,
                                "extracted_text": result["extracted_text"],
                                "parsed_questions": result["parsed_questions"],
                                "question_count": result["question_count"],
                                "status": "success",
                                "pdf_id": pdf_record.pdf_id
                            })
                            
                    except Exception as db_error:
                        logger.error(f"Database error while saving PDF {file.filename}: {db_error}")
                        # Return success but without database save
                        results.append({
                            "filename": file.filename,
                            "extracted_text": result["extracted_text"],
                            "parsed_questions": result["parsed_questions"],
                            "question_count": result["question_count"],
                            "status": "success_no_db",
                            "pdf_id": None
                        })
                else:
                    results.append({
                        "filename": file.filename,
                        "status": "error",
                        "error": result["error"]
                    })
                
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
            
            finally:
                # Clean up individual file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
        
        return JSONResponse(content={
            "results": results,
            "total_files": len(files),
            "successful": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"])
        })
        
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

@router.get("/health")
async def health_check():
    """
    Health check endpoint for the upload service
    """
    return {"status": "healthy", "service": "upload"}
