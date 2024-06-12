def bytes_to_str(byte_data, encoding='utf-8'):
    try:
        return byte_data.decode(encoding)
    except UnicodeDecodeError:
        # Fallback handling strategy if decoding fails
        return byte_data.decode(encoding, errors='ignore')
