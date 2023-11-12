import yt_dlp as youtube_dl
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import certifi
import os
import asyncio
import random


from new_api import api

os.chmod('venv/lib/python3.11/site-packages/ffmpeg', 0o755)

os.environ["SSL_CERT_FILE"] = certifi.where()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

queue = []


ffmpeg_options = {
}

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }],
    'source_address': '0.0.0.0',
}

# Функция для воспроизведения музыки
async def play(ctx, url):
    try:
        with youtube_dl.YoutubeDL({**ydl_opts, **ffmpeg_options}) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            voice_channel = ctx.author.voice.channel
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name=voice_channel.name)
            voice_channel = await voice_channel.connect()
            voice_channel.play(FFmpegPCMAudio(url2, executable="/Users/dima/ffmpeg"))
            while voice_channel.is_playing():
                await asyncio.sleep(1)
            await voice_channel.disconnect()
    except youtube_dl.DownloadError as e:
        print(e)
        await ctx.send(f'Произошла ошибка при обработке видео: {e}')

# Команда для включения песни
@bot.command(name="играй")
async def play_command(ctx, *, url: str = None):
    try:
        if url is None:
            # Если нет аргумента, играть рандомную песню
            url = "ссылка на рандомную песню"
        await play(ctx, url)
    except Exception as e:
        print(e)
        await ctx.send(f'Произошла ошибка при добавлении песни: {e}')

# Команда для постановки на паузу
@bot.command(name="пауза")
async def pause_command(ctx):
    try:
        pass  # Здесь добавьте логику для постановки на паузу
    except Exception as e:
        print(e)
        await ctx.send(f'Произошла ошибка при постановке на паузу: {e}')

# Обработчик события запуска бота
@bot.event
async def on_ready():
    print(f'Бот подключен к Discord как {bot.user.name}')
    print(f'Список команд: {", ".join([command.name for command in bot.commands])}')
    activity = discord.Game(name="!помощь для списка команд")
    await bot.change_presence(activity=activity)

# Запуск бота
bot.run(api)
