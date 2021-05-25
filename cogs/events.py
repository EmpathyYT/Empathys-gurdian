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
import aiohttp
from cogs.utils.checks import is_legend





class EventsCog(commands.Cog, name="Events"):
    def __init__(self, bot):
        self.bot = bot
        self.giveawaything.start()
        self.mutething.start()
        self.ff.start()
        self.fd.start()
        self.status.start()





    @tasks.loop(seconds=60)
    async def giveawaything(self):
        db = sqlite3.connect('mute.db')
        cursor = db.cursor()
        cursor.execute("UPDATE giveaways SET starttime = starttime + 60")  
        db.commit()
        cursor.execute(f"SELECT messageid, prize FROM giveaways WHERE starttime >= endtime")
        result = cursor.fetchall()
        result = [item for t in result for item in t]
        
        guild = 800280721179541515
        channel1 = 801006674093015082
        channel = self.bot.get_channel(channel1)
        for thing in result:
            message = await channel.fetch_message(result[0])
            users = await message.reactions[0].users().flatten()
            users.pop(users.index(channel.guild.me))
            
            winner = random.choice(users)
            
            e = discord.Embed(
                title = f"{winner} has won the giveaway!",
                description = f"Prize: {result[1]}.\nDm Empathy to claim the prize!!",
                color = discord.Colour.green()
            )
            
            await channel.send(f"https://discord.com/channels/{guild}/{channel1}/{result[0]}")
            await channel.send(winner.mention)
            await channel.send(embed = e)
            result.pop(0)
            result.pop(0)
            cursor.execute("DELETE FROM giveaways WHERE starttime >= endtime")
            cursor.close()
            db.commit()

    
    @giveawaything.before_loop
    async def before_change_statusa(self):
        await self.bot.wait_until_ready()






    @tasks.loop(seconds=60)
    async def mutething(self):
    
        db = sqlite3.connect('mute.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT timeofmute FROM mutes")
        
        cursor.execute(f"UPDATE mutes SET timeofmute = timeofmute + 60")
        db.commit()
        
        
        

        cursor.execute(f"SELECT id FROM mutes WHERE timeofmute >= timetofinish")
        result1 = cursor.fetchall()
        out = [item for t in result1 for item in t]
        out = [int(i) for i in out]
        guild = self.bot.get_guild(800280721179541515)
        role = guild.get_role(800980194692169749)
        for mid in out:
            member = guild.get_member(mid)
            await member.remove_roles(role)
            e = discord.Embed(
                title = f"{member} has been automatically unmuted",
                color = discord.Color.green()
            )
            e.timestamp = round_time()
            log_channel = self.bot.get_channel(801008069890408488)
            await log_channel.send(embed=e)
        cursor.execute(f"DELETE FROM mutes WHERE timeofmute >= timetofinish")
        cursor.close()
        db.commit()
    
    
    

    
    @mutething.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()



    @tasks.loop(seconds=180)
    async def status(self):
    
        member_count = self.bot.get_guild(800280721179541515)
        activitys=discord.Status.do_not_disturb
        activity = discord.Game(name=f'Dm for modmail || Entertaining {member_count.member_count} members', type=3)
        await self.bot.change_presence(status=activitys, activity=activity)
        channel = self.bot.get_channel(830728950543155230)
        await channel.edit(name=f"Member Count: {member_count.member_count}")


    
    @status.before_loop
    async def before_change_statusas(self):
        await self.bot.wait_until_ready()











    @tasks.loop(seconds=500)
    async def fd(self):
        token = "AIzaSyAtpJBbyi7ClOyEI8Oxdsb4mCKRTauHx5s"
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC1HLnJprOsUmQlS9iRaXhzQ&key={token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                response = await r.json()
        x = response
        e = self.bot.get_channel(829266141906075678)
        subs = x["items"][0]["statistics"]["viewCount"]
        await e.edit(name="View Count:"+ " "+ "{:,d}".format(int(subs)))
        



    


    @fd.before_loop
    async def qas(self):
        await self.bot.wait_until_ready()


    @tasks.loop(seconds=500)
    async def ff(self):
        token = "AIzaSyAtpJBbyi7ClOyEI8Oxdsb4mCKRTauHx5s"
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC1HLnJprOsUmQlS9iRaXhzQ&key={token}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                response = await r.json()
        x = response
        e = self.bot.get_channel(801455671497064518)
        subs = x["items"][0]["statistics"]["subscriberCount"]
        await e.edit(name="Subscriber count:"+ " "+ "{:,d}".format(int(subs)))
        



    





    @ff.before_loop
    async def before_change_statusfsdf(self):
        await self.bot.wait_until_ready()





def setup(bot):
    bot.add_cog(EventsCog(bot))
    print('Events has been loaded')