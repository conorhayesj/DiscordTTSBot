import os
import time
import asyncio

from gtts import gTTS

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='^')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected!')

@bot.command(name='tts')
async def speech(ctx, *, ttstext):
    try:
        voice_channel = ctx.author.voice.channel
    except AttributeError:
        await ctx.channel.send("You need to be in a voice channel to use me.")
        return
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client

    print(f'Name: {ctx.author.name} - Nick: {ctx.author.nick}')
    if ctx.author.nick == 'Taz' or ctx.author.name == 'Nan':
        vc.play(discord.FFmpegPCMAudio(source='./other_sounds/taz.mp3'))
    else:
        mytts = gTTS(text=ttstext, lang='en', slow=False)
        mytts.save('tts.mp3')
        vc.play(discord.FFmpegPCMAudio(source='./tts.mp3'))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    if os.path.isfile('./tts.mp3'):
        os.remove('./tts.mp3')

@bot.command(name='stop')
async def leave(ctx):
    try:
        await ctx.voice_client.disconnect()
    except AttributeError:
        pass

bot.run(TOKEN)
