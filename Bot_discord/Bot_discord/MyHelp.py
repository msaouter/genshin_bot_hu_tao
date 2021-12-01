from discord.ext import commands


class MyHelp(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.cooldown(1, 3.0, commands.BucketType.user),
                "aliases": ['commands']
            }
        )

    async def send(self, **kwargs):
        """ a short cut to sending to get_destination """
        await self.get_destination().send(**kwargs)

    # !help
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in commands]
            if command_signatures:
                cog_name = getattr(cog, "qualified name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        await self.send(embed=embed)
