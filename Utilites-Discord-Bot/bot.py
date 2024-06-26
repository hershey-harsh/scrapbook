import discord
import random

from discord.ext import commands

TOKEN = '<redacted>'

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='die_roll', aliases=['roll'])
async def die_roll(ctx):
    roll_result = random.randint(1, 6)
    
    await ctx.send(f'You rolled a {roll_result}!')

@bot.command(name='mock')
async def mock_text(ctx, *, text):
    mock_text = ''.join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(text))
    await ctx.send(mock_text)

@bot.command(name='countdown')
async def countdown(ctx, seconds: int):
    for i in range(seconds, 0, -1):
        await ctx.send(f'{i} seconds remaining...')
        await asyncio.sleep(1)
    await ctx.send('Countdown complete!')

bot.run(TOKEN)
