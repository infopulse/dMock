from tortoise import BaseDBAsyncClient
from dmock.models.models import Settings


async def upgrade(db: BaseDBAsyncClient) -> str:
    default_setting = Settings(key='default_key', value='default_value')
    await default_setting.save()
    return ''


async def downgrade(db: BaseDBAsyncClient) -> str:
    await Settings.filter(key='default_key').delete()
    return ''
