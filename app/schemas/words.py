from datetime import datetime

from pydantic import BaseModel


class QuestionResponseSchema(BaseModel):
    word: str
    options: list[str]
    correct: str
    direction: str


class WordBaseSchema(BaseModel):
    english: str
    russian: str


class WordCreateSchema(WordBaseSchema):
    pass


class WordReadSchema(WordBaseSchema):
    id: int
    create_at: datetime
