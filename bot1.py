import discord
import json
import asyncio
import yt_dlp
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True

bot = discord.Bot(intents=intents)

with open("config.json") as f:
    config = json.load(f)

guild_id = config["guild_id"]
voice_channel_id = config["voice_channel_id"]
playlist = config["mix"]

YDL_OPTIONS = {
    "format": "bestaudio",
    "quiet": True,
    "noplaylist": True
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

current_index = 0
voice_client = None


async def play_loop():
    global current_index, voice_client

    await bot.wait_until_ready()

    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(voice_channel_id)

    voice_client = await channel.connect()

    while True:
        url = playlist[current_index]

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]

        source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
        voice_client.play(source)

        while voice_client.is_playing():
            await asyncio.sleep(1)

        current_index = (current_index + 1) % len(playlist)


<@&1219705820275806220>.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    bot.loop.create_task(play_loop())


bot.run(os.getenv("DISCORD_TOKEN"))