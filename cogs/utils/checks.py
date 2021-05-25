import discord
from discord.ext import commands



def is_legend():
        async def predicate(ctx):
            guild = ctx.message.guild
            role = guild.get_role(829371403215831070)
            return ctx.guild is not None \
                and role in ctx.author.roles
                
        return commands.check(predicate)