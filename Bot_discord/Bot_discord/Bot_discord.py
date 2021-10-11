import discord
from discord.ext import commands

#create a bot that will execute it's command when we enter ![command_name]
bot = commands.Bot(command_prefix = "!", description = "Genshin bot")

#verifiy if the bot is ready to be executed
@bot.event
async def on_ready():
    print("Ready")

#run the bot
bot.run("ODk3MTI0Njk1MTg5NjQ3NDEw.YWRGew.LZT2eCCrMzMRA4X5p9LKa1nKCSA")
