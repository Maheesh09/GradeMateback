from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
import enum

# -------- Enums --------
class QuestionType(str, enum.Enum):
    MCQ = "MCQ"
    SHORT = "SHORT"
    ESSAY = "ESSAY"

class ReviewStatus(str, enum.Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"

# -------- Database Schemas --------
class AnswerBase(BaseModel):
    roman_text: str = Field(..., description="Roman numeral text (i, ii, iii, etc.)")
    part_no: int = Field(..., ge=1, le=50, description="Numeric part number (1 for i, 2 for ii, etc.)")
    answer_text: str = Field(..., description="The actual answer text")

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    answer_id: int
    question_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    main_no: int = Field(..., description="Main question number")

class QuestionCreate(QuestionBase):
    answers: List[AnswerCreate] = Field(default_factory=list, description="List of answers for this question")

class Question(QuestionBase):
    question_id: int
    pdf_id: int
    created_at: datetime
    answers: List[Answer] = Field(default_factory=list)
    
    class Config:
        from_attributes = True

class PDFBase(BaseModel):
    pdf_name: str = Field(..., description="Name of the PDF file")

class PDFCreate(PDFBase):
    questions: List[QuestionCreate] = Field(default_factory=list, description="List of questions in the PDF")

class PDF(PDFBase):
    pdf_id: int
    uploaded_at: datetime
    questions: List[Question] = Field(default_factory=list)
    
    class Config:
        from_attributes = True

# -------- Upload Response Schemas --------
class UploadResponse(BaseModel):
    filename: str
    extracted_text: str
    parsed_questions: dict
    question_count: int
    status: str
    pdf_id: Optional[int] = None  # Added to return the created PDF ID

class BatchUploadResponse(BaseModel):
    results: List[dict]
    total_files: int
    successful: int
    failed: int

class HealthResponse(BaseModel):
    status: str
    service: str

# -------- API Response Schemas --------
class PDFListResponse(BaseModel):
    pdfs: List[PDF]
    total: int

class QuestionListResponse(BaseModel):
    questions: List[Question]
    total: int
    pdf_id: int

class AnswerListResponse(BaseModel):
    answers: List[Answer]
    total: int
    question_id: int