import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging

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
