import sys
from pathlib import Path
from loguru import logger
from src.config import settings

_logging_configured = False

def _console_filter(record) -> bool:
    return record['extra'].get('sink', 'both') in ('console', 'both')

def _file_filter(record) -> bool:
    return record['extra'].get('sink', 'both') in ('file', 'both')

def setup_logging():
    global _logging_configured
    if _logging_configured:
        return logger

    logger.remove()
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    LOG_FORMAT_COLORIZED = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
        '<level>{level: <8}</level> | '
        '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | '
        '<level>{message}</level> | '
        '<magenta>{extra}</magenta>'
    )

    logger.add(
        sys.stdout,
        format=LOG_FORMAT_COLORIZED,
        level=settings.LOG_LEVEL if settings.IS_DEBUG else 'INFO',
        colorize=True,
        filter=_console_filter,
    )

    logger.add(
        'logs/debug.log',
        level='DEBUG',
        rotation='10 MB',
        retention='7 days',
        compression='zip',
        serialize=True,
        filter=_console_filter,
    )

    logger.add(
        'logs/errors.log',
        level='ERROR',
        rotation='20 MB',
        retention='90 days',
        serialize=True,
        filter=_file_filter,
    )

    _logging_configured = True
    return logger