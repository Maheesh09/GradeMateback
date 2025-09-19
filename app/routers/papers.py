from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/", response_model=schemas.PaperRead, status_code=201)
async def create_paper(payload: schemas.PaperCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_paper(db, payload)
