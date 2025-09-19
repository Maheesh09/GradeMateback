from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/", response_model=schemas.SubmissionRead, status_code=201)
async def create_submission(payload: schemas.SubmissionCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_submission(db, payload)
