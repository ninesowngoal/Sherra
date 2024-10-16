import discord

def server_join(bot):
    @bot.event
    async def on_guild_join(guild):
        '''
        DMs the user who added the bot to the server.
        Gives a brief outline of main functions.
        '''
        async for entry in guild.audit_logs(
            limit=1, action=discord.AuditLogAction.bot_add):
            inviter = entry.user
            embed = discord.Embed(
            title = "Thank you for adding me to your server!")
            # embed.set_thumbnail(
            #     url=""
            #     )
            embed.add_field(
                name="**Help commands**", 
                value="""`!help` Lists all commands.
                `!help [command name]` Gives info about a specific command."""
                )
            embed.set_footer(
                text="github link: https://github.com/ninesowngoal/Sherra"
                )
        await inviter.send(embed=embed)