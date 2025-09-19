from sqlalchemy import (
    Column, String, Integer, BigInteger, Boolean, Text, TIMESTAMP, DateTime,
    ForeignKey, UniqueConstraint, Enum, Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import JSON as MySQLJSON
from .database import Base
import enum

# ---------- ENUMS ----------
class QuestionType(str, enum.Enum):
    MCQ = "MCQ"
    SHORT = "SHORT"
    ESSAY = "ESSAY"

class ReviewStatus(str, enum.Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"

# ---------- TABLES ----------
class Student(Base):
    __tablename__ = "students"
    student_id = Column(String(20), primary_key=True)
    name = Column(String(120), nullable=False)

    submissions = relationship("Submission", back_populates="student")

class ModelPaper(Base):
    __tablename__ = "model_papers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    subject_name = Column(String(200), nullable=False)
    paper_no = Column(Integer, nullable=False)
    part = Column(String(10))
    is_results_released = Column(Boolean, server_default="0")
    is_reasoning_visible = Column(Boolean, server_default="1")
    layout_json = Column(MySQLJSON)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    __table_args__ = (
        UniqueConstraint("subject_name", "paper_no", "part", name="uq_paper_subject_no_part"),
    )

    questions = relationship("Question", back_populates="paper", cascade="all,delete-orphan")
    schemes = relationship("MarkingScheme", back_populates="paper", cascade="all,delete-orphan")
    submissions = relationship("Submission", back_populates="paper", cascade="all,delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    paper_id = Column(BigInteger, ForeignKey("model_papers.id"), nullable=False)
    qno = Column(Integer, nullable=False)
    type = Column(Enum(QuestionType), nullable=False)
    text = Column(Text, nullable=False)
    options = Column(MySQLJSON)           # ["1","2","3","4","5"]
    answer_key = Column(String(10))
    max_marks = Column(Integer, server_default="1")
    rubric = Column(MySQLJSON)

    __table_args__ = (
        UniqueConstraint("paper_id", "qno", name="uq_paper_qno"),
    )

    paper = relationship("ModelPaper", back_populates="questions")
    scheme_links = relationship("SchemeQuestion", back_populates="question", cascade="all,delete-orphan")
    answers = relationship("Answer", back_populates="question")

class MarkingScheme(Base):
    __tablename__ = "marking_schemes"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    paper_id = Column(BigInteger, ForeignKey("model_papers.id"), nullable=False)
    name = Column(String(120), nullable=False)
    version = Column(Integer, nullable=False)
    is_active = Column(Boolean, server_default="1")
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    __table_args__ = (
        UniqueConstraint("paper_id", "version", name="uq_paper_version"),
    )

    paper = relationship("ModelPaper", back_populates="schemes")
    scheme_questions = relationship("SchemeQuestion", back_populates="scheme", cascade="all,delete-orphan")

class SchemeQuestion(Base):
    __tablename__ = "scheme_questions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    scheme_id = Column(BigInteger, ForeignKey("marking_schemes.id"), nullable=False)
    question_id = Column(BigInteger, ForeignKey("questions.id"), nullable=False)
    max_marks = Column(Integer, nullable=False)
    notes = Column(Text)

    __table_args__ = (
        UniqueConstraint("scheme_id", "question_id", name="uq_scheme_question"),
    )

    scheme = relationship("MarkingScheme", back_populates="scheme_questions")
    question = relationship("Question", back_populates="scheme_links")
    mcq_keys = relationship("SchemeMCQKey", back_populates="scheme_question", cascade="all,delete-orphan")
    points = relationship("SchemePoint", back_populates="scheme_question", cascade="all,delete-orphan")
    answers = relationship("Answer", back_populates="scheme_question")

class SchemeMCQKey(Base):
    __tablename__ = "scheme_mcq_keys"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    scheme_question_id = Column(BigInteger, ForeignKey("scheme_questions.id"), nullable=False)
    option_code = Column(String(10), nullable=False)
    is_correct = Column(Boolean, server_default="1", nullable=False)
    partial_credit = Column(Integer, server_default="0")
    rationale = Column(Text)

    __table_args__ = (
        UniqueConstraint("scheme_question_id", "option_code", name="uq_schemeq_option"),
    )

    scheme_question = relationship("SchemeQuestion", back_populates="mcq_keys")

class SchemePoint(Base):
    __tablename__ = "scheme_points"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    scheme_question_id = Column(BigInteger, ForeignKey("scheme_questions.id"), nullable=False)
    point_order = Column(Integer, nullable=False)
    description = Column(String(255), nullable=False)
    keywords = Column(MySQLJSON)
    marks = Column(Integer, nullable=False)
    required = Column(Boolean, server_default="0")

    __table_args__ = (
        UniqueConstraint("scheme_question_id", "point_order", name="uq_schemeq_pointorder"),
    )

    scheme_question = relationship("SchemeQuestion", back_populates="points")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    paper_id = Column(BigInteger, ForeignKey("model_papers.id"), nullable=False)
    student_id = Column(String(20), ForeignKey("students.student_id"), nullable=False)
    total_marks = Column(Integer, server_default="0")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    is_visible_to_student = Column(Boolean)  # NULL = inherit

    __table_args__ = (
        UniqueConstraint("paper_id", "student_id", name="uq_submission_once"),
    )

    paper = relationship("ModelPaper", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")
    answers = relationship("Answer", back_populates="submission", cascade="all,delete-orphan")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    submission_id = Column(BigInteger, ForeignKey("submissions.id"), nullable=False)
    question_id = Column(BigInteger, ForeignKey("questions.id"), nullable=False)
    scheme_question_id = Column(BigInteger, ForeignKey("scheme_questions.id"))
    response_text = Column(Text)
    chosen_option = Column(String(10))
    score = Column(Integer, server_default="0")
    reasoning = Column(Text)
    omr_json = Column(MySQLJSON)
    ocr_text = Column(Text)
    ocr_conf = Column(Numeric(5, 4))
    flags = Column(MySQLJSON)
    image_crop_path = Column(String(255))

    __table_args__ = (
        UniqueConstraint("submission_id", "question_id", name="uq_submission_question"),
    )

    submission = relationship("Submission", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    scheme_question = relationship("SchemeQuestion", back_populates="answers")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    answer_id = Column(BigInteger, ForeignKey("answers.id"), nullable=False)
    status = Column(Enum(ReviewStatus), nullable=False)
    reviewer = Column(String(120))
    resolution = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    resolved_at = Column(DateTime)

    # No backref needed unless you want: relationship("Answer", back_populates="reviews")
