import re
import json as js
import logging.config
from async_lru import alru_cache
from h11._abnf import status_code
from tortoise import transactions
from dmock.settings import CACHE_TTL, LOGGING_CONFIG
from dmock.models.models import Mock, Rule, MockLog
from dmock.middleware.matchers import match_rule
from dmock.misc.misc import str_to_bytes

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_mock(id: int):
    return await Mock.get_or_none(id=id)


@alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_mocks() -> list[Mock]:
    return await Mock.all()


# @alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_rules(mock: Mock = None) -> list[Rule]:
    if mock:
        return await mock.rules
    else:
        return await Rule.all()


# @alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_matching_mocks(method: str, url: str,
                             body: str = '', json: dict or list = None,
                             headers: dict = None, query_params: dict = None) -> list[Mock]:
    mocks = await get_mocks()
    result = list()
    for mock in mocks:
        if mock.is_default:
            result.append(mock)
            continue
        if method in [mock.method, "ANY"] and mock.status == "active":
            rules = await get_rules(mock)
            mock_ok_counter = 0
            active_rules = 0
            for rule in rules:
                if not rule.is_active:
                    continue
                active_rules += 1
                if match_rule(rule, url, body, json, headers, query_params):
                    mock_ok_counter += 1
                else:
                    break
            if mock_ok_counter > 0 and mock_ok_counter == active_rules:
                result.append(mock)
    return result


async def get_top_priority_mock(mocks: list[Mock]) -> Mock:
    def get_priority(mock: Mock):
        if mock.priority:
            return mock.priority
        else:
            return mock.id

    return max(mocks, key=lambda x: get_priority(x))


async def create_mock_manually( **kwargs) -> Mock:
    Mock.check_static_dynamic(**kwargs)
    name = kwargs.get('name')
    rules = kwargs.get('rules')
    if kwargs.get('response_body') is not None:
        kwargs['response_body'] = str_to_bytes(kwargs['response_body'])
    del kwargs['rules']
    logger.info(f"Creating mock {name}")
    async with transactions.in_transaction():
        mock = await Mock.create(**kwargs)
        len_rules = 0
        if rules:
            len_rules = len(rules)
            for rule in rules:
                await Rule.create(mock=mock, **rule)

    logger.info(f"Mock {name} created. id: {mock.id}, rules: {len_rules}")
    clear_all_caches()
    return mock


async def create_mock_automatically(mock: Mock,
                                    method: str,
                                    url: str,
                                    request_headers: dict = None,
                                    request_body: str = None,
                                    **kwargs) -> Mock:
    # TODO search for similar mocks
    default_status_code = 200
    logger.info(f"Creating mock for {method} {url}")
    async with transactions.in_transaction():
        a_mock = await Mock.create(name=f"{method} {url}", method=method,
                                   url=url, status_code=default_status_code,
                                   labels=["auto"], **kwargs)
        # logging record for new potential mock
        await log_request(a_mock, method, url, request_headers, request_body, [mock.id])

    logger.info(f"Mock created. id: {a_mock.id}")
    clear_all_caches()
    return mock


async def has_duplicates(method: str, url: str):
    mocks = await get_mocks()
    for mock in mocks:
        if mock.method == method and mock.url == url:
            logger.debug(f"Mock {mock.id} already exists for {method} {url}. Skipping automatic mock creation")
            return True
    return False

async def create_rule(mock: Mock,
                      type: str,
                      operation: str,
                      key: str,
                      is_active: bool = True,
                      ):
    if mock.is_default:
        raise ValueError("Cannot add rule to default mock")
    return await Rule.create(mock=mock, type=type, operation=operation, key=key, is_active=is_active)


async def edit_mock(mock: Mock, **kwargs) -> Mock:
    if mock.is_default:
        raise ValueError("Cannot edit default mock")
    logger.info(f"Editing mock {mock.id}: {mock.name}")
    if kwargs.get('response_body') is not None:
        kwargs['response_body'] = str_to_bytes(kwargs['response_body'])
    async with transactions.in_transaction():
        await mock.update(**kwargs)
    logger.info(f"Mock {mock.id}: {mock.name} edited")
    clear_all_caches()
    return mock


async def get_rule(id: int):
    return await Rule.get_or_none(id=id)


async def edit_rule(rule: Rule, **kwargs):
    mock = await rule.mock
    if mock.is_default:
        raise ValueError("Cannot edit rule of default mock")
    logger.info(f"Editing rule {rule.id} of mock {rule.mock.id}: {rule.mock.name}")
    async with transactions.in_transaction():
        for key, value in kwargs.items():
            setattr(rule, key, value)
        await rule.save()
    logger.info(f"Rule {rule.id} edited")
    clear_all_caches()
    return rule


async def delete_mock_by_id(id: int):
    mock = await get_mock(id)
    if not mock:
        raise (f"Mock {id} not found")
    await delete_mock(mock)


async def delete_mock(mock: Mock):
    if mock.is_default:
        raise ValueError("Cannot delete default mock")
    logger.info(f"Deleting mock {mock.id}: {mock.name}")
    await mock.delete()
    logger.info(f"Mock {mock.id}: {mock.name} deleted")
    clear_all_caches()


async def delete_rule(rule: Rule):
    mock = await rule.mock
    if mock.is_default:
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
    get_mock.cache_clear()
    get_mocks.cache_clear()
    # get_rules.cache_clear()
    # get_matching_mocks.cache_clear()
    logger.info("All caches cleared")
