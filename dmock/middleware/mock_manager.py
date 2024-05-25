import re
import json as js
import logging.config
from async_lru import alru_cache
from h11._abnf import status_code
from tortoise import transactions
from dmock.settings import CACHE_TTL, LOGGING_CONFIG
from dmock.models.models import Mock, Rules, MockLog
from dmock.middleware.matchers import match_rule

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


# @alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_mock(id: int):
    return await Mock.get_or_none(id=id)


# @alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_mocks() -> list[Mock]:
    return await Mock.all()


# @alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_rules(mock: Mock = None) -> list[Rules]:
    if mock:
        return await mock.rules
    else:
        return await Rules.all()


# @alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_matching_mocks(method: str, url: str,
                             body: str = '', json: dict or list = None, headers: dict = None) -> list[Mock]:
    mocks = await get_mocks()
    result = list()
    for mock in mocks:
        if mock.method == method and mock.status == "active":
            rules = await get_rules(mock)
            mock_ok = True
            for rule in rules:
                if not rule.is_active:
                    continue
                if not match_rule(rule, url, body, json, headers):
                    mock_ok = False
                    break
            if mock_ok:
                result.append(mock)
    return result


async def get_top_priority_mock(mocks: list[Mock]) -> Mock:
    def get_priority(mock: Mock):
        if mock.priority:
            return mock.priority
        else:
            return mock.id

    return max(mocks, key=lambda x: get_priority(x))


async def create_mock_manually(name: str,
                               status: str = "draft",
                               labels: list = None,
                               delay: int = 0,
                               is_default: bool = False,
                               priority: int = None,
                               method: str = None,
                               url: str = None,
                               rules: list = None,
                               **kwargs) -> Mock:
    logger.info(f"Creating mock {name}")
    async with transactions.in_transaction():
        mock = await Mock.create(name=name, status=status,
                                 labels=labels, delay=delay,
                                 is_default=is_default, priority=priority,
                                 method=method, url=url, **kwargs)
        if rules:
            for rule in rules:
                await Rules.create(mock=mock, **rule)
    logger.info(f"Mock {name} created. id: {mock.id}, rules: {len(rules)}")
    clear_all_caches()
    return mock


async def create_mock_automatically(mock: Mock,
                                    method: str,
                                    url: str,
                                    request_headers: dict = None,
                                    request_body: str = None,
                                    **kwargs) -> Mock:
    # TODO search for similar mocks

    logger.info(f"Creating mock for {method} {url}")
    async with transactions.in_transaction():
        a_mock = await Mock.create(name=f"{method} {url}", method=method, url=url, **kwargs)
        # logging record for new potential mock
        await log_request(a_mock, method, url, request_headers, request_body, [mock.id])

    logger.info(f"Mock created. id: {mock.id}")
    clear_all_caches()
    return mock


async def create_rule(mock: Mock,
                      type: str,
                      operation: str,
                      key: str,
                      is_active: bool = True,
                      ):
    if mock.is_default:
        raise ValueError("Cannot add rule to default mock")
    return await Rules.create(mock=mock, type=type, operation=operation, key=key, is_active=is_active)


async def edit_mock(mock: Mock, **kwargs):
    for key in kwargs.keys():
        if key in ['method', 'is_action', 'is_default', 'status']:
            raise ValueError(f"Cannot change {key} of mock")
    logger.info(f"Editing mock {mock.id}: {mock.name}")
    async with transactions.in_transaction():
        for key, value in kwargs.items():
            setattr(mock, key, value)
        await mock.save()
    logger.info(f"Mock {mock.id}: {mock.name} edited")
    clear_all_caches()
    return mock


async def edit_rule(rule: Rules, **kwargs):
    if rule.mock.is_default:
        raise ValueError("Cannot edit rule of default mock")
    logger.info(f"Editing rule {rule.id} of mock {rule.mock.id}: {rule.mock.name}")
    async with transactions.in_transaction():
        for key, value in kwargs.items():
            setattr(rule, key, value)
        await rule.save()
    logger.info(f"Rule {rule.id} edited")
    clear_all_caches()
    return rule


async def delete_mock(mock: Mock):
    if mock.is_default:
        raise ValueError("Cannot delete default mock")
    logger.info(f"Deleting mock {mock.id}: {mock.name}")
    await mock.delete()
    logger.info(f"Mock {mock.id}: {mock.name} deleted")
    clear_all_caches()


async def delete_rule(rule: Rules):
    if rule.mock.is_default:
        raise ValueError("Cannot delete rule of default mock")
    logger.info(f"Deleting rule {rule.id} of mock {rule.mock.id}: {rule.mock.name}")
    await rule.delete()
    logger.info(f"Rule {rule.id} deleted")
    clear_all_caches()


async def log_request(mock: Mock, method: str, url: str, headers: dict, body: str, matched_mock_ids: list):
    await MockLog.create(mock=mock, request_method=method, request_url=url, request_headers=headers, request_body=body,
                         response_headers=mock.response_headers, response_body=mock.response_body,
                         status_code=mock.status_code, mocks_matched_ids=matched_mock_ids)


def clear_all_caches():
    # get_mock.cache_clear()
    # get_mocks.cache_clear()
    # get_rules.cache_clear()
    # get_matching_mocks.cache_clear()
    logger.info("All caches cleared")
