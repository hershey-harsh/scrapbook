import discord
import random

from discord.ext import commands

TOKEN = '<redacted>'

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='8ball')
async def eight_ball(ctx, *, question):
    responses = [
        "Yes.",
        "No.",
        "Maybe.",
        "Ask again later.",
        "My sources say no.",
        "Outlook not so good.",
        "Most likely.",
        "Cannot predict now."
    ]

    response = random.choice(responses)
    await ctx.send(response)

bot.run(TOKEN)
