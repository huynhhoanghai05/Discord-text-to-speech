from gtts import gTTS

import os
import random
import secrets
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!xu',activity=discord.Activity(type=discord.ActivityType.listening,name="Thay lời muốn nói <3"))
language = 'vi'
voice_client, channel = None, None

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="oi")
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
            response = [
            "Mày chưa vào kênh thoại mà dám gọi tao à? Ăn đấm không??",
            "Vào kênh thoại đi mài!!",
            "Bạn yêu vào kênh thoại đi rồi mình hú hí :3"
            ]
            await ctx.send(random.choice(response))

    vc = ctx.voice_client

    if vc:
        if vc.channel.id == channel.id:
            return
        try:
            await vc.move_to(channel)
        except TimeoutError:
            raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
    else:
        try:
            await channel.connect()
        except TimeoutError:
            raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

    await ctx.send(f'Chị vào với mấy cưng đây **{channel}**')

@bot.command(name="ka")
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
        await ctx.send(f"Hey {ctx.author.mention}, mày bị khùng à")
        return

    vc = ctx.voice_client # We use it more then once, so make it an easy variable
    if not vc:
        # We are not currently in a voice channel
        await ctx.send(f"Cho mày vài đấm bây giờ {ctx.author.mention}")
        return

    # Lets prepare our text, and then save the audio file
    tts = gTTS(text=text, lang="vi")
    tts.save("text.mp3")

    try:
        # Lets play that mp3 file in the voice channel
        vc.play(discord.FFmpegPCMAudio(executable="D:/ffmpeg/bin/ffmpeg.exe",source = 'text.mp3'), after=lambda e: print(f"Finished playing: {e}"))

        # Lets set the volume to 1
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1

    # Handle the exceptions that can occur
    except Exception as e:
        await ctx.send(f"Lỗi rồi: \n`{e}`")
    except TypeError as e:
        await ctx.send(f"Lỗi rồi: \n`{e}`")
    # except OpusNotLoaded as e:
    #     await ctx.send(f"OpusNotLoaded exception: \n`{e}`")

@bot.command("bye")
async def disconnect(ctx):
    """
    Disconnect from a voice channel, if in one
    """
    vc = ctx.voice_client

    if not vc:
        await ctx.send("Chưa vào đã đuổi ??")
        return

    await vc.disconnect()
    await ctx.send("Chị của mấy đứa đi nhá !")

bot.run(secrets.TOKEN)