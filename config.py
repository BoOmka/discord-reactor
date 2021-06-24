import typing as t

from models import Emoji

LOG_LEVEL = 'INFO'

CHARS_TO_EMOJIS_MAP: t.Dict[str, Emoji] = {
    "a": Emoji("a", ["🇦", "🅰️"], "a.png"),
    "b": Emoji("b", ["🇧", "🅱️"], "b.png"),
    "c": Emoji("c", ["🇨"], "c.png"),
    "d": Emoji("d", ["🇩"], "d.png"),
    "e": Emoji("e", ["🇪"], "e.png"),
    "f": Emoji("f", ["🇫"], "f.png"),
    "g": Emoji("g", ["🇬"], "g.png"),
    "h": Emoji("h", ["🇭"], "h.png"),
    "i": Emoji("i", ["🇮", "ℹ️"], "i.png"),
    "j": Emoji("j", ["🇯"], "j.png"),
    "k": Emoji("k", ["🇰"], "k.png"),
    "l": Emoji("l", ["🇱"], "l.png"),
    "m": Emoji("m", ["🇲"], "m.png"),
    "n": Emoji("n", ["🇳"], "n.png"),
    "o": Emoji("o", ["🇴"], "o.png"),
    "p": Emoji("p", ["🇵"], "p.png"),
    "q": Emoji("q", ["🇶"], "q.png"),
    "r": Emoji("r", ["🇷"], "r.png"),
    "s": Emoji("s", ["🇸"], "s.png"),
    "t": Emoji("t", ["🇹"], "t.png"),
    "u": Emoji("u", ["🇺"], "u.png"),
    "v": Emoji("v", ["🇻"], "v.png"),
    "w": Emoji("w", ["🇼"], "w.png"),
    "x": Emoji("x", ["🇽"], "x.png"),
    "y": Emoji("y", ["🇾"], "y.png"),
    "z": Emoji("z", ["🇿"], "z.png"),
}
