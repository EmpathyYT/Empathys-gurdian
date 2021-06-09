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
import datetime
from datetime import datetime
import traceback





class OwnerCog(commands.Cog, name="Owner"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


    @commands.command(aliases=['disconnect', 'close', 'stopbot'])
    @commands.is_owner()
    async def logout(self, ctx):
        """
        If the user running the command owns the bot then this will disconnect the bot from discord.
        """
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()
    

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        """Reloads all/a selected cog."""
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)


    @commands.command()
    @commands.is_owner()
    async def roleretroscan(self, ctx):
        """Makes sure all members have the required roles."""
        member_count = self.bot.get_guild(800280721179541515)
        rolex = member_count.get_role(830125506749136946)
        roley = member_count.get_role(830124591870509056)
        rolez = member_count.get_role(830125863248723988)
        roleu = member_count.get_role(830125364310704218)
        list = [rolex, roley, rolez, roleu]
        for role_id in list:
            for members in member_count.members:
                await members.add_roles(role_id)
        await ctx.send("done!") 



def setup(bot):
    bot.add_cog(OwnerCog(bot))
    