from gtts import gTTS

import os
import random
import secrets
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!',activity=discord.Activity(type=discord.ActivityType.listening,name="Thay lời muốn nói <3"))
language = 'vi'
voice_client, channel = None, None

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def connect(ctx, *, channel: discord.VoiceChannel=None):
    """
    Connect to a voice channel
    This command also handles moving the bot to different channels.

    Params:
    - channel: discord.VoiceChannel [Optional]
        The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
        will be made.
    """
    if not channel:
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

    vc = ctx.voice_client

    if vc:
        if vc.channel.id == channel.id:
            return
        try:
            await vc.move_to(channel)
        except asyncio.TimeoutError:
            raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
    else:
        try:
            await channel.connect()
        except asyncio.TimeoutError:
            raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

    await ctx.send(f'Connected to: **{channel}**', delete_after=20)

@bot.command()
async def repeat(ctx, *, text=None):
    """
    A command which saves `text` into a speech file with
    gtts and then plays it back in the current voice channel.

    Params:
     - text [Optional]
        This will be the text we speak in the voice channel
    """
    if not text:
        # We have nothing to speak
        await ctx.send(f"Hey {ctx.author.mention}, I need to know what to say please.")
        return

    vc = ctx.voice_client # We use it more then once, so make it an easy variable
    if not vc:
        # We are not currently in a voice channel
        await ctx.send("I need to be in a voice channel to do this, please use the connect command.")
        return

    # Lets prepare our text, and then save the audio file
    tts = gTTS(text=text, lang="en")
    tts.save("text.mp3")

    try:
        # Lets play that mp3 file in the voice channel
        vc.play(discord.FFmpegPCMAudio('text.mp3'), after=lambda e: print(f"Finished playing: {e}"))

        # Lets set the volume to 1
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1

    # Handle the exceptions that can occur
    except ClientException as e:
        await ctx.send(f"A client exception occured:\n`{e}`")
    except TypeError as e:
        await ctx.send(f"TypeError exception:\n`{e}`")
    except OpusNotLoaded as e:
        await ctx.send(f"OpusNotLoaded exception: \n`{e}`")

@bot.command()
async def disconnect(ctx):
    """
    Disconnect from a voice channel, if in one
    """
    vc = ctx.voice_client

    if not vc:
        await ctx.send("I am not in a voice channel.")
        return

    await vc.disconnect()
    await ctx.send("I have left the voice channel!")

bot.run(secrets.TOKEN)