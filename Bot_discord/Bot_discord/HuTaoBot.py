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
import asyncio
import os
import discord
from discord.ext import tasks
from discord.ext import commands
import os

if not os.environ.get("PRODUCTION"):
    from dotenv import load_dotenv
from datetime import datetime
import RoleAttribute


class HuTaoBot(commands.Bot):
    """
    This class is the one that have all the non-callable methods (role attribution, reminders,...)

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
    on_raw_reaction_add(payload)
        Gives a role to a member based on reacted emoji
    on_raw_reaction_remove(payload)
        Remove the role when the member unreact to the corresponding emoji
    duration_calculation(local_time, start_date)
        Calculate the time duration of the sleep for each reminder
    genshin_reminder()
        Ping every people with the genshin role to remind them to connect to hoyolab
    before_genshin_reminder()
        Start the reminder any day at 8pm
    epic_store_reminder()
        Ping every people with the epic games role to remind them to connect to epic games store to get their free
        game(s)
    before_epic_reminder()
        Start the reminder on a thursday at 5pm
    on_ready()
        Function called when the bot is ready to answer command, print in console when it's ready to answer and
        start the reminders
    """

    def __init__(self, reminder_channel, genshin_role, epicgames_role, answer_channel, guild_id, role_channel,
                 birthday_channel):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

        self.reminder_channel_id = reminder_channel
        self.genshin_role_id = genshin_role
        self.epicgames_role_id = epicgames_role
        self.answer_channel_id = answer_channel
        self.birthday_channel_id = birthday_channel

        self.guild_id = guild_id
        self.role_channel_id = role_channel
        self.target_message_id = 0  # id of the message that can be reacted to add/remove role
        self.emoji_to_role = {  # dictionary of the emoji you can use to store it
            # ADD YOUR EMOJIS HERE
            # format : emoji to be detected by the bot (can be personalized one), id of the role it give
            discord.PartialEmoji(name='😊'): self.genshin_role_id,
            discord.PartialEmoji(name='🥳'): self.epicgames_role_id,
        }
        self.init_flag = False

    #### REACTION ROLE ####

    @commands.has_permissions(manage_roles=True)
    async def on_raw_reaction_add(self, payload):
        """
        Gives a role to a member based on reacted emoji

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

    @commands.has_permissions(manage_roles=True)
    async def on_raw_reaction_remove(self, payload):
        """
        Remove the role when the member unreact to the corresponding emoji

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

    @staticmethod
    def duration_calculation(local_time, start_date):
        """
        Calculate the time duration of the sleep for each reminder in seconds
        :return: duration : the duration time of the wait before the timer start
        """
        calculation_time = start_date - local_time
        day = abs(calculation_time.days)
        seconds = abs(calculation_time.seconds)  # seconds already have the minutes and hours added
        duration = (day * 86400) + seconds
        return duration

    @commands.has_permissions(mention_everyone=True)
    @tasks.loop(hours=24)
    async def genshin_reminder(self):
        """
        Ping every people with the genshin role to remind them to connect to hoyolab
        """
        genshin_embed = discord.Embed(
            title='Genshin reminder',
            description="It's time for the hoyolab connection travelers !",
            url="http://urlr.me/GDsvz",
            color=discord.Color.dark_blue()
        )
        genshin_embed.set_image(
            url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSK6nW9SP61_xGZVgecspo6vND_UDN38ZP69Q&usqp=CAU")
        mention = self.get_guild(self.guild_id).get_role(self.genshin_role_id).mention
        await self.get_channel(channel_remind).send(f"{mention}", embed=genshin_embed)

    @genshin_reminder.before_loop
    async def before_genshin_reminder(self):
        """
        Start the reminder any day at 8pm
        """
        local_time = datetime.now()
        # minus one hour for the time difference with the server
        start_date = datetime(year=local_time.year, month=local_time.month, day=local_time.day, hour=19)

        if local_time != start_date:
            duration = self.duration_calculation(local_time, start_date)
            print("Genshin impact : ", duration)
            await asyncio.sleep(duration)
        else:
            await self.wait_until_ready()

    @commands.has_permissions(mention_everyone=True)
    @tasks.loop(hours=168)
    async def epic_store_reminder(self):
        """
        Ping every people with the epic games role to remind them to connect to epic games store to get their
        free game(s)
        """
        epic_embed = discord.Embed(
            title='Epic games reminder',
            description="It's time to go get your free games on Epic Game store !",
            url="https://store.epicgames.com/fr/free-games",
            color=discord.Color.gold()
        )
        epic_embed.set_image(
            url="https://cdn2.unrealengine.com/Unreal+Engine%2Feg-logo-filled-1255x1272-0eb9d144a0f981d1cbaaa1eb957de7a3207b31bb.png")
        mention = self.get_guild(self.guild_id).get_role(self.epicgames_role_id).mention
        await self.get_channel(channel_remind).send(f"{mention}", embed=epic_embed)

    @epic_store_reminder.before_loop
    async def before_epic_reminder(self):
        """
        Start the reminder on a thursday at 5pm
        """
        local_time = datetime.now()
        weekday = local_time.weekday()
        day_to_add = 0
        if weekday == 0:  # Monday
            day_to_add = 3
        elif weekday == 1:  # Tuesday
            day_to_add = 2
        elif weekday == 2:  # Wednesday
            day_to_add = 1
        elif weekday == 3:  # Thursday TARGET DAY
            day_to_add = 0
        elif weekday == 4:  # Friday
            day_to_add = 6
        elif weekday == 5:  # Saturday
            day_to_add = 5
        elif weekday == 6:  # Sunday
            day_to_add = 4

        # minus one hour for the time difference with the server
        start_date = datetime(year=local_time.year, month=local_time.month, day=local_time.day + day_to_add, hour=16)
        duration = self.duration_calculation(local_time, start_date)
        print("Epic store : ", duration)
        await asyncio.sleep(duration)
        await self.wait_until_ready()

    #### ON READY ####
    async def on_ready(self):
        """ Function called when the bot is ready to answer command, print in console when it's ready to answer and
        start the reminders
        """
        print(f"{self.user.display_name} is ready !")
        self.genshin_reminder.start()
        self.epic_store_reminder.start()


# the following line is used to retrieve the variable needed to run the bot
if not os.environ.get("PRODUCTION"):
    load_dotenv(dotenv_path="config")

# assign all config variables to a python variable
channel_role = int(os.getenv("CHANNEL_ROLE"))
channel_remind = int(os.getenv("CHANNEL_REMIND"))
channel_answer = int(os.getenv("CHANNEL_ANSWER"))
channel_birthdays = int(os.getenv("CHANNEL_BIRTHDAYS"))
guild = int(os.getenv("GUILD"))
genshin_role = int(os.getenv("GENSHIN_ROLE"))
epicgames_role = int(os.getenv("EPIC_GAMES_ROLE"))

HuTao = HuTaoBot(reminder_channel=channel_remind, genshin_role=genshin_role, epicgames_role=epicgames_role,
                 answer_channel=channel_answer, guild_id=guild, role_channel=channel_role,
                 birthday_channel=channel_birthdays)
HuTao.add_cog(RoleAttribute.RoleAttribute(HuTao))

HuTao.run(os.getenv("TOKEN"))
