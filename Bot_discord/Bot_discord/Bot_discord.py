import discord
from discord.ext import commands

#create a bot that will execute it's command when we enter ![command_name]
bot = commands.Bot(command_prefix = "!", description = "Genshin bot")

#verifiy if the bot is ready to be executed
@bot.event
async def on_ready():
    print("Ready")

@bot.command()
async def coucou(ctx):
    print("coucou")
    await ctx.send("Coucou !") #await sert à attendre que le bot se connecte à discord (coroutine)

@bot.command()
async def serverInfo(ctx):
    server = ctx.guild # guild = serveur
    numberOfTxtChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes. \nLa description du serveur : {serverDescription}. \nCe serveur possède *{numberOfTxtChannels}* salons écrits et *{numberOfVoiceChannels}* salons vocaux."
    await ctx.send(message)

#run the bot
bot.run("ODk3MTI0Njk1MTg5NjQ3NDEw.YWRGew.LZT2eCCrMzMRA4X5p9LKa1nKCSA")
