from dataclasses import dataclass
import typing as t


@dataclass
class Emoji:
    """
    Emoji dataclass allows to associate char with corresponding default emojies
    and a file containing image for duplicated characters.
    """
    char: str
    emojis: t.Tuple[str]
    file: str

    def __init__(self, char: str, emojis: t.Iterable[str], file: str):
        self.char = char
        self.emojis = tuple(emoji for emoji in emojis)
        self.file = file
