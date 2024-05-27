from pathlib import Path
from typing import Optional, Any

from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    Settings class with constants and validators
    """
    # list of sores with urls of catalog and links of each category
    ROOT_URLS: dict[str, tuple[str, str]] = {
        "wildberries": (
            'https://www.wildberries.ru/catalog',
            'https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v3.json')
    }

    WILDBERRIES_HEADERS: dict = {"Accept": "*/*",
                                 "Accept-Encoding": "gzip, deflate, br, zstd",
                                 "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                                 "Connection": "keep-alive",
                                 "Dnt": "1",
                                 "Host": "catalog.wb.ru",
                                 }

    # logger config
    LOGGER_PATH: Path = BASE_DIR / 'logs'
    LOGGER_ROTATION: str = "10 MB"
    LOGGER_COMPRESSION: str = "zip"
    LOGGER_DEBUG: bool = False
    LOGGER_LEVELS: list = []

    @field_validator("LOGGER_LEVELS")
    @classmethod
    def assemble_logger_level(cls, v: Optional[list], info: ValidationInfo) -> Any:
        if v:
            return v

        debug_lvl = info.data.get("LOGGER_DEBUG")

        if debug_lvl is True:
            return ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
        else:
            return ["INFO", "WARNING", "ERROR", "CRITICAL"]

    @field_validator("LOGGER_PATH")
    @classmethod
    def assemble_logger_path(cls, v: Optional[list], info: ValidationInfo) -> Any:
        if v:
            return v

        python_path = info.data.get("PYTHONPATH")
        if python_path:
            return Path(python_path).resolve() / 'logs'

        return BASE_DIR / 'logs'


settings = Settings()
