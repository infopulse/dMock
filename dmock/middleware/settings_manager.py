from async_lru import alru_cache
from dmock.settings import CACHE_TTL
from dmock.models.models import Settings


@alru_cache(maxsize=None, ttl=60 * CACHE_TTL)
async def get_setting(key: str) -> str or None:
    s = await Settings.get_or_none(key=key)
    if s:
        return s.value


async def set_setting(key: str, value: str):
    setting = await Settings.get_or_none(key=key)
    if setting:
        setting.value = value
        await setting.save()
    else:
        await Settings.create(key=key, value=value)
    get_setting.cache_clear()
