import asyncio
import typing as t
from collections import defaultdict

import aiofiles
import discord
import discord_slash

import config
from helpers import (
    get_message_id_from_id_or_url,
    prepare_text,
)


class Reaction:
    char: str  # char which is represented by reaction
    n: int  # number of reaction copy
    emoji: t.Union[discord.Emoji, discord.PartialEmoji]
    prepare_coro: t.Awaitable[None]

    def __init__(self, ctx: discord_slash.SlashContext, char: str, n):
        self._ctx = ctx
        self.char = char
        self.n = n
        self.prepare_coro = asyncio.create_task(self.prepare())

    async def prepare(self):
        """Prepare emoji (native or custom) for reaction"""
        _emoji = config.CHARS_TO_EMOJIS_MAP[self.char]
        if self.n < len(_emoji.emojis):
            self.emoji = discord.PartialEmoji(name=_emoji.emojis[self.n])
            return
        async with aiofiles.open(f"emojis/{_emoji.file}", "rb") as f:
            num = self.n - len(_emoji.emojis)
            self.emoji: discord.Emoji = await self._ctx.guild.create_custom_emoji(
                name=f"reactor_{_emoji.char}_{num}",
                image=await f.read(),
            )
        print(f"Emoji '{self.emoji.name}' is ready")

    async def react(self, wait_for_it: t.Optional[t.Awaitable], message):
        """React to the message"""
        await asyncio.wait_for(self.prepare_coro, timeout=None)
        if wait_for_it is not None:
            await asyncio.wait_for(wait_for_it, timeout=None)
        await message.add_reaction(self.emoji)
        print(f"Reacted with '{self.emoji.name}'")
        asyncio.create_task(self.remove())

    async def remove(self):
        """Remove emoji from guild if it is custom"""
        if isinstance(self.emoji, discord.Emoji):
            await self.emoji.delete(reason="We won't need this anymore")
            print(f"Custom emoji '{self.emoji.name}' removed")


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

    counter_dict = defaultdict(int)
    last_reaction = None

    for char in text:
        reaction = Reaction(ctx, char, counter_dict[char])
        counter_dict[char] += 1
        last_reaction = asyncio.create_task(reaction.react(last_reaction, message))

    await ctx.send(content=f"Cleaned up your text and reacted with: ```{text}```", hidden=True)
