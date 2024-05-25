from pathlib import Path
from typing import Optional, Any, Dict

from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Settings class with constants and validators
    """
    ROOT_URLS: list[str] = [
        {
            'https://www.wildberries.ru/catalog/':
                'https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v3.json'
        }
    ]
    # logger config
    LOGGER_PATH: Path = None
    LOGGER_ROTATION: str = "10 MB"
    LOGGER_COMPRESSION: str = "zip"
    LOGGER_DEBUG: bool = False
    LOGGER_LEVELS: list = []

    @field_validator("LOGGER_LEVELS")
    def assemble_logger_level(cls, v: Optional[list], info: FieldValidationInfo) -> Any:

        if v:
            return v

        debug_lvl = info.data.get("LOGGER_DEBUG")

        if debug_lvl is True:
            return ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
        else:
            return ["INFO", "WARNING", "ERROR", "CRITICAL"]

    @field_validator("LOGGER_PATH")
    def assemble_logger_path(cls, v: Optional[list],  info: FieldValidationInfo) -> Any:

        if v:
            return v

        python_path = info.data.get("PYTHONPATH")
        if python_path:
            return Path(python_path).resolve() / 'app' / 'logs'

        return BASE_DIR / 'logs'

    class Config:
        case_sensitive = True


settings = Settings()
