from gtts import gTTS

import os
import random
import secrets
import discord
from discord.ext import commands

client = discord.Client(activity=discord.Activity(type=discord.ActivityType.listening,name="Thay lời muốn nói <3"))
language = 'vi'
voice_client, channel = None, None

@client.event
async def on_ready():
    print('Connected as')
    print(client.user.name)
    print('id: {}'.format(client.user.id))
    print('------')

@client.event
async def on_message(message):

    # display logs
    print(message)
    print(f"message: {message.content}")

    # allow voice client to be used across different commands
    global voice_client, channel

    # check bot
    if message.author == client.user:
        return

    # check command
    split_msg = message.content.split()
    if len(split_msg) >= 2 and split_msg[0] == 'tts':

        # check voice channel
        if voice_client:
            if channel != voice_client.channel:
                await voice_client.disconnect()

        try:
            channel = message.author.voice.channel
        except AttributeError:
            response = [
            "Mày chưa vào kênh thoại mà dám gọi tao à? Ăn đấm không??",
            "Vào kênh thoại đi mài!!",
            "Bạn yêu vào kênh thoại đi rồi mình hú hí :3"
            ]
            await message.channel.send(random.choice(response))
            print(f"response: {response}")

        # create text to speech
        tts = gTTS(text=" ".join(split_msg[1:]), lang=language, slow=False)
        tts.save('tts.mp3')


        try:
            voice_client = await channel.connect(reconnect=False)
            audio_source = await discord.FFmpegPCMAudio('tts.mp3')
            if not voice_client.is_playing():
                voice_client.play(audio_source,after=None)
            else:
                response = "Đừng chặn họng chị !!"
                await message.channel.send(response)
                print(f"response: {response}")
        except Exception as e:
            print(e)

        # disconnect voice when bot is finished speaking

    elif message.content == 'raise-exception':
        raise discord.DiscordException


client.run(secrets.TOKEN)

