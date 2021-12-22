import discord
from discord.ext import commands
from discord.ext import tasks
import json
import datetime
import asyncio
import HuTaoHelpCommand

#### BIRTHDAYS ####
""" 
- Store every birthday in a file
- let people add their birthday to the file via discord command
- let people remove their birthday from the file via discord command
- bot send a message at 9am telling today's birthdays 
"""


class RoleAttribute(commands.Cog, name="Birthday commands"):
    def __init__(self, bot):
        self.bot = bot

        help_command = HuTaoHelpCommand.HuTaoHelpCommand()
        bot.help_command = help_command

    @commands.has_permissions(mention_everyone=True)
    @tasks.loop(hours=86400)
    async def check_for_birthdays(self):
        await self.bot.wait_until_ready()
        now = datetime.datetime.now()
        current_month = now.month
        current_day = now.day

        with open('birthdays.json', 'r') as f:
            var = json.load(f)
            for member in var:
                if member['month'] == current_month:
                    if member['day'] == current_day:
                        await self.bot.get_channel(self.bot.birthday_channel_id).send(
                            f"Happy birthday to <@{member}>!")


    def checking_answer(ctx):
        """ Check if the current channel is the same as the one specified in the config file for answering birthday
        commands
        """
        return ctx.message.channel.id == 897121894568972298
    @commands.command(name="setbirthday")
    @commands.check(checking_answer)
    async def setbirthday(ctx, self):
        '''Set a birthday.'''
        member = ctx.message.author.id
        await ctx.send("What is your birthday? Please use MM/DD format.")

        def check(user):
            return user == ctx.message.author and user == ctx.message.channel

        msg = await self.bot.wait_for('message', check=check)
        try:
            birth_date = msg.split("/")
            if birth_date[0] > 13 or birth_date[0] < 1:
                await ctx.send("Invalid date.")
                await ctx.send("Aborting...")
                return
            else:
                pass

            if birth_date[0] in (1, 3, 5, 7, 8, 10, 12):
                if birth_date[1] > 31 or birth_date[1] < 1:
                    await ctx.send("Invalid date.")
                    await ctx.send("Aborting...")
                    return
                else:
                    pass
            elif birth_date[0] in (4, 6, 9, 11):
                if birth_date[1] > 30 or birth_date[1] < 1:
                    await ctx.send("Invalid date.")
                    await ctx.send("Aborting...")
                    return
                else:
                    pass
            elif birth_date[0] == 2:
                if birth_date[1] > 29 or birth_date[1] < 1:
                    await ctx.send("Invalid date.")
                    await ctx.send("Aborting...")
                    return
                else:
                    pass
            else:
                await ctx.send("Invalid date.")
                await ctx.send("Aborting...")
                return
        except:
            await ctx.send("Invalid date.")
            await ctx.send("Aborting...")
            return

        birth_date = msg.split("/")
        month = birth_date[0]
        day = birth_date[1]

        with open('./birthdays.json', 'r+') as f:
            var = json.load(f)
            var[member] = {'month': month, 'day': day}
            json.dump(var, f, indent=4)
