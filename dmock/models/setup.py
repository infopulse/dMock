import logging.config
from tortoise import transactions
from dmock.models.models import Mock, MockLog, Rules, Settings
from dmock.settings import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


async def set_data() -> Mock:
    logger.info("Setting up default data")
    async with transactions.in_transaction():
        default_mock = await Mock.get_or_create(id=1, name="Master mock (default)",
                                                method="ANY", url="/",
                                                response_body="hello world",
                                                response_headers={"Content-Type": "text/plain"},
                                                status_code=200, is_default=True,
                                                labels=["default"], status="active")
        await Rules.get_or_create(mock=default_mock[0], type="1-default",
                                  operation="any", key="", is_active=True)
    return default_mock[0]
