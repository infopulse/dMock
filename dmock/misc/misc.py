import json


def bytes_to_str(byte_data: bytes, encoding: str = 'utf-8') -> str:
    try:
        return byte_data.decode(encoding)
    except UnicodeDecodeError:
        # Fallback handling strategy if decoding fails
        return byte_data.decode(encoding, errors='ignore')


def str_to_bytes(str_data: str, encoding: str = 'utf-8') -> bytes:
    try:
        return str_data.encode(encoding)
    except UnicodeEncodeError:
        return str_data.encode(encoding, errors='ignore')


def nice_body_repr(body: bytes) -> str or dict:
    if body is None:
        return None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return bytes_to_str(body)
