import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.users import UserCreateSchema

logger = logging.getLogger(__name__)


class CRUDUser:

    async def create_user(self, user: UserCreateSchema, session: AsyncSession):
        try:
            new_user = User(**user.model_dump())
            session.add(new_user)
            await session.flush()
            await session.commit()
            await session.refresh(new_user)
            logger.info(
                f"Добавлен пользователь '{new_user.telegram_username}' id: {new_user.telegram_id} "
            )
            return new_user
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении пользователя: {e}")
            raise

    async def get_all_users(self, session: AsyncSession):
        try:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            logger.info("Получен список всех пользователей")
            return users
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при получении списка всех пользователей: {e}"
            )
            raise

    async def get_user(self, telegram_id: int, session: AsyncSession):
        try:
            query = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                logger.info(
                    f"Получен пользователь: '{user.telegram_username}' id={user.telegram_id}"
                )
                return user
            else:
                logger.warning(
                    f"Пользователь id={telegram_id} не найден в базе"
                )
                raise
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при получении пользователя id={telegram_id}: {e}"
            )
            raise

    async def delete_user(self, user: User, session: AsyncSession):
        try:
            await session.delete(user)
            await session.commit()
            logger.info(
                f"Пользователь: '{user.telegram_username}' id={user.telegram_id} удалён"
            )
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при удалении пользователя '{user.telegram_username}' id={user.telegram_id}: {e}"
            )
            raise
