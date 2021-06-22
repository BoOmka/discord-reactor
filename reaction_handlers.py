import discord


async def remove_self_reaction(
        message: discord.Message,
        emoji: discord.Emoji,
        self_user: discord.User,
) -> None:
    await message.remove_reaction(emoji, self_user)
