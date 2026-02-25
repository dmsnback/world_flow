from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.users import CRUDUser
from app.schemas.users import UserCreateSchema, UserReadSchema

user_router = APIRouter(
    prefix="/users",
    tags=[
        "Пользователи",
    ],
)

user_crud = CRUDUser()


@user_router.post(
    "", response_model=UserReadSchema, summary="Добавление пользователя"
)
async def add_user(
    user: UserCreateSchema, session: AsyncSession = Depends(get_session)
) -> UserReadSchema:
    try:
        add_user = await user_crud.create_user(user, session)
        return add_user
    except Exception as e:
        raise e


@user_router.delete("/{telegram_id}", summary="Удаление Пользователя")
async def delete_user(
    telegram_id: int, session: AsyncSession = Depends(get_session)
) -> dict:
    user = await user_crud.get_user(telegram_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    try:
        await user_crud.delete_user(user, session)
        return {"detail": f"Пользователь id={telegram_id} удален"}
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении пользователя",
        )


@user_router.get(
    "/all",
    response_model=list[UserReadSchema],
    summary="Получение всех пользователей",
)
async def get_all_users(
    session: AsyncSession = Depends(get_session),
) -> list[UserReadSchema]:
    try:
        users = await user_crud.get_all_users(session)
        if not users:
            raise HTTPException(
                status_code=status.HTT_404_NOT_FOUND,
                detail="Список пользоввателей отсутсттвует",
            )
        return users
    except Exception as e:
        raise e


@user_router.get(
    "/{telegram_id}",
    response_model=UserReadSchema,
    summary="Получение пользователя по telegram_id",
)
async def get_user(
    telegram_id: int, session: AsyncSession = Depends(get_session)
) -> UserReadSchema:
    try:
        user = await user_crud.get_user(telegram_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь id={telegram_id} не найден",
            )
        return user
    except Exception as e:
        raise e
