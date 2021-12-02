from discord.ext import commands
import MyHelpCommand


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        help_command = MyHelpCommand.MyHelpCommand()
        help_command.cog = self  # Instance of YourCog class
        bot.help_command = help_command

    def checking_answer(ctx):
        return ctx.message.channel.id == 897121894568972298

    def checking_role(ctx):
        return ctx.message.channel.id == 897155104426307614

    @commands.command(name="hutao")
    @commands.check(checking_answer)
    async def ping_pong(self, ctx):
        """ When calling her name, the bot answer
        Used for debug or to check if the bot is responding
         """
        await ctx.send("I am here !")

    @commands.command(name="init")
    @commands.check(checking_role)
    async def initialisation(self, ctx):
        """ Send init in the chat to let the bot post the reaction role message
        Can only be called one time
        """
        # check if the init have already been done
        if self.bot.init_flag:
            await self.bot.get_channel(self.bot.channel_answer).send("Initialisation have already been done, check ancient "
                                                        "messages !")
            return
        message = await self.bot.get_channel(self.bot.role_channel_id).send(
            "React to this message to get the corresponding roles :\n😊 : bla\n🥳 : blo")
        self.bot.target_message_id = message.id
        # list all the emojis to add them on the reaction messages
        for e in self.bot.emoji_to_role:
            await message.add_reaction(e)
        self.bot.init_flag = True
        print("Initialization done !")

    @initialisation.error
    async def initialisation_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You can't call this command outside the initialisation channel")

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

