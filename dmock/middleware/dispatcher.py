import asyncio
import logging.config
from dmock.middleware.mock_manager import (get_matching_mocks, log_request,
                                           get_top_priority_mock, create_mock_automatically)
from dmock.settings import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


async def dispatch_request(method: str, url: str, headers: dict, body: str) -> dict:
    logger.info(f"Dispatching request {method} {url}")
    # TODO add json parameter
    mocks = await get_matching_mocks(method, url, body, headers)
    mock_ids = [m.id for m in mocks]
    logger.debug(f"Matching mocks: {mock_ids}")
    response_mock = await get_top_priority_mock(mocks)
    response_mock.requests_count += 1
    await response_mock.save()
    logger.info(f"Selected mock: {response_mock.id}. {response_mock.name}")
    if response_mock.is_default:
        await create_mock_automatically(response_mock, method, url, headers, body)

    await asyncio.sleep(response_mock.delay)
    await log_request(response_mock, method, url, headers, body, mock_ids)

    return {
        "mock_id": response_mock.id,
        "status_code": response_mock.status_code,
        "headers": response_mock.response_headers,
        "body": response_mock.response_body
    }
