import discord
from discord.ext import commands
import feedparser

from function.feed_parser import feed_parser

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content.startswith('rss'):
            for list in flux :
                await message.channel.send(list)
                if message.content.startswith('1'):
                    await message.channel.send(list[1])
            await message.channel.send(feed_parser(message.content))

client = MyClient()
client.run('OTgzMzc2OTkwMDA0NDQ1MjQ0.G4lDaB.ABDR585VOIcnDxcxr82iyIB1qlO3MPxQ1RhDQA')