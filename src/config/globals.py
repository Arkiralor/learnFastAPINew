from os import getenv, path, makedirs
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = getenv("PROJECT_NAME", "Learn FastAPI v2")
    SECRET_KEY: Optional[str] = getenv("SECRET_KEY")
    DEBUG: bool = getenv("DEBUG", False)
    BASE_URL: str = getenv("BASE_URL", "http://localhost:8000")
    MONGO_URI: str = getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str = getenv("MONGO_DB", "fastapi")
    MAX_ITEMS_PER_PAGE: int = 10
    JWT_ALGORITHM: str = getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_TIME: int = 3600  # in seconds

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Optional[str] = None
    ENV_LOG_FILE: Optional[str] = None
    ENV_LOG_FILE_NAME: str = "app.log"

    def model_post_init(self, __context):
        self.LOG_DIR = path.join(str(self.BASE_DIR), "logs")
        if not path.exists(self.LOG_DIR):
            makedirs(self.LOG_DIR)
        self.ENV_LOG_FILE = path.join(self.LOG_DIR, self.ENV_LOG_FILE_NAME)
        if not path.exists(self.ENV_LOG_FILE):
            with open(self.ENV_LOG_FILE, mode="w+t", encoding="utf-8") as f:
                f.write("")

        
        



settings = Settings()