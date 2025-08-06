from typing import Sequence
import discord
from discord.guild import Guild
from discord.channel import TextChannel
import string


client = discord.Client(intents=discord.Intents.default())


# <Server Name>: <Target Bot Channel Name>
CONFIGURED_SERVERS: dict[str, str] = {
    "Dev Server": "general",
    "Try Hard Wargaming": "warcomm-update-f5",
    "Battle Barn": "warcomm-updates",
}


def _clean_channel_name(name: str) -> str:
    printable = set(string.printable)
    clean_name = "".join(filter(lambda x: x in printable, name))
    return clean_name


def _get_target_guilds(guilds: Sequence[Guild]) -> list[Guild]:
    return [guild for guild in guilds if guild.name in CONFIGURED_SERVERS]


def _get_target_channel(guild: Guild) -> TextChannel | None:
    for channel in guild.text_channels:
        if _clean_channel_name(channel.name) == CONFIGURED_SERVERS[guild.name]:
            return channel

    print(
        f"Could not find channel '{CONFIGURED_SERVERS[guild.name]}' on server '{guild.name}'"
    )
    return None


def _get_channels() -> list[TextChannel]:
    guilds = _get_target_guilds(client.guilds)

    target_channels: list[TextChannel] = []

    for guild in guilds:
        channel = _get_target_channel(guild)
        if channel is None:
            continue

        target_channels.append(channel)

    return target_channels


async def send_message(msg: str) -> None:
    channels = _get_channels()
    for channel in channels:
        try:
            await channel.send(msg)
        except Exception as e:
            print(
                f"Failed to send message to channel {channel.name} on {channel.guild.name}"
            )
            print(e)


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
