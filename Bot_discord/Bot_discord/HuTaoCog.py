from discord.ext import commands
import HuTaoHelpCommand


class HuTaoCog(commands.Cog, name="Hu Tao commands"):
    """
    This class is the class with every callable command registered for this bot (ping, init, ...)

    . . .
    Attributes
    ---------

    bot : commands.Bot
        the bot that will be running

    Methods
    ------
    checking_answer(ctx)
        Check if the current channel is the same as the one specified in the config file for answering commands
    checking_role(ctx)
        Check if the current channel is the same as the one specified in the config file to post the reaction
        role message
    ping_pong(message)
        When calling her name, the bot answer. Used for debug or to check if the bot is responding
    initialisation(message)
        Send init in the chat to let the bot post the reaction role message. Can only be called one time.
    initialisation_error(self, ctx, error)
        Called if the initialisation have been called in the wrong channel
    """
    def __init__(self, bot):
        self.bot = bot

        help_command = HuTaoHelpCommand.HuTaoHelpCommand()
        bot.help_command = help_command

    def checking_answer(ctx):
        """ Check if the current channel is the same as the one specified in the config file for answering commands
        """
        return ctx.message.channel.id == 897121894568972298

    def checking_role(ctx):
        """ Check if the current channel is the same as the one specified in the config file to post the reaction
        role message
        """
        return ctx.message.channel.id == 897155104426307614

    @commands.command(name="hutao")
    @commands.check(checking_answer)
    async def ping_pong(self, ctx):
        """ When calling her name, the bot answer
        Mostly used for debug or to check if the bot is responding
         """
        await ctx.send("I am here !")

    @commands.command(name="init")
    @commands.check(checking_role)
    async def initialisation(self, ctx):
        """ Initialise the reaction role message.
        Can only be called one time and if the channel id is equal to CHANNEL_ROLE
        """
        # check if the init have already been done, if not -> error
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
        """ Called if the initialisation have been called in the wrong channel """
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You can't call this command outside the initialisation channel")
