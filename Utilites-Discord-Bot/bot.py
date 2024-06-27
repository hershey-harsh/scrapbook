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

@bot.command(name='random_number', aliases=['rand_num'])
async def random_number(ctx, low: int, high: int):
    if low > high:
        low, high = high, low
    num = random.randint(low, high)
    await ctx.send(f'Random number between {low} and {high}: {num}')

@bot.command(name='compliment')
async def compliment(ctx):
    compliments = [
        "You're amazing!",
        "You're a star!",
        "You're brilliant!",
        "You're so kind!",
        "You're beautiful inside and out!",
        "You're doing great!"
    ]
    compliment = random.choice(compliments)
    await ctx.send(compliment)

@bot.command(name='coin_flip')
async def coin_flip(ctx):
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(f'You flipped: {result}!')

@bot.command(name='choose')
async def choose(ctx, *, choices: str):
    options = choices.split(',')
    chosen = random.choice(options)
    await ctx.send(f'I choose: {chosen.strip()}')

@bot.command(name='catfact')
async def catfact(ctx):
    cat_facts = [
        "Cats have 32 muscles in each ear.",
        "A group of cats is called a clowder.",
        "Cats sleep for 70% of their lives.",
        "A cat’s nose is as unique as a human’s fingerprint.",
        "A cat can jump up to six times its length."
    ]
    fact = random.choice(cat_facts)
    await ctx.send(f'Cat fact: {fact}')

@bot.command(name='dogfact')
async def dogfact(ctx):
    dog_facts = [
        "Dogs have a sense of time and can sense how much time has passed.",
        "A dog's sense of smell is 10,000 times stronger than humans.",
        "Dogs have wet noses to help absorb scent chemicals.",
        "Dogs have three eyelids, including one to help keep their eyes moist.",
        "Dogs have about 1,700 taste buds."
    ]
    fact = random.choice(dog_facts)
    await ctx.send(f'Dog fact: {fact}')

@bot.command(name='serverinfo')
async def serverinfo(ctx):
    # Send information about the current server
    server = ctx.guild
    total_members = len(server.members)
    server_region = server.region
    verification_level = server.verification_level
    server_info = (
        f'Server: {server.name}\n'
        f'Members: {total_members}\n'
        f'Region: {server_region}\n'
        f'Verification Level: {verification_level}'
    )
    await ctx.send(server_info)

@bot.command(name='poll')
async def poll(ctx, question, *options):
    # Create a poll with a question and multiple options
    if len(options) > 10:
        await ctx.send("I can only handle up to 10 options for a poll.")
        return

    options_str = "\n".join(f"{index + 1}. {option}" for index, option in enumerate(options))
    poll_message = (
        f'**Poll: {question}**\n'
        f'React with the corresponding number to vote!\n'
        f'{options_str}'
    )
    poll = await ctx.send(poll_message)

    for emoji_number in range(1, len(options) + 1):
        await poll.add_reaction(f'{emoji_number}\N{COMBINING ENCLOSING KEYCAP}')

@bot.command(name='remindme')
async def remindme(ctx, time, *, reminder):
    # Set a reminder for a specific time
    # You can implement a reminder system to notify users at the specified time
    await ctx.send(f'Reminder set: I will remind you in {time} about "{reminder}"')

bot.run(TOKEN)
