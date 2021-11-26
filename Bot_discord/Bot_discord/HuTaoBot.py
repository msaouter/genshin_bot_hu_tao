import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


class HuTaoBot(discord.Client):
    """ This class is the core of the bot, every command of the bot is written in this class
    """

    def __init__(self):
        super().__init__(intents=discord.Intents.all())

        self.target_message_id = 0  # id of the message that can be reacted to add/remove role
        self.emoji_to_role = {  # dictionary of the emoji you can use to store it
            # format of the lines : emoji to be detected by the bot (can be personalized one), id of the role it give
            discord.PartialEmoji(name='😊'): 897153295150374992,
            discord.PartialEmoji(name='🥳'): 897153343644893236,
        }

    async def on_ready(self):
        """ Function called when the bot is ready to answer command, print in console when it's ready to answer"""
        print(f"{self.user.display_name} is ready !")

    @staticmethod
    async def ping_pong(message):
        """ When sending ping, the bot answer pong
        Used for debug or to check if the bot is responding"""
        await message.channel.send("pong")

    async def initialisation(self, message):
        """ Send init in the chat to let the bot post the reaction role message
        Only needs to be called once """
        message = await message.channel.send(
            "React to this message to get the corresponding roles :\n😊 : bla\n🥳 : blo")
        self.target_message_id = message.id

    async def on_message(self, message):
        """ Function to read messages sent by users, used to see if a command has been invoked """
        if message.content.lower() == "ping":
            await self.ping_pong(message)
        if message.content.lower() == "init":
            await self.initialisation(message)

    async def on_raw_reaction_add(self, payload):
        """Gives a role to a member based on reacted emoji"""
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

    async def on_raw_reaction_remove(self, payload):
        """ Remove the role when the member unreact to the corresponding emoji"""
        message_id = payload.message_id
        if message_id == self.target_message_id:
            member_id = payload.user_id
            guild = guild = self.get_guild(payload.guild_id)

            try:
                role_id = self.emoji_to_role[payload.emoji]
            except KeyError:
                # the reacted emoji isn't on the list
                return
            role = guild.get_role(role_id)
            member = guild.get_member(member_id)

            if member is None:
                return

            await member.remove_roles(role)


bot = HuTaoBot()

# the following line is used to retrieve the token needed to run the bot and the channel in which the bot is allowed
# to speak
load_dotenv(dotenv_path="config")

bot.run(os.getenv("TOKEN"))
