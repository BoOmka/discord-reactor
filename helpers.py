def get_message_id_from_id_or_url(message_id_or_url: str) -> int:
    message_id_str = message_id_or_url.rsplit('/', 1)[-1]
    return int(message_id_str)