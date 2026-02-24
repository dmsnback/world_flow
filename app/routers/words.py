from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.words import CRUDWord
from app.schemas.words import WordCreateSchema, WordReadSchema

word_router = APIRouter(
    prefix="/words",
    tags=[
        "Слова",
    ],
)

word_crud = CRUDWord()


@word_router.post(
    "",
    response_model=WordReadSchema,
    summary="Добавление слова",
)
async def add_word(
    word: WordCreateSchema, session: AsyncSession = Depends(get_session)
) -> WordReadSchema:
    try:
        add_word = await word_crud.create_word(word, session)
        return add_word
    except Exception as e:
        raise e


@word_router.get(
    "/all",
    response_model=list[WordReadSchema],
    summary="Получение списка всех слов",
)
async def get_all_words(
    session: AsyncSession = Depends(get_session),
) -> list[WordReadSchema]:
    try:
        words = await word_crud.get_all_words(session)
        if not words:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Список слов отсутсттвует",
            )
        return words
    except Exception as e:
        raise e


@word_router.get(
    "/{word}", response_model=WordReadSchema, summary="Получение слова"
)
async def get_word(
    word: str, session: AsyncSession = Depends(get_session)
) -> WordReadSchema:
    try:
        word = word.lower()
        find_word = await word_crud.get_word(word, session)
        if not find_word:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Слово не найдено",
            )
        return find_word
    except Exception as e:
        raise e
