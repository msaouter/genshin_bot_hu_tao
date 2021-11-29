"""
Hu Tao Discord Bot
~~~~~~~~~~~~~~~~~~

A Genshin Impact bot that can :
* send notifications if genshin official social network are posting something -> TODO
* send reminder for the hoyolab connexion, the epic game store free game & birthdays
* give infos about the upcomming banners -> TODO
* assign roles on your discord

:copyright: (c) 2021-present Marion SAOUTER
:license: MIT, see LICENSE for more details.
"""

import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv


class HuTaoBot(discord.Client):
    """ This class is the core of the bot, every command of the bot is written in this class

    . . .

    Attributes
    ---------

    reminder_channel_id : int
        the id of the channel to post the reminder messages
    guild_id : int
        the id of the guild in which the bot is used
    genshin_role_id :
        the id of the role to ping people who have the role for genshin impact daily connection
    epicgames_role_id :
        the id of the role to ping people who have the role for epic games weekly reminder for free games
    role_channel_id : int
        the id of the channel to post the reaction role message
    target_message_id : int
        the id of the message to react to get a role
    emoji_to_role : dict
        the list of emojis associated to their role id to attribute a role while reacting to the reaction message
    init_flag : bool
        a flag to block the init once it has been done once

    Methods
    ------
    ping_pong(message)
        When calling her name, the bot answer. Used for debug or to check if the bot is responding
    easter_egg(message)
        When sending a special message, the bot answer with this easter egg
    initialisation(message)
        Send init in the chat to let the bot post the reaction role message. Can only be called one time.
    on_message(message)
        Function to read messages sent by users, used to see if a command has been invoked
    on_raw_reaction_add(payload)
        Gives a role to a member based on reacted emoji
    on_raw_reaction_remove(payload)
        Remove the role when the member unreact to the corresponding emoji
    genshin_reminder()
        Ping every people with the genshin role to remind them to connect to hoyolab
    epic_store_reminder()
        Ping every people with the epic games role to remind them to connect to epic games store to get their free
        game(s)
    help(message)
        Post a message with every command available
    on_ready()
        Function called when the bot is ready to answer command, print in console when it's ready to answer and
        start the reminders
    """

    def __init__(self, role_channel, reminder_channel, guild, genshin_role, epicgames_role):
        super().__init__(intents=discord.Intents.all())

        self.guild_id = guild
        self.reminder_channel_id = reminder_channel
        self.genshin_role_id = genshin_role
        self.epicgames_role_id = epicgames_role
        self.role_channel_id = role_channel
        self.target_message_id = 0  # id of the message that can be reacted to add/remove role
        self.emoji_to_role = {  # dictionary of the emoji you can use to store it
            # ADD YOUR EMOJIS HERE
            # format : emoji to be detected by the bot (can be personalized one), id of the role it give
            discord.PartialEmoji(name='😊'): 897153295150374992,
            discord.PartialEmoji(name='🥳'): 897153343644893236,
        }
        self.init_flag = False

    #### MESSAGES ####

    @staticmethod
    async def ping_pong(message):
        """ When calling her name, the bot answer
        Used for debug or to check if the bot is responding

        :param message: Message that have triggered this command of the bot
        :type message: discord.Message
         """
        await message.channel.send("I am here !")

    @staticmethod
    async def easter_egg(message):
        """ When sending a special message, the bot answer with this easter egg

        :param message: Message that have triggered this command of the bot
        :type message: discord.Message
        """
        await message.channel.send("I know da way 😉")

    async def initialisation(self, message):
        """ Send init in the chat to let the bot post the reaction role message
        Can only be called one time

        :param message: Message that have triggered this command of the bot
        :type message: discord.Message
        """
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
        """ Function to read messages sent by users, used to see if a command has been invoked

        :param message: The last message sent in the bot channel
        :type message: discord.Message
        """
        if message.content.lower() == "hu tao ?":
            await self.ping_pong(message)
        if message.content.lower() == "init":
            await self.initialisation(message)
        if message.content.lower() == "do you know da way ?":
            await self.easter_egg(message)
        if message.content.lower() == "help":
            await self.help(message)

    #### REACTION ROLE ####

    async def on_raw_reaction_add(self, payload):
        """Gives a role to a member based on reacted emoji

        :param payload: The raw event payload data
        :type payload: RawReactionActionEvent
        """
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
        """ Remove the role when the member unreact to the corresponding emoji

        :param payload: The raw event payload data
        :type payload: RawReactionActionEvent
        """
        message_id = payload.message_id
        if message_id == self.target_message_id:
            # the id of the message the member reacted to is the same as the message registered
            member_id = payload.user_id
            guild = self.get_guild(payload.guild_id)

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

    #### REMINDERS ####

    @tasks.loop(hours=24)
    async def genshin_reminder(self):
        """ Ping every people with the genshin role to remind them to connect to hoyolab
         """
        genshin_embed = discord.Embed(
            title='Genshin reminder',
            description="It's time for the hoyolab connection traveler's !",
            url="http://urlr.me/GDsvz",
            color=discord.Color.dark_blue()
        )
        mention = self.get_guild(self.guild_id).get_role(self.genshin_role_id).mention
        await self.get_channel(channel_remind).send(f"{mention}", embed=genshin_embed)

    @tasks.loop(hours=168)
    async def epic_store_reminder(self):
        """ Ping every people with the epic games role to remind them to connect to epic games store to get their
        free game(s)
        """
        epic_embed = discord.Embed(
            title='Epic games reminder',
            description="It's time to go get your free games on Epic Game store !",
            url="https://www.epicgames.com/store/fr/",
            color=discord.Color.gold()
        )
        mention = self.get_guild(self.guild_id).get_role(self.epicgames_role_id).mention
        await self.get_channel(channel_remind).send(f"{mention}", embed=epic_embed)

    #### HELP ####

    @staticmethod
    async def help(message):
        """ Post a message with every command available

        :param message: Message that have triggered this command of the bot
        :type message: discord.Message
        """
        help_embed = discord.Embed(
            title='Hu Tao - List of commands',
            color=discord.Color.dark_red()
        )

        help_embed.add_field(name='Init', value='Command to call to initialize the bot for reaction role', inline=False)
        help_embed.add_field(name='Help', value='Shows every command you can use', inline=False)
        help_embed.add_field(name='Hu Tao ?', value='Reply, used to check if the bot is ready to answer', inline=False)
        help_embed.add_field(name='Do you know da way ?', value='Small easter egg 😉', inline=False)
        await message.channel.send(embed=help_embed)

    #### ON READY ####
    async def on_ready(self):
        """ Function called when the bot is ready to answer command, print in console when it's ready to answer and
        start the reminders
        """
        print(f"{self.user.display_name} is ready !")
        self.genshin_reminder.start()
        self.epic_store_reminder.start()


# the following line is used to retrieve the token needed to run the bot and the channel in which the bot is allowed
# to speak
load_dotenv(dotenv_path="config")

# assign all config variables to a python variable
channel_role = int(os.getenv("CHANNEL_ROLE"))
channel_remind = int(os.getenv("CHANNEL_REMIND"))
guild = int(os.getenv("GUILD"))
genshin_role = int(os.getenv("GENSHIN_ROLE"))
epicgames_role = int(os.getenv("EPIC_GAMES_ROLE"))


bot = HuTaoBot(channel_role, channel_remind, guild, genshin_role, epicgames_role)
bot.run(os.getenv("TOKEN"))
