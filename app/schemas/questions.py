from pydantic import BaseModel


class QuestionReadSchema(BaseModel):
    word: str
    options: list[str]
    correct: str
    direction: str
