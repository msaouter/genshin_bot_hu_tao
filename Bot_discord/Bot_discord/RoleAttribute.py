from discord.ext import commands
import HuTaoHelpCommand


class RoleAttribute(commands.Cog, name="Hu Tao commands"):
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

    def checking_answer(self, ctx):
        """ Check if the current channel is the same as the one specified in the config file for answering commands
        """
        return ctx.message.channel.id == self.bot.answer_channel_id

    def checking_role(self, ctx):
        """ Check if the current channel is the same as the one specified in the config file to post the reaction
        role message
        """
        return ctx.message.channel.id == self.bot.role_channel_id

    async def check_last_message(self, ctx):
        channel = self.bot.get_channel(self.bot.role_channel_id)

        messages = [message async for message in channel.history(limit=2)]

        message = messages[1]

        if message.author.id == self.bot.user.id:
            self.bot.target_message_id = message.id
        else:
            self.bot.target_message_id = None

    @commands.command(name="hutao")
    async def ping_pong(self, ctx):
        """ When calling her name, the bot answer
        Mostly used for debug or to check if the bot is responding
         """
        if self.checking_answer(ctx):
            await ctx.send("Henlo~ ! 👋")

    @commands.command(name="init")
    async def initialisation(self, ctx):
        """ Initialise the reaction role message.
        Can only be called one time and if the channel id is equal to CHANNEL_ROLE
        """
        if not self.checking_role(ctx):
            await self.initialisation_error(ctx)
            return

        # check if the init have already been done, if not -> error
        if self.bot.init_flag:
            await ctx.message.delete()
            await self.bot.get_channel(self.bot.answer_channel_id).send(
                "Initialisation have already been done, check ancient "
                "messages ! " + ctx.message.author.mention, delete_after=5)
            return

        # check if the bot have already been run and initialized previously
        await self.check_last_message(ctx)

        if self.bot.target_message_id is not None:
            self.bot.init_flag = True
            await ctx.message.delete()
            print("Last role reaction message have been fetched")
            return

        else:
            message = await self.bot.get_channel(self.bot.role_channel_id).send(
                "React to this message to get the corresponding roles :\n🗡️ Rappel genshin\n"
                "🎮 Rappel Epic Games\n👑 Rappel Twitch Prime")
            self.bot.target_message_id = message.id
            # list all the emojis to add them on the reaction messages
            for e in self.bot.emoji_to_role:
                await message.add_reaction(e)

            await ctx.message.delete()
            self.bot.init_flag = True
            print("Initialization done")

    @commands.command(name="repeat")
    async def write_message(self, ctx, *, message):
        """
        Rewrite the same message entered in the current channel
        Deletes the command message
        """
        if self.checking_answer(ctx):
            await ctx.message.delete()
            await ctx.send(f"{message}")

    @staticmethod
    async def initialisation_error(ctx):
        """ Called if the initialisation have been called in the wrong channel """
        await ctx.message.delete()
        await ctx.send("You can't call this command outside the initialisation channel", delete_after=5)
