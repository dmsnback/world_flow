import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.routers.questions import question_router
from app.routers.users import user_router
from app.routers.words import word_router

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Приложение Word Flow запущено")
    yield
    logging.info("Приложение Word Flow остановлено")


app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    lifespan=lifespan,
)

app.include_router(word_router)
app.include_router(question_router)
app.include_router(user_router)
