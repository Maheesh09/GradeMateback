from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/schemes", tags=["schemes"])

@router.post("/", response_model=schemas.SchemeRead, status_code=201)
async def create_scheme(payload: schemas.SchemeCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_scheme(db, payload)

@router.post("/questions", response_model=schemas.SchemeQuestionRead, status_code=201)
async def add_scheme_question(payload: schemas.SchemeQuestionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_scheme_question(db, payload)

@router.post("/mcq-key", response_model=schemas.SchemeMCQKeyRead, status_code=201)
async def add_mcq_key(payload: schemas.SchemeMCQKeyCreate, db: AsyncSession = Depends(get_db)):
    return await crud.add_scheme_mcq_key(db, payload)

@router.post("/point", response_model=schemas.SchemePointRead, status_code=201)
async def add_point(payload: schemas.SchemePointCreate, db: AsyncSession = Depends(get_db)):
    return await crud.add_scheme_point(db, payload)
