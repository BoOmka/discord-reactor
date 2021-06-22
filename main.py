import logging
import os

import discord.ext
import discord_slash
from discord_slash.utils.manage_commands import create_option

import config
import handlers
import reaction_handlers

logging.basicConfig()
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(config.LOG_LEVEL)

intents = discord.Intents.all()
bot = discord.ext.commands.Bot(command_prefix='/', intents=discord.Intents.all())
slash = discord_slash.SlashCommand(bot, sync_commands=True)


@slash.slash(
    name='react',
    description='React to a message',
    options=[
        create_option(
            name="text",
            description="Text to print with reactions (max 20 characters)",
            option_type=discord_slash.SlashCommandOptionType.STRING,
            required=True
        ),
        create_option(
            name="message_id_or_url",
            description="ID or URL of message to react. If not provided, react to last message in the channel",
            option_type=discord_slash.SlashCommandOptionType.STRING,
            required=False
        )
    ],
)
async def react(ctx: discord_slash.SlashContext, text: str, message_id_or_url: str = None) -> None:
    return await handlers.react(ctx=ctx, text=text, message_id_or_url=message_id_or_url)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if (self_user := bot.user).id != payload.user_id:
        message = bot.get_channel(payload.channel_id).get_partial_message(payload.message_id)
        return await reaction_handlers.remove_self_reaction(message, payload.emoji, self_user)


@bot.event
async def on_connect():
    _LOGGER.info(f"Bot {bot.user} connected!")


def main():
    token = os.environ.get('DISCORD_TOKEN')
    if not token:
        raise ValueError('Must provide DISCORD_TOKEN env')
    bot.run(token)


if __name__ == '__main__':
    main()
