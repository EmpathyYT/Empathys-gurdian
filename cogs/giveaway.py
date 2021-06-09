import random
import discord
from discord import channel 
from discord.ext import commands, tasks
import os
import sqlite3
import asyncio
from cogs.utils.stuff import TimeConverter
from cogs.utils.stuff import get_random_alphanumeric_string
from cogs.utils.stuff import round_time
from .utils import stuff
import json
import datetime
from datetime import datetime
import aiohttp
from cogs.utils.checks import is_legend
import aiosqlite3
from pathlib import Path
import json
from typing import Union
import platform
from collections import OrderedDict, deque, Counter




class GiveawaysCog(commands.Cog, name="Giveaway"):
    def __init__(self, bot):
        self.bot = bot
    

    #fires when the cog is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    
    @commands.command()
    @commands.is_owner()
    async def giveaway(self, ctx, timea: TimeConverter, *, prize):
        """Starts a giveaway."""
        db = sqlite3.connect("mute.db")
        cursor = db.cursor()
        
        if timea and timea < 300:
                await ctx.send("@everyone")
                e = discord.Embed(
                title = f"{ctx.author} started a giveaway",
                description = f"It ends in less than 5 mins\nPrize: {prize}\nReact with \U0001f381 to join",
                color = ctx.author.color
                )
                e.timestamp = round_time()
                e = await ctx.send(embed = e)
                await e.add_reaction('\U0001f381')
                sql = "INSERT INTO giveaways(starttime, endtime, prize, messageid) VALUES(?, ?, ?, ?)"
                val = (0, timea, prize, e.id)
                cursor.execute(sql, val)
                db.commit()
                return
            
        else:
            minutes, seconds = divmod(timea, 60)
            hours, minutes = divmod(minutes, 60)
            await ctx.send("@everyone")
            if int(hours):
                e = discord.Embed(
            title = f"{ctx.author.mention} started a giveaway",
                description = f"It ends in {hours} hours, {minutes} minutes and {seconds} seconds\nPrize: {prize}\nReact with \U0001f381 to join",
                color = ctx.author.color
                )
                
                
                e.timestamp = round_time()
                
                e = await ctx.send(embed=e)
                await e.add_reaction('\U0001f381')
                sql = "INSERT INTO giveaways(starttime, endtime, prize, messageid) VALUES(?, ?, ?, ?)"
                val = (0, timea, prize, e.id)
                cursor.execute(sql, val)
                db.commit()        
            elif int(minutes):
                e = discord.Embed(
                title = f"{ctx.author.mention} started a giveaway",
                    description = f"It ends in {minutes} minutes and {seconds} seconds\nPrize: {prize}\nReact with \U0001f381 to join",
                    
                    color = ctx.author.color
                )
                e.timestamp = round_time()
                
                e = await ctx.send(embed=e)
                await e.add_reaction('\U0001f381')
                sql = "INSERT INTO giveaways(starttime, endtime, prize, messageid) VALUES(?, ?, ?, ?)"
                val = (0, timea, prize, e.id)
                cursor.execute(sql, val)
                db.commit()        
            elif int(seconds):
                e = discord.Embed(
                    title = f"{ctx.author.mention} started a giveaway",
                    description = f"It ends in {seconds} seconds\nPrize: {prize}\nReact with \U0001f381 to join",
                    color = ctx.author.color
                )
                e.timestamp = round_time()
                
                e = await ctx.send(embed=e)
                await e.add_reaction('\U0001f381')
                sql = "INSERT INTO giveaways(starttime, endtime, prize, messageid) VALUES(?, ?, ?, ?)"
                val = (0, timea, prize, e.id)
                cursor.execute(sql, val)
                db.commit()


def setup(bot):
    bot.add_cog(GiveawaysCog(bot))
    