import os
from dotenv import load_dotenv
from importlib.metadata import distribution

load_dotenv()

# VERSION = distribution('dMock').version
# os.getenv()


DB_CONFIG = {
    "connections": {
        "default": os.getenv('DB_URL', default='sqlite://db.sqlite3')
    },
    "apps": {
        "models": {
            "models": ["dmock.models.models",
                       "aerich.models"],
            "default_connection": "default",
        }
    }
}
