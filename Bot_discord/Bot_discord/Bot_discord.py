import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


# '😊'
# '🥳'
class HuTaoBot(discord.Client):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())

        self.target_message_id = 0
        self.emoji_to_role = {
            discord.PartialEmoji(name='😊'): 897153295150374992,
            discord.PartialEmoji(name='🥳'): 897153343644893236,
        }

    async def on_ready(self):
        print(f"{self.user.display_name} is ready !")

    @staticmethod
    async def ping_pong(message):
        await message.channel.send("pong")

    async def initialisation(self, message):
        message = await message.channel.send(
            "React to this message to get the corresponding roles :\n😊 : bla\n🥳 : blo")
        self.target_message_id = message.id

    async def on_message(self, message):
        if message.content.lower() == "ping":
            await self.ping_pong(message)
        if message.content.lower() == "init":
            await self.initialisation(message)

    async def on_raw_reaction_add(self, payload):
        """Gives a role based on reacted emoji"""
        message_id = payload.message_id
        if message_id == self.target_message_id:
            member = payload.member
            guild = member.guild

            try:
                role_id = self.emoji_to_role[payload.emoji]
            except KeyError:
                # the reacted emoji isn't on the list
                return

            role = guild.get_role(role_id)
            await member.add_roles(role)


bot = HuTaoBot()
load_dotenv(dotenv_path="config")

bot.run(os.getenv("TOKEN"))
