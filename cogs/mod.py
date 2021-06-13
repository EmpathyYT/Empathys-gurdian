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
from cogs.utils.checks import is_legend






class ModCog(commands.Cog, name="Mod"):
    """Commands related to moderation"""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    
    
    
    @commands.command()
    @is_legend()
    async def ban(self, ctx, member: discord.Member, *, reason):
        """Bans a member."""
        log_channel = self.bot.get_channel(801008069890408488)
        if member == ctx.author:
            await ctx.send("Sorry I can't ban you :/")
            return
        
        embeds = discord.Embed(
            colour=discord.Colour.green(),
            title=f"{member} has been banned",
            description=f"By {ctx.author.mention}"
        )
        embeds.timestamp = round_time()
        
        
        await member.ban(reason=reason)
        await ctx.send(embed=embeds)
        await log_channel.send(embed=embeds)
    
    @commands.command()
    @is_legend()
    async def kick(self, ctx, member: discord.Member, *, reason):
        """Kicks a member"""
        log_channel = self.bot.get_channel(801008069890408488)
        if member == ctx.author:
            await ctx.send("Sorry I can't kick you :/")
            return
        embeds = discord.Embed(
            colour=discord.Colour.green(),
            title=f"{member} has been kicked",
            description=f"By {ctx.author.mention}"
        )
        embeds.timestamp = round_time()
        
        
        await member.kick(reason=reason)
        await ctx.send(embed=embeds)
        await log_channel.send(embed=embeds)



    @commands.command()
    @is_legend()
    async def softban(self, ctx, member: discord.Member, *, reason):
        """Kicks a member and delete's their messages."""
        log_channel = self.bot.get_channel(801008069890408488)
        if member == ctx.author:
            await ctx.send("Sorry I can't ban you :/")
            return
        embeds = discord.Embed(
            colour=discord.Colour.green(),
            title=f"{member} has been softbanned",
            description=f"By {ctx.author.mention}"
        )
        embeds.timestamp = round_time()
        
        
        await member.ban(reason=reason)
        await ctx.guild.unban(member)
        await ctx.send(embed=embeds)
        await log_channel.send(embed=embeds)




    @commands.command()
    @is_legend()
    async def unban(self, ctx, *, member):
        """Unbans a user."""
        log_channel = self.bot.get_channel(801008069890408488)
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            try:
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    title=f"{user} has been unbanned",
                    description=f"By: {ctx.author.mention}"
                )

                await ctx.send(embed=embed)
                await log_channel.send(embed=embed)
                return
            except Exception as e:
                await ctx.send(e)
    
    
    
    
    @commands.command()
    @is_legend()
    async def purge(self, ctx, limit: int):
        """Removes multiple messages."""
        log_channel = self.bot.get_channel(801008069890408488)
        if limit >= 200:
            await ctx.send(f"Sorry `{limit}` is too large")
            return
        messages = await ctx.channel.history(limit=limit).flatten()
        new_limit = len(messages)
        embed = discord.Embed(
                colour=discord.Colour.green(),
                title=f"{len(messages)} have been purged",
                description=f"By: {ctx.author.mention}"
            )

        await ctx.channel.purge(limit=new_limit)
        await ctx.send(embed=embed)
        await log_channel.send(embed=embed)
        
    
    
    
    
    
    @commands.command()
    @is_legend()
    async def mute(self, ctx, member: discord.Member, *, timea: TimeConverter = None):
        """Mutes a member."""
        db = sqlite3.connect('mute.db')
        cursor = db.cursor()
        guild = ctx.message.guild
        role = guild.get_role(800980194692169749)
        e = get_random_alphanumeric_string(4, 5)
        if role in member.roles:
            await ctx.send("member is already muted")
            

        
        else: 
            try:
                cursor1 = db.cursor()
                sql = "INSERT INTO warns(id, warnedby, warnid, dateofwarn, action) VALUES(?, ?, ?, ?, ?)"
                val = (member.id, ctx.author.id, e, round_time(), "Mute")
                
                cursor1.execute(sql, val)
                db.commit()
                cursor1.close() 
                await member.add_roles(role)
                if timea == None:
                    return
                
                if timea and timea < 300:
                    e = discord.Embed(
                    title = f"{member} has been muted for less than 5 minutes",
                    description = f"Muted by: {ctx.author}",
                    color = ctx.author.color
                    )
                    e.timestamp = round_time()
                    log_channel = self.bot.get_channel(801008069890408488)
                    await log_channel.send(embed=e)
                    await ctx.send(embed = e)
                    await asyncio.sleep(timea)
                    
                    if role in member.roles:
                        await member.remove_roles(role)
                        
                        return
                
                else:
                    minutes, seconds = divmod(timea, 60)
                    hours, minutes = divmod(minutes, 60)
                    
                    if int(hours):
                        e = discord.Embed(
                        title = f"{member} has been muted for {hours} hours, {minutes} minutes and {seconds} seconds",
                        description = f"Muted by: {ctx.author}",
                        color = ctx.author.color
                        )
                        
                        
                        e.timestamp = round_time()
                        log_channel = self.bot.get_channel(801008069890408488)
                        await log_channel.send(embed=e)
                        await ctx.send(embed=e)
                    elif int(minutes):
                        e = discord.Embed(
                            title = f"{member} has been muted for {minutes} minutes and {seconds} seconds",
                            description = f"Muted by: {ctx.author}",
                            color = ctx.author.color
                        )
                        e.timestamp = round_time()
                        log_channel = self.bot.get_channel(801008069890408488)
                        await log_channel.send(embed=e)
                        await ctx.send(embed=e)
                    elif int(seconds):
                        e = discord.Embed(
                            title = f"{member} has been muted for {seconds} seconds",
                            description = f"Muted by: {ctx.author}",
                            color = ctx.author.color
                        )
                        e.timestamp = round_time()
                        log_channel = self.bot.get_channel(801008069890408488)
                        await log_channel.send(embed=e)
                        await ctx.send(embed=e)
                        
                    sql = (f"INSERT INTO mutes(id, timeofmute, timetofinish, mutedby) VALUES(?, ?, ?, ?)")
                    val = (member.id, 0, timea, ctx.author.id)
                    cursor.execute(sql, val)
                    cursor.close()
                    db.commit()
        
            except Exception as e:
                await ctx.send(e)





    @commands.command()
    @is_legend()
    async def unmute(self, ctx, member: discord.Member):
        """Unmutes a member."""
        guild = ctx.message.guild
        role = guild.get_role(800980194692169749)
        if role not in member.roles:
            await ctx.send("member isnt even muted bruh")
            return
        else:
            try:
                e = discord.Embed(
                title = f"{member} has been unmuted",
                description = f"Unmuted by: {ctx.author}",
                color = ctx.author.color
                )
                e.timestamp = round_time()
                log_channel = self.bot.get_channel(801008069890408488)
                await log_channel.send(embed=e)
                await member.remove_roles(role)
                db = sqlite3.connect('mute.db')
                cursor = db.cursor()
                sql = f"DELETE FROM mutes WHERE id = '{member.id}'"
                cursor.execute(sql)
                await ctx.send("unmuted!")
                cursor.close()
                db.commit()
            except Exception as e:
                await ctx.send(e)

    





    @commands.command()
    @is_legend()
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        """Warns a member."""
        db = sqlite3.connect('mute.db')
        cursor = db.cursor()
        e = get_random_alphanumeric_string(4, 5)
        sql = "INSERT INTO warns(id, warnedby, warnid, dateofwarn, action) VALUES(?, ?, ?, ?, ?)"
        val = (member.id, ctx.author.id, e, round_time(), "Warn:" + " " + reason)
        cursor.execute(sql, val)
        db.commit()
        cursor.close
        await ctx.send(f"{member.mention} has been warned. `Warn id: {e}`")
        e = discord.Embed(
                title = f"{member} has been warned",
                description = f"warned by: {ctx.author}\nWarn: {reason}\nID: {e} ",
                color = ctx.author.color
            )
        e.timestamp = round_time()
        log_channel = self.bot.get_channel(801008069890408488)
        await log_channel.send(embed=e)





    @commands.command()
    @is_legend()
    async def removewarn(self, ctx, *, warnid):
        """removes a member's warn."""
        db = sqlite3.connect("mute.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM warns WHERE warnid = '{warnid}'")
        result = cursor.fetchone()
        if result == None:
            await ctx.send(
                f"Warn: `{warnid}` doesn't exist"
            )
            return
        
        
        else:
            e = await ctx.send(f" {ctx.author.mention}, Are you sure you want to remove warn: `{warnid}`?\nReact with \U0001f44d to remove the warn")
        
        
        

            await e.add_reaction("\U0001f44d")
            
            def check(reaction, user):	
                return user == ctx.author and str(reaction.emoji) == '\U0001f44d'
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Aborted")
            else:
                cursor1 = db.cursor()
                cursor1.execute(f"SELECT id, action FROM warns WHERE warnid = '{warnid}'")
                result = cursor1.fetchone()
                mid = int(result[0])
                guild = ctx.message.guild
                mid = guild.get_member(mid)
                action = result[1]
                cursor.execute(f"DELETE FROM warns WHERE warnid = '{warnid}'")
                e = discord.Embed(
                    title = "Warn removed!",
                    color = ctx.author.color
                )
                await ctx.send(embed=e)
                db.commit()
                cursor.close()
                e = discord.Embed(
                title = f"Warn: {warnid} has been removed",
                description = f"Removed by: {ctx.author.mention}\nWarn: {action}\nWarned Member: {mid}",
                color = ctx.author.color
                )
                e.timestamp = round_time()
                log_channel = self.bot.get_channel(801008069890408488)
                await log_channel.send(embed=e)




    @commands.command()
    @is_legend()
    async def findwarn(self, ctx, *, warnid):
        """Finds a warn via WARNID."""
        db = sqlite3.connect("mute.db")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM warns WHERE warnid = '{warnid}'")
        result = cursor.fetchone()
        if result == None:
            await ctx.send(
                f"Warn: `{warnid}` doesn't exist"
            )
            return
        else:
            guild = ctx.message.guild
            db = sqlite3.connect('mute.db')
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM warns WHERE warnid='{warnid}'")
            result = cursor.fetchone()
            memberwarned = result[0]
            memberwarned = guild.get_member(memberwarned)
            warnedby = result[1]
            warnedby = guild.get_member(warnedby)
            dateofwarn = result[3]
            action = result[4]
            e = discord.Embed(
                title = action,
                color = ctx.author.color,
            )
            e.add_field(name=f"Member warned:", value= memberwarned, inline=False)
            e.add_field(name=f"Warned by:", value= warnedby.mention, inline=False)
            e.add_field(name = f"Date of warn:", value = dateofwarn + " " + "UTC", inline = False)
            
            
            await ctx.send(embed = e)






    @commands.command()
    @is_legend()
    async def findwarns(ctx, member: discord.Member):
        """Lists all of a member's warns."""
        try:
            db = sqlite3.connect('mute.db')
            cursor1 = db.cursor()
            cursor = db.cursor()
            cursor1.execute(f"SELECT action FROM warns WHERE id='{member.id}'")
            cursor.execute(f"SELECT warnid FROM warns WHERE id='{member.id}'")
            result1 = cursor1.fetchall()
            result1 = [item for t in result1 for item in t]
            result = cursor.fetchall()
            result = [item for t in result for item in t]
            e = discord.Embed(
                title = f"Warns for {member.name}",
                color = ctx.author.color
            )
            e.add_field(name=result1[0], value = f"Warn ID: " + " " + result[0])
            
            
            for fielda in result:
                for anotherfield in result1:
                    for anotherrfield in result:
                        for evenanotherfield in result1:

                            result.pop(0)
                            result1.pop(0)
                            e.add_field(name=result1[0], value = f"Warn ID: " + " " + result[0])
                        
                
            
            await ctx.send(embed = e)
        except Exception as e:
            await ctx.send(f"{member.mention} doesn't have any warnings: {e}")
    


    @commands.command()
    @is_legend()
    async def susify(self, ctx, member: discord.Member,*, reason="sus"):
        """Sends a member to the sus dimension."""
        await ctx.message.delete()
        guilds = self.bot.get_guild(800280721179541515)
        role = guilds.get_role(829298754464120862)
        role2 = guilds.get_role(800975142686687252)
        if role in member.roles:
            await ctx.send(f"{member.mention} is already sus!")
            return   
        else:
            await member.add_roles(role)
            await member.remove_roles(role2)
            channel = self.bot.get_channel(829301025549713420)
            await channel.send(f"@everyone a sus habibi has joined({member.mention}), Code: `{reason}`")





    @commands.command()
    @is_legend()
    async def unsusify(self, ctx, member: discord.Member):
        """Sends a member back to heaven."""
        await ctx.message.delete()
        guilds = self.bot.get_guild(800280721179541515)
        role = guilds.get_role(829298754464120862)
        role2 = guilds.get_role(800975142686687252)
        if role not in member.roles:
            await ctx.send(f"{ctx.author.mention} how am i supposed to unsus someone that isn't even sus?!")
            return
        else:
            await member.remove_roles(role)
            await member.add_roles(role2)
            channel = self.bot.get_channel(829301025549713420)
            await channel.send(f"Done!")

    @commands.command(aliases=['usd'])
    @is_legend()
    async def unraid(self, ctx):
        """Unlocks all channels."""


        dsds = discord.Embed(
            colour=ctx.author.color,
            title="Unlocked All channels",
            description=f"all channels are unlocked.\n\nUnlocked by : {ctx.author.mention}")
        await ctx.message.delete()
        x = self.bot.get_channel(800974918660522004)
        c = self.bot.get_channel(800280721633443863)
        b = self.bot.get_channel(800981203364478986)
        n = self.bot.get_channel(800981291116920854)
        m = self.bot.get_channel(800981401016991785)
        a = self.bot.get_channel(800981687093166100)
        p = self.bot.get_channel(829252267098112030)
        f = self.bot.get_channel(829284701189570620)
        await x.set_permissions(ctx.guild.default_role, send_messages=None)
        await c.set_permissions(ctx.guild.default_role, send_messages=None)
        await b.set_permissions(ctx.guild.default_role, send_messages=None)
        await n.set_permissions(ctx.guild.default_role, send_messages=None)
        await m.set_permissions(ctx.guild.default_role, send_messages=None)
        await a.set_permissions(ctx.guild.default_role, send_messages=None)
        await p.set_permissions(ctx.guild.default_role, send_messages=None)
        await f.set_permissions(ctx.guild.default_role, send_messages=None)
        await ctx.send(embed=dsds)




    @commands.command(aliases=['sd'])
    @is_legend()
    async def raid(self, ctx):
        """Locks all channels."""
        dsds = discord.Embed(
            colour=ctx.author.color,
            title="Emergency Server Lock",
            description=
            f"A possible raid has been triggered and all channels are locked. Please do not direct message staff members during this time. You are not muted, no one can talk.\n\nLocked by : {ctx.author.mention}"
        )
        await ctx.message.delete()
        
        x = self.bot.get_channel(800974918660522004)
        c = self.bot.get_channel(800280721633443863)
        b = self.bot.get_channel(800981203364478986)
        n = self.bot.get_channel(800981291116920854)
        m = self.bot.get_channel(800981401016991785)
        a = self.bot.get_channel(800981687093166100)
        p = self.bot.get_channel(829252267098112030)
        f = self.bot.get_channel(829284701189570620)
        await x.set_permissions(ctx.guild.default_role, send_messages=False)
        await c.set_permissions(ctx.guild.default_role, send_messages=False)
        await b.set_permissions(ctx.guild.default_role, send_messages=False)
        await n.set_permissions(ctx.guild.default_role, send_messages=False)
        await m.set_permissions(ctx.guild.default_role, send_messages=False)
        await a.set_permissions(ctx.guild.default_role, send_messages=False)
        await p.set_permissions(ctx.guild.default_role, send_messages=False)
        await f.set_permissions(ctx.guild.default_role, send_messages=False)

        await ctx.send(embed=dsds)


















def setup(bot):
    bot.add_cog(ModCog(bot))
    