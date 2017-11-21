#!/usr/bin/env python3

from os import environ
from random import randint
from discord.ext import commands
from aiohttp import web
import asyncio
from base64 import b64decode
import json


debug = environ.get('DEBUG', False)
buildbot_auth_user = environ.get('BUILDBOT_AUTH_USER', 'buildbot')
buildbot_auth_pass = environ.get('BUILDBOT_AUTH_PASS')

bot = commands.Bot(command_prefix='bender ')

app = web.Application()
routes = web.RouteTableDef()


def buildbot_authenticate(request):
    auth = request.headers['authorization'].split(' ')
    auth_text = b64decode(auth[1])
    return auth_text != buildbot_auth_user + ':' + buildbot_auth_pass


@routes.post('/buildbot')
async def buildbot_event(request):
    if buildbot_authenticate(request):
        data = await request.json()
        if debug:
            pretty = json.dumps(data, indent=2, sort_keys=False)
            print('/buildbot => json:', pretty)
        state_string = data['state_string']
        builder = data['builder']['name']
        number = data['number']
        message = '{} #{}: {}'.format(builder, number, state_string)
        for channel in bot.get_all_channels():
            if channel.name == 'general':
                await bot.send_message(channel, message)
    return web.Response()


@bot.event
async def on_ready():
    print('Logged in as {}'.format(bot.user.name))


quotes = [
    'Quit squawking, fleshwad!',
    'Bite my shiny metal ass.',
    'Hahahahaha. Oh wait you’re serious. Let me laugh even harder.',
    'I guess if you want children beaten, you have to do it yourself.'
]


@bot.command()
async def quote():
    message = quotes[randint(0, len(quotes) - 1)]
    await bot.say(message)


loop = asyncio.get_event_loop()
app.router.add_routes(routes)
handler = app.make_handler()
f = loop.create_server(handler, '0.0.0.0', 1111)
srv = loop.run_until_complete(f)
print('Http server listening')
bot.run(environ['DISCORD_TOKEN'])
