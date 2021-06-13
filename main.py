import discord
from discord.ext import commands, tasks
import asyncio
import datetime
from datetime import datetime, timedelta
import os
import random
import time
from cogs.utils import stuff
import json
import aiohttp
import sqlite3
from typing import Union
import io
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
import sys
import traceback
from cogs.utils import keep_alive


#cogs list
initial_extensions = [
    'cogs.events',
    'cogs.help',
    'cogs.mod',
    'cogs.misc',
    'cogs.owner',
    'cogs.stars',
    'cogs.giveaway'
]


#Bot setup
class Bot(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents.all()
        super().__init__(command_prefix='.', 
                         description="The One And Only Empathy's Guard\nDm for Mod Mail",
                         fetch_offline_members=False, 
                         allowed_mentions=allowed_mentions, 
                         intents=intents,
                         help_command=None)

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()


    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=stuff.Context)
        
        if ctx.command is None:
            return
        
        await self.invoke(ctx)
    

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild.id == 840738399895814144:
            return
        await self.process_commands(message)
        if message.author.id == bot.user.id:
	        return
        
    
    
    
    
    #fires when the bot is ready
    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.utcnow()

        print(f'Ready: {self.user} (ID: {self.user.id})')

    
    
    
    #error handling
    async def on_command_error(ctx, error):
        if isinstance(error,commands.MissingPermissions):
            embeds = discord.Embed(
                colour=discord.Colour.red(),
                title="Sorry",
                description=f"I couldn't complete the operation since you have missing priveleges"
            )
            await ctx.send(embed=embeds)
        
        elif isinstance(error, commands.MissingRole):
            embedsz = discord.Embed(
                colour=discord.Colour.red(),
                title="Sorry",
                description=f"I couldn't complete the operation since you're not a law reinforcer"
            )
            await ctx.send(embed=embedsz)
        
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title="Sorry",
                description="Missing required argument, use `.help` for more information."
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("This command is nonexistent.")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Too many arguments.")
        elif isinstance(error, commands.NotOwner):
            await ctx.send("This command is Owner-Only")
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)
        elif isinstance(error, Union[commands.MemberNotFound, commands.UserNotFound]):
            await ctx.send("User not found")
        
    
    
    
    
    
    async def close(self):
        await super().close()
    


    def run(self):
        try:
            super().run(os.environ.get("DISCORD_BOT_SECRET"))

        finally:
            pass

#Turning on the bot
keep_alive.keep_alive()
bot = Bot()
bot.run()
