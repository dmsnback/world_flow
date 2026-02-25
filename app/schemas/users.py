from datetime import datetime

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    telegram_id: int
    telegram_username: str | None = None


class UserCreateSchema(UserBaseSchema):
    pass


class UserReadSchema(UserBaseSchema):
    id: int
    create_at: datetime

    class Config:
        orm_mode = True
