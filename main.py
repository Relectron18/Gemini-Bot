import settings
import discord
from discord.ext import commands
import asyncio
from cogs.GeminiCog import GeminiAgent




intents= discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="&",intents=intents,help_command=None)

@bot.event
async def on_ready():
    print("Bot is online..")

@bot.event
async def on_member_join(member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!👋'
            await guild.system_channel.send(to_send)

@bot.command()
async def unloadGemini(ctx):
    await bot.remove_cog('GeminiAgent')

@bot.command()
async def reloadGemini(ctx):
    await bot.add_cog(GeminiAgent(bot))

async def startcogs():
    await bot.add_cog(GeminiAgent(bot))

asyncio.run(startcogs())

@bot.command()
async def remind(ctx, time: int, *, reminder = "time\'s up baby"):
    await ctx.send(f"Okay, {ctx.author.mention}! I'll remind you in {time} seconds.")
    await asyncio.sleep(time)
    await ctx.send(f"Reminder for {ctx.author.mention}: {reminder}")

bot.run(settings.DISCORD_SDK)