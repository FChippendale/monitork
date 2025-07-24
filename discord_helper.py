from typing import Sequence
import discord
from discord.guild import Guild
from discord.channel import TextChannel
import string
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

from data_helper import get_download_link, read_json, File

DOTENV = os.path.join(os.path.dirname(__file__), ".env")
SERVER_NAME = "Dev Server"
CHANNEL_NAME = "general"


client = discord.Client(intents=discord.Intents.default())


class Settings(BaseSettings):
    token: str
    model_config = SettingsConfigDict(env_file=DOTENV)


def _clean_channel_name(name: str) -> str:
    printable = set(string.printable)
    clean_name = "".join(filter(lambda x: x in printable, name))
    return clean_name


def _get_target_guild(guilds: Sequence[Guild]) -> Guild:
    for guild in guilds:
        if guild.name == SERVER_NAME:
            return guild

    raise Exception("Could not find Try Hard Guild")


def _get_target_channel(channels: Sequence[TextChannel]) -> TextChannel:
    for channel in channels:
        if _clean_channel_name(channel.name) == CHANNEL_NAME:
            return channel

    raise Exception("Could not find channel")


def _get_channel() -> TextChannel:
    guild = _get_target_guild(client.guilds)
    guild_channel = _get_target_channel(guild.text_channels)
    channel = guild.get_channel(guild_channel.id)
    assert isinstance(channel, TextChannel)
    return channel


async def send_message(msg: str) -> None:
    channel = _get_channel()
    await channel.send(msg)


@client.event
async def on_ready():
    print("Started on_ready")

    try:
        diff = read_json(File.UPDATED_RESULTS)
        for result in diff:
            msg = f"{result.title} (updated {result.last_updated}): {get_download_link(result.file)}"
            await send_message(msg)
    finally:
        print("Finished on_ready")
        await client.close()


def post_updates():
    settings = Settings()
    client.run(settings.token)
    
