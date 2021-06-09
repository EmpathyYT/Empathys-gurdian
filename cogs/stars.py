from cogs.utils.checks import is_legend
import discord
from discord import embeds
from discord.channel import TextChannel
from discord.ext import commands, tasks
import platform
import datetime
from datetime import datetime
from typing import Union

from discord.message import Attachment
from cogs.utils.stuff import round_time
from cogs.utils.stuff import get_random_alphanumeric_string
import json
from collections import OrderedDict, deque, Counter
from .utils import stuff
import sqlite3
import os, shutil
from pathlib import Path

class StarError(commands.CheckFailure):
    pass
class StarsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        if payload.guild_id is None:
            return
        db = sqlite3.connect("mute.db")
        cursor = db.cursor()
        if str(payload.emoji) == "\U00002b50":
            
            cursor.execute(f"SELECT * FROM stars WHERE messageid = '{payload.message_id}' AND channelid = {payload.channel_id}")
            result =  cursor.fetchone()
            if result == None:
                sql = "INSERT INTO stars(numberofstars, messageid, channelid, starboardmessageid) VALUES(?, ?, ?, ?)"
                val = (1, payload.message_id, payload.channel_id, 0)
                cursor.execute(sql, val)
                db.commit()
            
            cursor.execute(f"SELECT * FROM stars WHERE messageid = '{payload.message_id}' AND channelid = {payload.channel_id}")
            result = cursor.fetchone()
            stars = int(result[0])
            sql = ("UPDATE stars SET numberofstars = ?, messageid = ?, channelid = ?")
            val = (stars + 1, int(payload.message_id), int(payload.channel_id))
            cursor.execute(sql, val)
            db.commit()
            cursor.execute(f"SELECT * FROM stars WHERE messageid = '{payload.message_id}' AND channelid = {payload.channel_id}")
            result = cursor.fetchone()
            stars = int(result[0])
            messageid = int(result[1])
            channelid = int(result[2])
            if stars >= 1:
                
                channel = self.bot.get_channel(852294025083879434   )
                anotherchannel = self.bot.get_channel(channelid)
                message = await anotherchannel.fetch_message(messageid)
                if message is None:
                    raise StarError('\N{BLACK QUESTION MARK ORNAMENT} This message could not be found.')
                    return
                if (len(message.content) == 0 and len(message.attachments) == 0) or message.type is not discord.MessageType.default:
                        raise StarError('\N{NO ENTRY SIGN} This message cannot be starred.')
                        return
                
                if len(message.attachments) == 0:
                    e = discord.Embed(
                        title = message.author.name,
                        description = f" ",
                        color = discord.Colour.random()
                    )
                    
                    e.add_field(name="Message:", value=message.content, inline=False)
                    e.add_field(name="Original:", value=f"[Jump]({message.jump_url} \"Jump to message\")")
                    e.timestamp = datetime.utcnow()
                    e = await channel.send(f"Channel: {anotherchannel.mention}, ID: {message.id}", embed = e)
                    
                    cursor.execute(f"UPDATE stars SET starboardmessageid = {e.id} WHERE messageid = '{payload.message_id}' AND channelid = {payload.channel_id}") 
                    cursor.close()
                    db.commit()
                    return
                else:
                    
                    e = discord.Embed(
                        title = message.author.name,
                        description = f" ",
                        color = discord.Colour.random()
                    )
                    if len(message.content) == 0:
                        e.add_field(name="Original:", value=f"[Jump]({message.jump_url} \"Jump to message\")", inline=False)
                    else:    
                        e.add_field(name="Message:", value=message.content, inline=False)
                        e.add_field(name="Original:", value=f"[Jump]({message.jump_url} \"Jump to message\")", inline=False)
                    e.timestamp = datetime.utcnow()
                    if message.attachments:
                        file = message.attachments[0]
                        spoiler = file.is_spoiler()
                        if not spoiler and file.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                            e.set_image(url=file.url)
                        elif spoiler:
                            e.add_field(name='Attachment', value=f'||[{file.filename}]({file.url})||', inline=False)
                        else:
                            e.add_field(name='Attachment', value=f'[{file.filename}]({file.url})', inline=False)


                    
                    e = await channel.send(f"Channel: {anotherchannel.mention}, ID: {message.id}", embed=e)
                    cursor.execute(f"UPDATE stars SET starboardmessageid = {e.id} WHERE messageid = '{payload.message_id}' AND channelid = {payload.channel_id}") 
                    cursor.close()
                    db.commit()

                    




    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        
        db = sqlite3.connect("mute.db")
        cursor = db.cursor()
        if str(payload.emoji) == "\U00002b50":
            
            cursor.execute(f"SELECT * FROM stars WHERE messageid = '{payload.message_id}' AND channelid = '{payload.channel_id}'")
            result = cursor.fetchone()
            stars = int(result[0])
            sql = ("UPDATE stars SET numberofstars = ?, messageid = ?, channelid = ?")
            val = (stars - 1, int(payload.message_id), int(payload.channel_id))
            cursor.execute(sql, val)
            db.commit()
            cursor.execute(f"SELECT * FROM stars WHERE messageid = '{payload.message_id}' AND channelid = {payload.channel_id}")
            result = cursor.fetchone()
            stars = int(result[0])
            messageid = int(result[1])
            channelid = int(result[2])
            if stars < 1:
                
                channel = self.bot.get_channel(852294025083879434)
                anotherchannel = self.bot.get_channel(channelid)
                message = await anotherchannel.fetch_message(messageid)
                if message is None:
                    raise StarError('\N{BLACK QUESTION MARK ORNAMENT} This message could not be found.')
                    return
                if (len(message.content) == 0 and len(message.attachments) == 0) or message.type is not discord.MessageType.default:
                        raise StarError('\N{NO ENTRY SIGN} This message cannot be unstarred.')
                        return
                
                cursor.execute(f"SELECT starboardmessageid FROM stars WHERE messageid = '{payload.message_id}' AND channelid = '{payload.channel_id}'")
                result = cursor.fetchone()
                thing = int(result[0])
                message = await channel.fetch_message(thing)
                await message.delete()
                cursor.execute(f"DELETE FROM stars WHERE starboardmessageid = '{thing}'")
                db.commit()


    @commands.command()
    @is_legend
    async def forcestar(self, ctx, starid: int, channel: TextChannel):
        """Forcefully stars a message"""
        db = sqlite3.connect("mute.db")
        cursor = db.cursor()
        
        
        anotherchannel = self.bot.get_channel(852294025083879434)
        cursor.execute(f"SELECT * FROM stars WHERE messageid = '{starid}'")
        result =  cursor.fetchone()
        if result is not None:
            await ctx.send("Message is already on the starboard!")
            return
        if result is None:
            
            message = await channel.fetch_message(starid)
            if message is None:
                await ctx.send("Message doesn't exist or message not in given channel!")
                return
            sql = "INSERT INTO stars(numberofstars, messageid, channelid, starboardmessageid) VALUES(?, ?, ?, ?)"
            val = (1, message.id, channel.id, 0)
            cursor.execute(sql, val)
            db.commit()
            if (len(message.content) == 0 and len(message.attachments) == 0) or message.type is not discord.MessageType.default:
                            raise StarError('\N{NO ENTRY SIGN} This message cannot be starred.')
                            return
                    
            if len(message.attachments) == 0:
                e = discord.Embed(
                    title = message.author.name,
                    description = f" ",
                    color = discord.Colour.random()
                )
                
                e.add_field(name="Message:", value=message.content, inline=False)
                e.add_field(name="Original:", value=f"[Jump]({message.jump_url} \"Jump to message\")")
                e.timestamp = datetime.utcnow()
                e = await anotherchannel.send(f"Channel: {channel.mention}, ID: {message.id}", embed = e)
                
                cursor.execute(f"UPDATE stars SET starboardmessageid = {e.id} WHERE messageid = '{message.id}' AND channelid = {channel.id}") 
                cursor.close()
                db.commit()
                return
            else:
                
                e = discord.Embed(
                    title = message.author.name,
                    description = f" ",
                    color = discord.Colour.random()
                )
                if len(message.content) == 0:
                    e.add_field(name="Original:", value=f"[Jump]({message.jump_url} \"Jump to message\")", inline=False)
                else:    
                    e.add_field(name="Message:", value=message.content, inline=False)
                    e.add_field(name="Original:", value=f"[Jump]({message.jump_url} \"Jump to message\")", inline=False)
                e.timestamp = datetime.utcnow()
                if message.attachments:
                    file = message.attachments[0]
                    spoiler = file.is_spoiler()
                    if not spoiler and file.url.lower().endswith(('png', 'jpeg', 'jpg', 'gif', 'webp')):
                        e.set_image(url=file.url)
                    elif spoiler:
                        e.add_field(name='Attachment', value=f'||[{file.filename}]({file.url})||', inline=False)
                    else:
                        e.add_field(name='Attachment', value=f'[{file.filename}]({file.url})', inline=False)


                
                e = await anotherchannel.send(f"Channel: {channel.mention}, ID: {message.id}", embed=e)
                cursor.execute(f"UPDATE stars SET starboardmessageid = {e.id} WHERE messageid = '{message.id}' AND channelid = {channel.id}") 
                cursor.close()
                db.commit()

    @commands.command()
    @is_legend()
    async def forceunstar(self, ctx, starid: int):
        """Forcefully unstars a message"""
        db = sqlite3.connect("mute.db")

        cursor = db.cursor()
        starchannel = self.bot.get_channel(852294025083879434)
        cursor.execute(f"SELECT * FROM stars WHERE starboardmessageid = '{starid}'")
        result =  cursor.fetchone()
        if result is None:
            await ctx.send("Message isn't on the leaderboard doesn't exist")
            return
        if result is not None:
            message = await starchannel.fetch_message(starid)
            if message is None:
                await ctx.send("Message not on starboard!")
                return
            if (len(message.content) == 0 and len(message.attachments) == 0) or message.type is not discord.MessageType.default:
                            raise StarError('\N{NO ENTRY SIGN} This message cannot be unstarred.')
                            return
            cursor.execute(f"DELETE FROM stars WHERE starboardmessageid = '{starid}'")
            db.commit()
            await message.delete()

        






def setup(bot):            
    bot.add_cog(StarsCog(bot))
    