import logging
import logging.config
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple" : {
            "format" : "%(asctime)s [%(levelname)s|%(name)s|%(module)s|L%(lineno)d]: %(message)s",
            "datefmt" : "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level" : "DEBUG",
            "formatter" : "simple",
            "stream" : "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level" : "DEBUG",
            "formatter" : "simple",
            "filename" : "logs/zork.log",
            "maxBytes" : 10*1024*1024,
            "backupCount" : 5
        },
        "info_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level" : "INFO",
            "formatter" : "simple",
            "filename" : "logs/zork-info.log",
            "maxBytes" : 10*1024*1024,
            "backupCount" : 5
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "file", "info_file"],
            "level": "DEBUG"
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
