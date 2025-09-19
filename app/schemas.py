from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from .models import QuestionType, ReviewStatus

# -------- Students --------
class StudentCreate(BaseModel):
    student_id: str
    name: str

class StudentRead(BaseModel):
    student_id: str
    name: str
    class Config: from_attributes = True

# -------- Model Papers --------
class PaperCreate(BaseModel):
    subject_name: str
    paper_no: int
    part: Optional[str] = None
    is_results_released: Optional[bool] = False
    is_reasoning_visible: Optional[bool] = True
    layout_json: Optional[Any] = None

class PaperRead(PaperCreate):
    id: int
    created_at: Optional[datetime]
    class Config: from_attributes = True

# -------- Questions --------
class QuestionCreate(BaseModel):
    paper_id: int
    qno: int
    type: QuestionType
    text: str
    options: Optional[Any] = None
    answer_key: Optional[str] = None
    max_marks: Optional[int] = 1
    rubric: Optional[Any] = None

class QuestionRead(QuestionCreate):
    id: int
    class Config: from_attributes = True

# -------- Schemes --------
class SchemeCreate(BaseModel):
    paper_id: int
    name: str
    version: int
    is_active: Optional[bool] = True
    notes: Optional[str] = None

class SchemeRead(SchemeCreate):
    id: int
    created_at: Optional[datetime]
    class Config: from_attributes = True

class SchemeQuestionCreate(BaseModel):
    scheme_id: int
    question_id: int
    max_marks: int
    notes: Optional[str] = None

class SchemeQuestionRead(SchemeQuestionCreate):
    id: int
    class Config: from_attributes = True

class SchemeMCQKeyCreate(BaseModel):
    scheme_question_id: int
    option_code: str
    is_correct: Optional[bool] = True
    partial_credit: Optional[int] = 0
    rationale: Optional[str] = None

class SchemeMCQKeyRead(SchemeMCQKeyCreate):
    id: int
    class Config: from_attributes = True

class SchemePointCreate(BaseModel):
    scheme_question_id: int
    point_order: int
    description: str
    keywords: Optional[List[str]] = None
    marks: int
    required: Optional[bool] = False

class SchemePointRead(SchemePointCreate):
    id: int
    class Config: from_attributes = True

# -------- Submissions & Answers --------
class SubmissionCreate(BaseModel):
    paper_id: int
    student_id: str
    is_visible_to_student: Optional[bool] = None

class SubmissionRead(SubmissionCreate):
    id: int
    total_marks: int
    created_at: Optional[datetime]
    class Config: from_attributes = True

class AnswerCreate(BaseModel):
    submission_id: int
    question_id: int
    scheme_question_id: Optional[int] = None
    response_text: Optional[str] = None
    chosen_option: Optional[str] = None
    reasoning: Optional[str] = None
    omr_json: Optional[Any] = None
    ocr_text: Optional[str] = None
    ocr_conf: Optional[float] = Field(None, ge=0, le=1)
    flags: Optional[Any] = None
    image_crop_path: Optional[str] = None

class AnswerRead(AnswerCreate):
    id: int
    score: int
    class Config: from_attributes = True

# -------- Reviews --------
class ReviewCreate(BaseModel):
    answer_id: int
    status: ReviewStatus
    reviewer: Optional[str] = None
    resolution: Optional[str] = None

class ReviewRead(ReviewCreate):
    id: int
    created_at: Optional[datetime]
    resolved_at: Optional[datetime]
    class Config: from_attributes = True
