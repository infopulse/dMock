import re
import json
import logging.config
from async_lru import alru_cache
from dmock.settings import CACHE_TTL, LOGGING_CONFIG
from dmock.models.models import Mock, Rules, MockLog, Settings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_mock(id: int):
    return await Mock.get_or_none(id=id)


@alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_mocks() -> list[Mock]:
    return await Mock.all()


@alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_rules(mock: Mock = None) -> list[Rules]:
    if mock:
        return await mock.rules
    else:
        return await Rules.all()


async def get_matching_mock(method: str, url: str, body: str, headers: dict):
    mocks = await get_mocks()
    for mock in mocks:
        if mock.method == method:
            rules = await get_rules(mock)
            for rule in rules:
                ...


def match_rule(rule: Rules, url: str, body: str, headers: dict) -> bool:
    match rule.type:
        case "2-url":
            return rule.key == url
        case "3-body":
            return rule.key == body
        case "4-header":
            return rule.key in headers and rule.value == headers[rule.key]
        case _:
            return False


def _rule_url_or_body_compare(rule: Rules, url_or_body: str) -> bool:
    match rule.operation:
        case "equals":
            return rule.key == url_or_body
        case "contains":
            return rule.key in url_or_body
        case "in":
            return url_or_body in rule.key
        case "regex":
            return bool(re.match(rule.key, url_or_body))
        case "starts_with":
            return url_or_body.startswith(rule.key)
        case "ends_with":
            return url_or_body.endswith(rule.key)
        case _:
            return False


def _rule_json_compare(rule: Rules, body: str) -> bool:
    try:
        body_json = json.loads(body)
    except json.JSONDecodeError:
        logger.error("Invalid request JSON body")
        return False

    try:
        rule_json = json.loads(rule.key)
    except json.JSONDecodeError as e:
        logger.error(e)
        raise e




def create_mock(name: str,
                status: str = "draft",
                labels: list = [],
                delay: int = 0,
                ):
    ...


def create_rule(mock: Mock,
                type: str,
                operation: str,
                key: str,
                ):
    ...


def clear_all_caches():
    get_mock.cache_clear()
    get_mocks.cache_clear()
    get_rules.cache_clear()
