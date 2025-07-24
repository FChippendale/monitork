from typing import Sequence
import discord
from discord.guild import Guild
from discord.channel import TextChannel
import string


SERVER_NAME = "Dev Server"
CHANNEL_NAME = "general"


client = discord.Client(intents=discord.Intents.default())


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
    global update_messages

    try:
        for msg in update_messages:
            await send_message(msg)
    finally:
        print("Finished on_ready")
        await client.close()


def post_updates(msgs: list[str], token: str):
    global update_messages
    update_messages = msgs

    client.run(token)
