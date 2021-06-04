"""
    Coisas a instalar na consola:
        pip install discord.py
        pip install -U discord.py[voice]
        pip install youtube_dl
        pip install mutagen
        git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
        https://www.youtube.com/watch?v=ObuBysxtv9M
"""
import time
from asyncio.tasks import sleep
import discord
import youtube_dl
import os
from mutagen.mp3 import MP3

client = discord.Client()

# Variaveis globais
guild = None  # Uma guild é o termo usado para referir um server

nomeRolesEId = {"forex basico": 847597237902770176, "forex intermedio": 847597424238264321,
                "forex avançado": 847597503988891648, "dcx": 847597583962210315, "kevin": 847597584667246603,
                "hfx": 847599509533884517, "desenvolvimento pessoal": 847608372739178496}  # Id dos Roles no server


@client.event
async def on_ready():  # Assim que o bot liga corre isto
    print("Sou um bot que se tornou ativo. Sentience here I go!")
    global guild
    guild = client.get_guild(847523022574845953)  # Id do server
    voiceChannel = discord.utils.get(guild.voice_channels, name='your-wish-is-your-command')
    await voiceChannel.connect()
    downloadVideos("https://youtube.com/playlist?list=PL80GxExWEfBVqOM572QB-ge-oueS_S7UV")
    while True:
        await play()


@client.event
async def on_message(message):  # Comandos que um user pode invocar
    if message.author == client.user:
        return  # A mensagem veio do bot
    if message.content.upper().startswith(":RANK"):
        await giveRankCMD(message)


async def giveRankCMD(message):
    autorMensagem = message.author
    if message.content[9::].strip() in nomeRolesEId:
        roleAAtribuir = guild.get_role(nomeRolesEId.get(
            message.content[9::].strip()))  # Role no server
        if roleAAtribuir not in autorMensagem.roles:
            await autorMensagem.add_roles(roleAAtribuir)
            out = "Role adicionado com sucesso."
        else:
            out = "O user já tem este role."
    else:
        out = "O role não foi encontrado. Verifique se o escreveu direito."
    await message.channel.send(out)


async def play():
    voice = discord.utils.get(client.voice_clients, guild=guild)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            voice.play(discord.FFmpegPCMAudio(file))
            time.sleep(MP3(file).info.length + 0.5)


def downloadVideos(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    client.run("ODQ5OTIwNDAzOTI0ODQ0NTY1.YLiMDw.dC2vXViWJbvmSFdhdX2brzdDnvM")