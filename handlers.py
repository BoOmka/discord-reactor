import asyncio
import typing as t
from collections import defaultdict

import discord
import discord_slash

import config
from helpers import (
    get_message_id_from_id_or_url,
    prepare_text,
)


class CharToEmojiConverter:
    def __init__(self, ctx: discord_slash.SlashContext, text: str):
        self._text = text
        self._ctx = ctx
        self.default_emoji_iterators: t.Dict[str, t.Iterator[str]] = {
            k: iter(v.emojis)
            for k, v in config.CHARS_TO_EMOJIS_MAP.items()
        }
        self.custom_emojis: t.List[discord.Emoji] = []
        self.custom_emoji_iterators: t.Dict[str, t.Iterator[str]] = {}

    async def create_missing_emojis(self, text: str) -> None:
        counter_dict = defaultdict(int)
        for char in text:
            counter_dict[char] += 1

        missing_char_count_dict = defaultdict(int)
        for char, count in counter_dict.items():
            if char not in self.default_emoji_iterators:
                continue
            if (missing_char_count := count - len(config.CHARS_TO_EMOJIS_MAP[char].emojis)) > 0:
                missing_char_count_dict[char] = missing_char_count

        custom_emoji_dict = defaultdict(list)
        for char, count in missing_char_count_dict.items():
            _emoji = config.CHARS_TO_EMOJIS_MAP[char]
            for _ in range(count):
                with open(f"emojis/{_emoji.file}", "rb") as f:
                    emoji: discord.Emoji = await self._ctx.guild.create_custom_emoji(
                        name=f"reactor_{_emoji.char}",
                        image=f.read(),
                    )
                self.custom_emojis.append(emoji)
                custom_emoji_dict[char].append(str(emoji))
        self.custom_emoji_iterators = {k: iter(v) for k, v in custom_emoji_dict.items()}

    async def delete_custom_emojis(self) -> None:
        coros = []
        for emoji in self.custom_emojis:
            coros.append(emoji.delete(reason="We won't need this anymore"))
        await asyncio.gather(*coros)

    def emoji_seq(self) -> t.Generator[str, None, None]:
        for char in self._text:
            try:
                emoji: str = next(self.default_emoji_iterators[char])
            except (StopIteration, KeyError):
                try:
                    emoji: str = next(self.custom_emoji_iterators[char])
                except (StopIteration, KeyError):
                    continue
            print(emoji)
            yield emoji

    async def __aenter__(self) -> 'CharToEmojiConverter':
        await self.create_missing_emojis(self._text)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.delete_custom_emojis()


async def react(ctx: discord_slash.SlashContext, text: str, message_id_or_url: str) -> None:
    await ctx.defer(hidden=True)

    text = prepare_text(text)

    if message_id_or_url:
        try:
            message_id = get_message_id_from_id_or_url(message_id_or_url)
        except ValueError:
            await ctx.send(content='Wrong message ID or URL format', hidden=True)
            return
    else:
        try:
            last_message = (await ctx.channel.history(limit=1).flatten())[0]
            message_id = last_message.id
        except KeyError:
            await ctx.send("No messages to react to", hidden=True)
            return

    try:
        await _react(ctx, text, message_id)
    except:
        await ctx.send("Unexpected error occured", hidden=True)
        raise


async def _react(ctx: discord_slash.SlashContext, text: str, message_id: int) -> None:
    message = ctx.bot.get_channel(ctx.channel_id).get_partial_message(message_id)
    async with CharToEmojiConverter(ctx, text) as converter:
        coros = []
        for emoji in converter.emoji_seq():
            coros.append(message.add_reaction(emoji))
        await asyncio.gather(*coros)
    await ctx.send(content=f"Cleaned up your text and reacted with: ```{text}```", hidden=True)
