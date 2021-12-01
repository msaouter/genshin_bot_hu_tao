from discord.ext import commands
import MyHelp


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # self._original_help_command = bot.help_command
        # bot.help_command = MyHelp()
        # bot.help_command.cog = self

    def checking(ctx):
        return ctx.message.channel.id == 897121894568972298

    @commands.command()
    @commands.check(checking) #predicat qui regarde si on est dans le channel answer
    async def coucou(self, ctx):
        await ctx.send("coucou")

    # def cog_unload(self):
    #     self.bot.help_command = self._original_help_command
