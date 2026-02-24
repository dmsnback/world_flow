import logging

from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.words import Word
from app.schemas.words import WordCreateSchema

logger = logging.getLogger(__name__)


class CRUDWord:

    async def create_word(self, word: WordCreateSchema, session: AsyncSession):
        try:
            new_word = Word(**word.model_dump())
            session.add(new_word)
            await session.flush()
            await session.commit()
            await session.refresh(new_word)
            logger.info(f"Добавлеено слово {new_word}")
            return new_word
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении слова: {e}")
            raise

    async def get_all_words(self, session: AsyncSession):
        try:
            query = select(Word)
            result = await session.execute(query)
            words = result.scalars().all()
            logger.info("Получен список всех слов")
            return words
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении списка слов: {e}")
            raise

    async def get_word(self, word: str, session: AsyncSession):
        try:
            query = select(Word).where(
                or_(Word.english == word, Word.russian == word)
            )
            result = await session.execute(query)
            find_word = result.scalars().first()
            if find_word:
                logger.info(f"Получено слово: '{find_word}'")
            else:
                logger.warning(f"Слово '{word}' не найдено в базе")
            return find_word
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении слова {word}: {e}")
            raise
