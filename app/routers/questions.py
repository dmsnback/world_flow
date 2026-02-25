import random

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.words import CRUDWord
from app.schemas.questions import QuestionReadSchema

question_router = APIRouter(
    prefix="/questions",
    tags=[
        "Вопросы",
    ],
)

word_crud = CRUDWord()


@question_router.get(
    "", response_model=QuestionReadSchema, summary="Получение вопроса"
)
async def get_question(
    session: AsyncSession = Depends(get_session),
) -> QuestionReadSchema:
    words = await word_crud.get_all_words(session)
    if len(words) < 4:
        return {"error": "В базее должно быть минимум 4 слова"}

    correct_word = random.choice(words)
    options_words = random.sample(words, 4)
    direction = random.choice(["en-ru", "ru-en"])

    if direction == "en-ru":
        question_word = correct_word.english
        correct_answer = correct_word.russian
        options = [w.russian for w in options_words]
    else:
        question_word = correct_word.russian
        correct_answer = correct_word.english
        options = [w.english for w in options_words]

    if correct_answer not in options:
        options[0] = correct_answer

    random.shuffle(options)

    return {
        "word": question_word,
        "options": options,
        "correct": correct_answer,
        "direction": direction,
    }
