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







class HelpCog(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot




    @commands.command()
    async def help(self, ctx, page=None):
        if page == None:
            e = discord.Embed(
                color = ctx.author.color,
                title='Help',
                description='Dm for mod mail :D')
            
            e.add_field(name='suggest', value="Usage: `.suggest (suggestion)`", inline=False)
            e.add_field(name='ytsuggest', value="Usage: `.ytsuggest (suggestion)`", inline=False)
            e.add_field(name='@allstaffcall', value="Pinging that role will ping all staff members incase of a raid.", inline=False)
            e.add_field(name='msgnum', value="It checks the number of messages you currently have.", inline=False)
            e.add_field(name='svrmsg', value="It checks how many messages the server currently has", inline=False)
            e.add_field(name='subscribercount', value="It checks Empathy's sub count", inline=False)
            e.add_field(name='Mod help', value="send `.help mod` to show mod commands!")
            e.add_field(name='Owner help', value="send `.help owner` to show owner commands!")
            await ctx.send(embed=e)
        
        if page == "mod":
            role = discord.utils.find(lambda r: r.name == 'law reinforcer', ctx.message.guild.roles)
            if role in ctx.author.roles:
                e = discord.Embed(
                    color = ctx.author.color,
                    title='Help Mod',
                    description=' ')
                e.add_field(name='raid', value='It locks server USE ONLY IN EMERGENCIES')
                e.add_field(name='unraid', value='It unlocks server USE ONLY IN EMERGENCIES')
                e.add_field(name='susify', value='Sends someone to the sus cell **|** Usage: `.susify [mention someone] [reason]`')
                e.add_field(name='unsusify', value='Sends someone back to the kindom **|** Usage: `.unsusify [mention someone]`')
                e.add_field(name='warn', value='Warns an outlaw **|** Usage: `.warn [mention someone] [reason here]`')
                e.add_field(name='findwarn', value='Finds a warn via warndID **|** Usage: `.findwarn [WARNID]`')
                e.add_field(name='findwarns', value="Lists a member's warnings **|** Usage: `.findwarns [mention someone]`")
                e.add_field(name='mute', value='Mutes an outlaw **|** Usage: `.mute [mention someone] Optional field: [duration, eg: 6h]`')
                e.add_field(name='unmute', value='Unmutes a member **|** Usage: `.unmute [mention someone]`')
                e.add_field(name='ban', value='Bans an outlaw **|** Usage: `.ban [mention someone] [reason here]`')
                e.add_field(name='kick', value='Kicks an outlaw **|** Usage: `.kick [mention someone] [reason here]`')
                e.add_field(name='softban', value='Kicks an outlaw and deletes their messages **|** Usage: `.softban [mention someone] [reason here]`')
                e.add_field(name='purge', value='Removes multiple messages **|** Usage: `.purge [number of messages]`')
                await ctx.send(embed=e)
            else:
                await ctx.send("You don't have permissions!")
        
        if page == "owner":
            if ctx.author.id == 528969729432485888:
                e = discord.Embed(
                        color = ctx.author.color,
                        title='Help Owner',
                        description=' ')
                e.add_field(name="logout", value='Logs the bot out **|** Usage: `.logout`')
                e.add_field(name="reload", value='Reloads a cog/all cogs **|** Usage: `.relaod Optional field:[cog name]`')
                await ctx.send(embed=e)
            else:
                await ctx.send("You're not the bot owner!")    

            
            
            










def setup(bot):
    bot.add_cog(HelpCog(bot))
    print('Help has been loaded')