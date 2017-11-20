from os import environ
from random import randint
from discord.ext import commands

bot = commands.Bot(command_prefix='bender ')


@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user.name))


quotes = [
    'Quit squawking, fleshwad!',
    'Bite my shiny metal ass.'
]


@bot.command()
async def quote():
    message = quotes[randint(0, len(quotes) - 1)]
    await bot.say(message)


bot.run(environ['DISCORD_TOKEN'])
