from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class PDF(Base):
    __tablename__ = "pdfs"
    
    pdf_id = Column(BigInteger, primary_key=True, autoincrement=True)
    pdf_name = Column(String(255), nullable=False, unique=True)
    uploaded_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    
    # Relationship to questions
    questions = relationship("Question", back_populates="pdf", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"
    
    question_id = Column(BigInteger, primary_key=True, autoincrement=True)
    pdf_id = Column(BigInteger, ForeignKey("pdfs.pdf_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    main_no = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    
    # Relationships
    pdf = relationship("PDF", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("pdf_id", "main_no", name="uq_question_per_pdf"),
    )

class Answer(Base):
    __tablename__ = "answers"
    
    answer_id = Column(BigInteger, primary_key=True, autoincrement=True)
    question_id = Column(BigInteger, ForeignKey("questions.question_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    roman_text = Column(String(8), nullable=False)
    part_no = Column(Integer, nullable=False)  # TINYINT UNSIGNED equivalent
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    
    # Relationships
    question = relationship("Question", back_populates="answers")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint("question_id", "part_no", name="uq_part"),
        CheckConstraint("part_no BETWEEN 1 AND 50", name="ck_part_range"),
        CheckConstraint("LOWER(roman_text) REGEXP '^(i|ii|iii|iv|v|vi|vii|viii|ix|x|xi|xii|xiii|xiv|xv|xvi|xvii|xviii|xix|xx)$'", name="ck_roman_format"),
    )
