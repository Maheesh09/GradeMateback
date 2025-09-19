from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import schemas, crud
from ..models import QuestionType, SchemeMCQKey, Question, SchemeQuestion, Answer
from sqlalchemy import select

router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/", response_model=schemas.AnswerRead, status_code=201)
async def add_answer(payload: schemas.AnswerCreate, db: AsyncSession = Depends(get_db)):
    """
    Adds an answer; if MCQ and scheme info available, auto-score.
    """
    # Try a tiny auto-score for MCQ using scheme if provided
    score = 0
    if payload.scheme_question_id and payload.chosen_option:
        # find question type:
        sq = await db.execute(select(SchemeQuestion).where(SchemeQuestion.id == payload.scheme_question_id))
        sq = sq.scalar_one_or_none()
        if sq:
            q = await db.execute(select(Question).where(Question.id == sq.question_id))
            q = q.scalar_one_or_none()
            if q and q.type == QuestionType.MCQ:
                keys = await db.execute(
                    select(SchemeMCQKey).where(SchemeMCQKey.scheme_question_id == payload.scheme_question_id)
                )
                options = {k.option_code: (k.is_correct, k.partial_credit or 0) for k in keys.scalars().all()}
                if payload.chosen_option in options:
                    is_correct, partial = options[payload.chosen_option]
                    score = partial if not is_correct else (q.max_marks or 1)

    # create the answer
    ans = await crud.add_answer(db, schemas.AnswerCreate(**payload.dict(), ))  # create first
    # if we computed a score, update and recalc submission total
    if score:
        ans.score = score
        await db.commit()
        await db.refresh(ans)
        await crud.recalc_submission_total(db, ans.submission_id)

    return ans
