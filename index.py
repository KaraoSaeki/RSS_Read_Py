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
            await message.channel.send("Entrez le flux que vous voulez lire :")
            for flux in list_flux:
                await message.channel.send(f"{flux} : {list_flux[flux]}")

            flux_choice = await self.wait_for('message', check=lambda message: message.author == message.author)

            if flux_choice.content in list_flux:
                await message.channel.send("Vous avez choisi le flux : {}".format(flux_choice.content))
                await message.channel.send("Veuillez patienter...")
                title, link = feed_parser(list_flux[flux_choice.content])
                await message.channel.send("{} \n{}".format(title, link))
            else:
                await message.channel.send("Vous avez choisi le flux n°{}".format(flux_choice.content))
                await message.channel.send(list_flux[id])

client = MyClient()
client.run(token_id)