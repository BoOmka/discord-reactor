import config


def get_message_id_from_id_or_url(message_id_or_url: str) -> int:
    message_id_str = message_id_or_url.rsplit('/', 1)[-1]
    return int(message_id_str)


def prepare_text(text: str) -> str:
    return ''.join(x for x in text.lower() if x in config.CHARS_TO_REGIONAL_INDICATORS_MAP)
