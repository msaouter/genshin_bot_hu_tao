import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


# '😊'
# '🥳'
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

    def get_message_id(self):
        return self.target_message_id


class HuTaoClient(discord.Client):
    def __init__(self, hutaobot, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot = hutaobot
        self.message_id = bot.get_message_id()
        self.emoji_to_role = {
            discord.PartialEmoji(name='😊'): 0,
            discord.PartialEmoji(name='🥳'): 0,
        }

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on reacted emoji"""
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)

        if guild is None:
            print("guild none")
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # the emoji isn't the one we care about -> exit
            print("don't care about this emoji")
            return

        role = guild.get_role(role_id)
        if role is None:
            # make sure the role still exists
            print("role doesn't exist")
            return

        try:
            await payload.member.add_roles(role)
        except discord.HTTPException:
            print("can't do anything for ya")
            return
        print(payload.member.role)


bot = HuTaoBot()
client = HuTaoClient(bot)
load_dotenv(dotenv_path="config")

bot.run(os.getenv("TOKEN"))
