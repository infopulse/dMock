import asyncio
import logging.config
from dmock.middleware.mock_manager import (get_matching_mocks, log_request,
                                           get_top_priority_mock, create_mock_automatically, has_duplicates)
from dmock.settings import LOGGING_CONFIG
from dmock.misc.misc import bytes_to_str

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

text_content_types = [
    "text/plain",
    "text/html",
    "text/css",
    "text/javascript",  # deprecated
    "application/javascript",
    "application/json",
    "application/xml",
    "text/xml",
    "application/xhtml+xml",
    "text/csv",
    "text/markdown",
    "application/rtf"
]


async def dispatch_request(method: str, url: str, headers: dict, body: str, query_params: dict) -> dict:
    logger.info(f"Dispatching request {method} {url}")
    # TODO add json parameter
    mocks = await get_matching_mocks(method, url, body, headers, query_params)
    mock_ids = [m.id for m in mocks]
    logger.debug(f"Matching mocks: {mock_ids}")
    response_mock = await get_top_priority_mock(mocks)
    response_mock.requests_count += 1
    await response_mock.save()
    logger.info(f"Selected mock: {response_mock.id}. {response_mock.name}")
    if response_mock.is_default and not await has_duplicates(method, url):
        await create_mock_automatically(response_mock, method, url, headers, body)

    await asyncio.sleep(response_mock.delay)
    await log_request(response_mock, method, url, headers, body, mock_ids)

    if response_mock.response_headers is None:
        # by default return plain text
        response_header = {"Content-Type": "text/plain"}
        response_body = bytes_to_str(response_mock.response_body)
    elif response_mock.response_headers.get('Content-Type') is None:
        response_header = {"Content-Type": "text/plain"}
        response_header.update(response_mock.response_headers)
        response_body = bytes_to_str(response_mock.response_body)
    elif response_mock.response_headers.get('Content-Type') in text_content_types:
        response_header = response_mock.response_headers
        response_body = bytes_to_str(response_mock.response_body)
    else:
        response_header = response_mock.response_headers
        response_body = response_mock.response_body

    return {
        "mock_id": response_mock.id,
        "status_code": response_mock.status_code,
        "headers": response_header,
        "body": response_body
    }
