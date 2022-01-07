def process_channel_headers_to_dict(headers_data):
    if isinstance(headers_data, dict):
        return headers_data

    try:
        return {data[0].decode(): data[1].decode() for data in headers_data}
    except (ValueError, AttributeError):
        return {data[0]: data[1] for data in headers_data}
