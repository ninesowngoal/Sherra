import asyncio
import discord
from discord.ext import commands

import os
absolute_path = os.path.dirname(__file__)
root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Enable logging.
import logging
import logging.handlers
logger = logging.getLogger('discord')

class Upload(commands.Cog):
    '''
    Everything to do with uploading files.
    '''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = "upload", 
    brief = "Uploads files from a specified directory.",
    help = """Uploads files from a specified directory with the specified sorting and amount.
    If no sorting method has been stated, then it defaults to alphabetical sorting.
    
    Usage:
    !upload "(directory)" (sort) (amount)""")
    @commands.has_permissions(administrator = True)
    async def upload(self, ctx,
        directory: str = commands.Parameter(
            description="The directory to the file(s).",
            name="directory",
            kind=commands.Parameter.VAR_POSITIONAL
        ),
        sorting: str = commands.Parameter(
            description="How to sort the files.",
            name="sort",
            kind=commands.Parameter.VAR_POSITIONAL
        ),
        batch: int = commands.Parameter(
            description="The amount of files to be uploaded (max 10).",
            name="batch",
            kind=commands.Parameter.VAR_POSITIONAL)):
        files_uploaded = 0

        # Check if directory exists.
        if not os.path.isdir(directory):
            await ctx.send(f"""
                           [{directory}]
                           That directory doesn't exist!
                           """)
            return
        
        # Get a list of files in the directory.
        files = [f for f in os.listdir(directory)
                 if os.path.isfile(os.path.join(directory, f)) and
                 os.path.getsize(os.path.join(directory, f)) < 10 * 1024 * 1024]
        
        # Log the number of files found
        logger.debug(f"Found {len(files)} files in {directory}.")

        # Sorting options.
        # Sort by date (modified).
        if sorting == "date":
            files.sort(key = lambda f: os.path.getmtime(os.path.join(directory, f)))
        elif sorting == "type":
            files.sort(key = lambda f: os.path.splitext(f)[1])
        else:
            files.sort() # Defaults to alphabetical sorting.
        
        # Ensuring the user inputs a valid number for the batch size.
        if not (1 <= batch <= 10):
            await ctx.send(
                "Please specify a number between 1 and 10 for the batch size."
            )
            return

        # Upload the specified amount.
        for f in range(0, len(files), 10):
            batch_files = files[f:f + 10] # Get the next batch of 10 files
            file_objects = [] # Create a list to hold discord.File objects

            for filename in batch_files:
                file_path = os.path.join(directory, filename)
                file_objects.append(discord.File(file_path, filename)) # Add file to the list 

            # Debug
            logger.debug(
            f"Preparing to upload {len(file_objects)} files: {[file.filename for file in file_objects]}"
            )       

            try:
                # Attempt to send files
                if batch == 1:
                    for file_object in file_objects:
                        await ctx.send(file=file_object)
                        files_uploaded += 1
                else:
                    if file_objects:
                        await ctx.send(files=file_objects)
                        files_uploaded += len(file_objects)
                logger.info(f"Successfully uploaded {files_uploaded} files.")
            except Exception as e:
                logger.error(f"Error uploading files: {e}")
            
            # Notify how many files have been uploaded so far.
            await ctx.send(f"Uploaded {files_uploaded} files so far.")

            # Pause between batches to avoid overloading the server.
            await asyncio.sleep(3) # 3 second pause.
        
        await ctx.send(f"All files uploaded. Total: {files_uploaded} files.")
        print(
        f"""[{ctx.guild.name}]\nUploaded {files_uploaded} files in {ctx.channel.name}.\n"""
        )

    @upload.error
    async def upload_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You don't have the required permission: Admin."
            )

async def setup(bot):
    await bot.add_cog(Upload(bot))