from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=schemas.StudentRead, status_code=201)
async def create_student(payload: schemas.StudentCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_student(db, payload)

@router.get("/", response_model=List[schemas.StudentRead])
async def list_students(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.list_students(db, skip, limit)
