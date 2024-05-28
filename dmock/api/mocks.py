from dmock.middleware.mock_manager import (get_mocks, get_mock, create_mock_manually)

class API:
    @staticmethod
    async def get_mocks_json() -> dict:
        mocks = await get_mocks()
        return {"mocks": [await mock.to_dict() for mock in mocks],
                "total": len(mocks)}

    @staticmethod
    async def get_mock_json(mock_id: int) -> dict:
        mock = await get_mock(id=mock_id)
        if mock:
            return await mock.to_dict()

    @staticmethod
    async def get_rules_json(mock_id: int) -> dict:
        mock = await get_mock(id=mock_id)
        if mock:
            rules = await mock.rules
            return {"rules": [await rule.to_dict() for rule in rules]}

    @staticmethod
    async def get_mock_logs_json(mock_id: int) -> dict:
        mock = await get_mock(id=mock_id)
        if mock:
            logs = await mock.logs
            return {"logs": [await log.to_dict() for log in logs]}

    @staticmethod
    async def create_mock(mock: dict) -> dict:
        mock = await create_mock_manually(**mock)
        return await mock.to_dict()
