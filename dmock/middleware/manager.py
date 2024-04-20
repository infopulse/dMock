from async_lru import alru_cache

from dmock.models.models import Mock, Rules, MockLog, Settings


# TODO make cache ttl configurable DB parameter
@alru_cache(maxsize=None, ttl=60 * 60 * 24)
async def get_mock(id: int):
    return await Mock.get_or_none(id=id)


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
