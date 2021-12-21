import discord
import datetime
from discord.ext import commands


class HelpEmbed(discord.Embed):  # Our embed with some preset attributes to avoid setting it multiple times
    """
    This class is an helper class for help presentation
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = datetime.datetime.utcnow()
        text = "Use help [command] or help [category] for more information"
        self.set_footer(text=text)
        self.color = discord.Color.dark_red()


class HuTaoHelpCommand(commands.HelpCommand):
    """
        This class is an override of the commands.HelpCommand to have personalized help commands.

        . . .

        Methods
        ------
        get_command_signature(command)
            Remove the command prefix when posting the command names
        send(**kwargs)
            A short cut to sending to get_destination
        send_bot_help(mapping)
            Triggers when a `<prefix>help` is called
        send_command_help(command)
            Triggers when a `<prefix>help <command>` is called
        send_help_embed(title, description, commands)
            A helper function to add commands to an embed
        send_group_help(group)
            Triggers when a `<prefix>help <group>` is called
        send_cog_help(cog)
            Triggers when a `<prefix>help <cog>` is called
        send_error_message(error)
            Triggers when the class fails to find a command/cog/group
        on_help_command_error(ctx, error)
            Triggers when any other error than command not found is happening
        """
    def get_command_signature(self, command):
        """ Remove the command prefix when posting the command names """
        return '%s %s' % (command.qualified_name, command.signature)

    async def send(self, **kwargs):
        """ A short cut to sending to get_destination """
        await self.get_destination().send(**kwargs)

    async def send_bot_help(self, mapping):
        """ Triggers when a `<prefix>help` is called """
        ctx = self.context
        embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
        embed.set_thumbnail(url=ctx.me.avatar_url)

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in commands]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Help commands")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        await self.send(embed=embed)

    async def send_command_help(self, command):
        """ Triggers when a `<prefix>help <command>` is called """
        signature = self.get_command_signature(command)
        embed = HelpEmbed(title=signature, description=command.help or "No help found...")
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        await self.send(embed=embed)

    async def send_help_embed(self, title, description, commands):
        """ A helper function to add commands to an embed """
        embed = HelpEmbed(title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")

        await self.send(embed=embed)

    async def send_group_help(self, group):
        """ Triggers when a `<prefix>help <group>` is called """
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """ Triggers when a `<prefix>help <cog>` is called """
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

    async def send_error_message(self, error):
        """ Triggers when the class fails to find a command/cog/group """
        embed = HelpEmbed(title="Error", description=str(error))
        await self.send(embed=embed)

    async def on_help_command_error(self, ctx, error):
        """ Triggers when any other error than command not found is happening """
        if isinstance(error, commands.BadArgument):
            print("hello")
            embed = HelpEmbed(title="Error", description=str(error))
            await self.send(embed=embed)
        else:
            raise error
