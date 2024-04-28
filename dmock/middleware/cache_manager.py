class CacheManager:
    _instance = None
    _results = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CacheManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def add_result(self, func_name, result):
        self._results[func_name] = result

    def get_result(self, func_name):
        return self._results.get(func_name)

singleton = CacheManager()

def store_result_decorator(func):
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        singleton.add_result(func.__name__, result)
        return result
    return wrapper