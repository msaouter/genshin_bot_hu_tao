import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


class HuTaoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        self.target_message_id = 0

    async def on_ready(self):
        print(f"{self.user.display_name} is ready !")

    @staticmethod
    async def ping_pong(message):
        await message.channel.send("pong")

    async def initialisation(self, message):
        await message.channel.send("React to this message to get the corresponding roles :\n😊 : bla\n🥳 : blo")
        self.target_message_id = discord.TextChannel.last_message_id

    async def on_message(self, message):
        if message.content.lower() == "ping":
            await self.ping_pong(message)
        if message.content.lower() == "init":
            await self.initialisation(message)


bot = HuTaoBot()
load_dotenv(dotenv_path="config")

bot.run(os.getenv("TOKEN"))
