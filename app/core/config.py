from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    description: str
    database_url: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
