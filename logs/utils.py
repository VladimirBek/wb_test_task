from loguru import logger
from core.config import settings


def add_named_logger(name: str):
    filter_by_name = lambda record: record["extra"].get("name") == name

    for level in settings.LOGGER_LEVELS:
        logger.add(
            settings.LOGGER_PATH / name / f"{level.lower()}.log",
            level=level,
            rotation=settings.LOGGER_ROTATION,
            compression=settings.LOGGER_COMPRESSION,
            enqueue=True,
            filter=filter_by_name
        )

    return logger.bind(name=name)
