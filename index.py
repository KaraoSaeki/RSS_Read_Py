import discord
from discord.ext import commands
import feedparser
import sys

default_intents = discord.Intents.default()
default_intents.members = True

sys.path.append('flux.py')
sys.path.append('token.py')

from token_id import token_id
from flux import list_flux
from function.feed_parser import feed_parser

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        async def on_message(message, *, content):
            await message.send(f"{content}")

        if message.content.startswith('rss'):
            #await message.channel.send(feed_parser())
            args = message.content.split()
            args.shift()
            on_message(message.content, *args)

client = MyClient()
client.run(token_id)