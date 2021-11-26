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
            # ADD YOUR EMOJIS HERE
            # format : emoji to be detected by the bot (can be personalized one), id of the role it give
            discord.PartialEmoji(name='😊'): 897153295150374992,
            discord.PartialEmoji(name='🥳'): 897153343644893236,
        }
        self.init_flag = False

    async def on_ready(self):
        """ Function called when the bot is ready to answer command, print in console when it's ready to answer"""
        print(f"{self.user.display_name} is ready !")

    @staticmethod
    async def ping_pong(message):
        """ When calling her name, the bot answer
        Used for debug or to check if the bot is responding"""
        await message.channel.send("I am here !")

    @staticmethod
    async def easter_egg(message):
        """ When calling her name, the bot answer
        Used for debug or to check if the bot is responding"""
        await message.channel.send("I know da way 😉")

    async def initialisation(self, message):
        """ Send init in the chat to let the bot post the reaction role message
        Only needs to be called once """
        # check if the init have already been done
        if self.init_flag:
            await message.channel.send("Initialisation have already been done, check ancient messages !")
            return
        message = await message.channel.send(
            "React to this message to get the corresponding roles :\n😊 : bla\n🥳 : blo")
        self.target_message_id = message.id
        # list all the emojis to add them on the reaction messages
        for e in self.emoji_to_role:
            await message.add_reaction(e)
        self.init_flag = True
        print("Initialization done !")

    async def on_message(self, message):
        """ Function to read messages sent by users, used to see if a command has been invoked """
        if message.content.lower() == "hu tao ?":
            await self.ping_pong(message)
        if message.content.lower() == "init":
            await self.initialisation(message)
        if message.content.lower() == "do you know da way ?":
            await self.easter_egg(message)

    async def on_raw_reaction_add(self, payload):
        """Gives a role to a member based on reacted emoji"""
        if payload.user_id == self.user.id:
            # if this is the bot that is reacting, do not add it a role
            return

        message_id = payload.message_id
        if message_id == self.target_message_id:
            # the id of the message the member reacted to is the same as the message registered
            member = payload.member
            guild = member.guild

            try:
                # retrieve the role based on the reacted emoji
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
            # the id of the message the member reacted to is the same as the message registered
            member_id = payload.user_id
            guild = guild = self.get_guild(payload.guild_id)

            try:
                # retrieve the role based on the reacted emoji
                role_id = self.emoji_to_role[payload.emoji]
            except KeyError:
                # the reacted emoji isn't on the list
                return
            role = guild.get_role(role_id)
            member = guild.get_member(member_id)

            if member is None:
                # member isn't in the server anymore
                return

            await member.remove_roles(role)


bot = HuTaoBot()

# the following line is used to retrieve the token needed to run the bot and the channel in which the bot is allowed
# to speak
load_dotenv(dotenv_path="config")

bot.run(os.getenv("TOKEN"))
