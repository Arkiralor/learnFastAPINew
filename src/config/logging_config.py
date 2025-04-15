from pydantic import BaseModel
from config.globals import settings


class LoggingConfig(BaseModel):
    VERBOSE_FMT: str = '[%(levelname)s|%(asctime)s.%(msecs)d|%(name)s|%(module)s|%(funcName)s:%(lineno)s]    %(message)s'
    LOCAL_FMT: str = '[%(asctime)s|%(name)s|%(module)s|%(funcName)s:%(lineno)s]    %(message)s'
    DATE_FMT: str = '%Y/%b/%d %H:%M:%S'

    CONFIG: dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': VERBOSE_FMT,
                'datefmt': DATE_FMT,
            },
            'local': {
                'format': LOCAL_FMT,
                'datefmt': DATE_FMT,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'local',
            },
            'root_file': {
                'class': 'logging.FileHandler',
                'filename': settings.ENV_LOG_FILE,
                'formatter': 'verbose',
                'encoding': 'utf-8',
            }
        },
        'loggers': {
            'root': {
                'handlers': [
                    'console',
                    'root_file'
                ],
                "level": 'INFO'
            },
            'watchfiles': {
                'handlers': [
                    'console'
                ],
                'level': 'WARNING',  # hide INFO
                'propagate': False,
            },
        },
    }

logging_config = LoggingConfig()
