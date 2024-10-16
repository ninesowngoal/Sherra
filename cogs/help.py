from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help_command(self, ctx):
        # Creating help text with a list of commands
        commands_list = "\n".join(
            [f"**{command.name}**: {command.help or 'No description provided.'}" for command in self.bot.commands]
        )
        help_text = f"**Available Commands:**\n{commands_list}"
        
        # Send the help text to the channel
        await ctx.send(help_text)

# Function to setup the cog
async def setup(bot):
    await bot.add_cog(Help(bot))
