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
import json
import datetime
from datetime import datetime
import aiohttp
from cogs.utils.checks import is_legend



class MiscCog(commands.Cog, name="Misc"):
    def __init__(self, bot):
        self.bot = bot


    



    @commands.command()
    @commands.is_owner()
    async def giveaway(self, ctx, timea: TimeConverter, *, prize):
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

    @commands.command()
    async def svrmsg(self, ctx):
        a_file = open("cogs/msgs.json", "r")
        json_object = json.load(a_file)
        a_file.close()
        x = json_object["messages"]
        embed = discord.Embed(
            colour=ctx.author.color,
            title=f"Server currently has `{x}` messages.",
            description=" "
        )
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)
        
    @commands.command()
    async def subscribercount(self, ctx):
        token = "AIzaSyAtpJBbyi7ClOyEI8Oxdsb4mCKRTauHx5s"
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC1HLnJprOsUmQlS9iRaXhzQ&key={token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                response = await r.json()
        x = response
        
        
        e = discord.Embed(
            color = ctx.author.color,
            title = "Subscribers",
            description =x["items"][0]["statistics"]["subscriberCount"]
        )
        e.timestamp = datetime.utcnow()
        
        await ctx.send(embed=e)






    @commands.command()
    async def ytsuggest(self, ctx,*, suggestion):
        await ctx.message.delete()
        e = discord.Embed(
        title=f'by {ctx.author.name}',
        description=' ',
        color=ctx.author.color
        )
        e.add_field(name=suggestion, value='\u200b', inline=False)
        e.set_thumbnail(url=ctx.author.avatar_url)

    
        w = self.bot.get_channel(800981534508187658)
        
        
        ea = await w.send(embed=e)
        await ea.add_reaction('\U0000274c')
        await ea.add_reaction('\U00002705')






    @commands.command()
    async def suggest(self, ctx,*, suggestion):
        await ctx.message.delete()
        e = discord.Embed(
        title=f'by {ctx.author.name}',
        description=' ',
        color=ctx.author.color
        )
        e.add_field(name=suggestion, value='\u200b', inline=False)
        e.set_thumbnail(url=ctx.author.avatar_url)

    
        w = self.bot.get_channel(800981534508187658)
        
        
        ea = await w.send(embed=e)
        await ea.add_reaction('\U0000274c')
        await ea.add_reaction('\U00002705')

def setup(bot):
    bot.add_cog(MiscCog(bot))
    print('Misc has been loaded')