from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/", response_model=schemas.QuestionRead, status_code=201)
async def create_question(payload: schemas.QuestionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_question(db, payload)

@router.get("/by-paper/{paper_id}", response_model=List[schemas.QuestionRead])
async def list_questions(paper_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.list_questions_for_paper(db, paper_id)
