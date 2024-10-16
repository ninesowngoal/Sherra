from discord.ext import commands

class Administration(commands.Cog):
    '''
    Everything to do with administration.
    '''
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="delete",
    brief = "Deletes the specified amount of messages.",
    help = """Deletes the specified amount of messages in the channel
    the command was used in.
    Deletes the command message and its own after five seconds.
    
    Usage:
    !delete (amount)""")
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx,
        num_messages: int = commands.Parameter(
            description="Amount of messages to delete.",
            name="num_messages",
            kind=commands.Parameter.VAR_POSITIONAL
        )):
        # Check if the user has specified a valid number of messages to delete
        if num_messages <= 0:
            await ctx.send("Please specify a number greater than 0.")
            return

        # Delete messages in the channel
        deleted = await ctx.channel.purge(limit=num_messages + 1)  # +1 to delete the command message itself
        await ctx.send(f"Deleted {len(deleted) - 1} messages.", delete_after=5)  # Shows message for 5 seconds
    
    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You don't have the required permission: manage messages."
            )

async def setup(bot):
    await bot.add_cog(Administration(bot))