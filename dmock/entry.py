import logging
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from main import app

log = logging.getLogger("dmock")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


def main():
    asyncio.run(serve(app, Config()))


if __name__ == "__main__":
    main()
