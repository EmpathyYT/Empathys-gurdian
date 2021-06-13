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
from pathlib import Path
import json
from typing import Union
import platform
from collections import OrderedDict, deque, Counter

class MiscCog(commands.Cog, name="Misc"):
    """Utility commands"""
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")



    

    @commands.command()
    async def svrmsg(self, ctx):
        """Shows the number of server messages."""
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
        """Shows the number of subscribers Empathy has."""
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
        """Sends a video suggestion to the suggestions channel."""
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
        """Sends a server suggestion to the suggestions channel."""
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
    async def msgnum(self, ctx, user: discord.User=None):
        """Shows the number of messages a user has. """
        
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        
        if user:
            cursor.execute(f"SELECT user_id, messnum FROM main WHERE user_id = '{user.id}'")
            result = cursor.fetchone()
            embed = discord.Embed(
                colour=ctx.author.color,
                title=f"{user.name} currently has `{str(result[1])}` messages.",
                description=" "
            )
            embed.timestamp = datetime.now()
            await ctx.send(embed=embed)
            
        else:
            cursor.execute(f"SELECT user_id, messnum FROM main WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            embed = discord.Embed(
                colour=ctx.author.color,
                title=f"You currently have `{str(result[1])}` messages.",
                description=" "
            )
            embed.timestamp = datetime.now()
            await ctx.send(embed=embed)
        cursor.close()
        db.close()


    @commands.command()
    async def botinfo(self, ctx):
        """Shows info about me :D."""
        b_file = open("cogs/utils/thing.json", "r")
        bot_version = json.load(b_file)
        b_file.close()
        bot_version = bot_version["bot_version"]
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description=" ",
            colour=ctx.author.colour
            
        )
        embed.timestamp = datetime.utcnow()
        embed.add_field(name="Bot Version:", value=bot_version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="EmpathyYT#1374")

        embed.set_footer(text=f"EmpathyYT | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)
    

    @commands.command()
    async def info(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """Shows info about a user."""

        user = user or ctx.author
        e = discord.Embed()
        roles = [role.name.replace('@', '@\u200b') for role in getattr(user, 'roles', [])]
        e.set_author(name=str(user))

        

        e.add_field(name='ID', value=user.id, inline=False)
        e.add_field(name='Joined', value=round_time(user.joined_at), inline=False)
        e.add_field(name='Created', value=round_time(user.created_at), inline=False)

        voice = getattr(user, 'voice', None)
        if voice is not None:
            vc = voice.channel
            other_people = len(vc.members) - 1
            voice = f'{vc.name} with {other_people} others' if other_people else f'{vc.name} by themselves'
            e.add_field(name='Voice', value=voice, inline=False)

        if roles:
            e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles', inline=False)

        colour = user.colour
        if colour.value:
            e.colour = colour

        if user.avatar:
            e.set_thumbnail(url=user.avatar_url)

        if isinstance(user, discord.User):
            e.set_footer(text='This member is not in this server.')

        await ctx.send(embed=e)


    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx, guild_id: int=None):
        """Shows info about the server."""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild

        roles = [role.name.replace('@', '@\u200b') for role in guild.roles]

        if not guild.chunked:
            async with ctx.typing():
                await guild.chunk(cache=True)

        # figure out what channels are 'secret'
        everyone = guild.default_role
        everyone_perms = everyone.permissions.value
        secret = Counter()
        totals = Counter()
        for channel in guild.channels:
            allow, deny = channel.overwrites_for(everyone).pair()
            perms = discord.Permissions((everyone_perms & ~deny.value) | allow.value)
            channel_type = type(channel)
            totals[channel_type] += 1
            if not perms.read_messages:
                secret[channel_type] += 1
            elif isinstance(channel, discord.VoiceChannel) and (not perms.connect or not perms.speak):
                secret[channel_type] += 1

        e = discord.Embed()
        e.title = guild.name
        e.description = f'**ID**: {guild.id}\n**Owner**: {guild.owner}'
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)

        channel_info = []
        key_to_emoji = {
            discord.TextChannel: '<:text_channel:847074672855613470>',
            discord.VoiceChannel: '<:voice_channel:847074556539306024>',
        }
        for key, total in totals.items():
            secrets = secret[key]
            try:
                emoji = key_to_emoji[key]
            except KeyError:
                continue

            if secrets:
                channel_info.append(f'{emoji} {total} ({secrets} locked)')
            else:
                channel_info.append(f'{emoji} {total}')

        info = []
        features = set(guild.features)
        all_features = {
            'PARTNERED': 'Partnered',
            'VERIFIED': 'Verified',
            'DISCOVERABLE': 'Server Discovery',
            'COMMUNITY': 'Community Server',
            'FEATURABLE': 'Featured',
            'WELCOME_SCREEN_ENABLED': 'Welcome Screen',
            'INVITE_SPLASH': 'Invite Splash',
            'VIP_REGIONS': 'VIP Voice Servers',
            'VANITY_URL': 'Vanity Invite',
            'COMMERCE': 'Commerce',
            'LURKABLE': 'Lurkable',
            'NEWS': 'News Channels',
            'ANIMATED_ICON': 'Animated Icon',
            'BANNER': 'Banner'
        }

        for feature, label in all_features.items():
            if feature in features:
                info.append(f'{ctx.tick(True)}: {label}')

        if info:
            e.add_field(name='Features', value='\n'.join(info))

        e.add_field(name='Channels', value='\n'.join(channel_info))

        if guild.premium_tier != 0:
            boosts = f'Level {guild.premium_tier}\n{guild.premium_subscription_count} boosts'
            last_boost = max(guild.members, key=lambda m: m.premium_since or guild.created_at)
            if last_boost.premium_since is not None:
                boosts = f'{boosts}\nLast Boost: {last_boost} ({round_time(last_boost.premium_since)})'
            e.add_field(name='Boosts', value=boosts, inline=False)

        bots = sum(m.bot for m in guild.members)
        fmt = f'Total: {guild.member_count} ({stuff.plural(bots):bot})'

        e.add_field(name='Members', value=fmt, inline=False)
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles')

        emoji_stats = Counter()
        for emoji in guild.emojis:
            if emoji.animated:
                emoji_stats['animated'] += 1
                emoji_stats['animated_disabled'] += not emoji.available
            else:
                emoji_stats['regular'] += 1
                emoji_stats['disabled'] += not emoji.available

        fmt = f'Regular: {emoji_stats["regular"]}/{guild.emoji_limit}\n' \
              f'Animated: {emoji_stats["animated"]}/{guild.emoji_limit}\n' \

        if emoji_stats['disabled'] or emoji_stats['animated_disabled']:
            fmt = f'{fmt}Disabled: {emoji_stats["disabled"]} regular, {emoji_stats["animated_disabled"]} animated\n'

        fmt = f'{fmt}Total Emoji: {len(guild.emojis)}/{guild.emoji_limit*2}'
        e.add_field(name='Emoji', value=fmt, inline=False)
        e.set_footer(text='Created').timestamp = guild.created_at
        await ctx.send(embed=e)


    @commands.command()
    async def avatar(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """Shows a user's enlarged avatar (if possible)."""
        embed = discord.Embed()
        user = user or ctx.author
        avatar = user.avatar_url_as(static_format='png')
        embed.set_author(name=str(user), url=avatar)
        embed.set_image(url=avatar)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MiscCog(bot))



def setup(bot):
    bot.add_cog(MiscCog(bot))
    