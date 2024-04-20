import json


def flatten_json(json_obj: dict or list, name: str = '', sep: str = '.') -> dict:
    result = dict()
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            full_key = key if name == '' else f'{name}{sep}{key}'
            if isinstance(value, (dict, list)):
                result.update(flatten_json(value, full_key, sep))
            else:
                result[full_key] = value
    elif isinstance(json_obj, list):
        for index, value in enumerate(json_obj):
            full_key = str(index) if name == '' else f'{name}{sep}{index}'
            if isinstance(value, (dict, list)):
                result.update(flatten_json(value, full_key, sep))
            else:
                result[full_key] = value
    else:
        raise ValueError('Invalid JSON object')

    return result


def sort_flat_json(json_obj: dict) -> dict:
    return dict(sorted(json_obj.items()))


def get_wild_cards(json_obj: dict) -> list:
    return [key for key, value in json_obj.items() if value == '*']


def is_subset(small_dict: dict, big_dict: dict):
    return all(item in big_dict.items() for item in small_dict.items())


def clear_wild_keys(json_obj: dict, wild_keys: list) -> dict:
    return {key: value for key, value in json_obj.items() if key not in wild_keys}
