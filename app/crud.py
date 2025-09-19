from sqlalchemy import select, func, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from . import models, schemas

# ---- Students ----
async def create_student(db: AsyncSession, data: schemas.StudentCreate):
    obj = models.Student(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Student already exists")
    return obj

async def list_students(db: AsyncSession, skip=0, limit=100):
    res = await db.execute(select(models.Student).offset(skip).limit(limit))
    return res.scalars().all()

# ---- Papers ----
async def create_paper(db: AsyncSession, data: schemas.PaperCreate):
    obj = models.ModelPaper(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate paper (subject_name, paper_no, part)")
    return obj

async def get_paper(db: AsyncSession, paper_id: int):
    res = await db.execute(select(models.ModelPaper).where(models.ModelPaper.id == paper_id))
    return res.scalar_one_or_none()

# ---- Questions ----
async def create_question(db: AsyncSession, data: schemas.QuestionCreate):
    obj = models.Question(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate qno for this paper")
    return obj

async def list_questions_for_paper(db: AsyncSession, paper_id: int):
    res = await db.execute(
        select(models.Question).where(models.Question.paper_id == paper_id).order_by(models.Question.qno)
    )
    return res.scalars().all()

# ---- Schemes & items ----
async def create_scheme(db: AsyncSession, data: schemas.SchemeCreate):
    obj = models.MarkingScheme(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Duplicate version for this paper")
    return obj

async def create_scheme_question(db: AsyncSession, data: schemas.SchemeQuestionCreate):
    obj = models.SchemeQuestion(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Scheme-question already exists")
    return obj

async def add_scheme_mcq_key(db: AsyncSession, data: schemas.SchemeMCQKeyCreate):
    obj = models.SchemeMCQKey(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Option already defined for this scheme-question")
    return obj

async def add_scheme_point(db: AsyncSession, data: schemas.SchemePointCreate):
    obj = models.SchemePoint(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Point order already exists for this scheme-question")
    return obj

# ---- Submissions & answers ----
async def create_submission(db: AsyncSession, data: schemas.SubmissionCreate):
    obj = models.Submission(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Submission already exists for this student on this paper")
    return obj

async def add_answer(db: AsyncSession, data: schemas.AnswerCreate):
    obj = models.Answer(**data.model_dump())
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Answer for this question already exists in this submission")
    return obj

async def recalc_submission_total(db: AsyncSession, submission_id: int):
    # Sum all answer scores into total_marks
    res = await db.execute(
        select(func.coalesce(func.sum(models.Answer.score), 0)).where(models.Answer.submission_id == submission_id)
    )
    total = res.scalar_one()
    await db.execute(
        update(models.Submission).where(models.Submission.id == submission_id).values(total_marks=total)
    )
    await db.commit()
    return total
