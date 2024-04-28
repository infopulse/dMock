import os
from dotenv import load_dotenv
from importlib.metadata import distribution

load_dotenv()

# VERSION = distribution('dMock').version
# os.getenv()

CACHE_TTL = int(os.getenv('CACHE_TTL_MINUTES', default=1440))

# ---- Logging ----
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'dmock.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'] if os.getenv('LOG_TO_FILE', default='true').lower() == 'true' else [
                'console'],
            'level': os.getenv('LOG_LEVEL', default='INFO'),
            'propagate': True
        }
    }
}

DB_CONFIG = {
    "connections": {
        "default": os.getenv('DB_URL', default='sqlite://db.sqlite3')
    },
    "apps": {
        "models": {
            "models": ["dmock.models.models"],
            "default_connection": "default",
        }
    }
}
