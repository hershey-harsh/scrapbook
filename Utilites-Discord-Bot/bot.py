import discord
import random
import aiohttp
import asyncio
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

@bot.command(name='weather')
async def weather(ctx, *, city: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=<redacted>') as resp:
            if resp.status == 200:
                data = await resp.json()
                description = data['weather'][0]['description']
                temp = data['main']['temp'] - 273.15
                await ctx.send(f'Weather in {city}: {description}, {temp:.2f}°C')
            else:
                await ctx.send('City not found.')

@bot.command(name='translate')
async def translate(ctx, target_language: str, *, text: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.mymemory.translated.net/get?q={text}&langpair=en|{target_language}') as resp:
            if resp.status == 200:
                data = await resp.json()
                translated_text = data['responseData']['translatedText']
                await ctx.send(f'Translation: {translated_text}')
            else:
                await ctx.send('Translation service error.')

@bot.command(name='shorten')
async def shorten(ctx, *, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://cleanuri.com/api/v1/shorten', data={'url': url}) as resp:
            if resp.status == 200:
                data = await resp.json()
                short_url = data['result_url']
                await ctx.send(f'Shortened URL: {short_url}')
            else:
                await ctx.send('URL shortening service error.')

@bot.command(name='countdown')
async def countdown(ctx, seconds: int):
    if seconds > 3600:
        await ctx.send("The countdown cannot be longer than 1 hour.")
        return

    message = await ctx.send(f'{seconds} seconds remaining...')
    while seconds > 0:
        await asyncio.sleep(1)
        seconds -= 1
        await message.edit(content=f'{seconds} seconds remaining...')
    await ctx.send('Countdown complete!')

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

@bot.command(name='reverse')
async def reverse(ctx, *, text: str):
    reversed_text = text[::-1]
    await ctx.send(f'Reversed text: {reversed_text}')

@bot.command(name='random_user')
async def random_user(ctx):
    members = ctx.guild.members
    random_member = random.choice(members)
    await ctx.send(f'A random user: {random_member.mention}')

@bot.command(name='roll_dice', aliases=['dice_roll'])
async def roll_dice(ctx, num_dice: int = 1):
    if num_dice > 10:
        await ctx.send("I can only roll up to 10 dice at a time!")
        return

    results = [random.randint(1, 6) for _ in range(num_dice)]
    await ctx.send(f'You rolled: {", ".join(map(str, results))}')

@bot.command(name='say_hi', aliases=['hello'])
async def say_hi(ctx):
    greetings = [
        "Hello!",
        "Hi there!",
        "Hey!",
        "Greetings!",
        "Howdy!",
        "Nice to see you!"
    ]
    greeting = random.choice(greetings)
    await ctx.send(greeting)

@bot.command(name='insult')
async def insult(ctx):
    insults = [
        "You're as bright as a black hole.",
        "You're a sandwich short of a picnic.",
        "If brains were dynamite, you wouldn’t have enough to blow your nose.",
        "You're not the sharpest tool in the shed, are you?",
        "You're the human equivalent of a participation award."
    ]
    insult = random.choice(insults)
    await ctx.send(insult)

@bot.command(name='echo')
async def echo(ctx, *, message):
    await ctx.send(message)

bot.run(TOKEN)
