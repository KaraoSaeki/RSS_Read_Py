from itertools import count
import numbers
import discord
from discord.ext import commands
import feedparser
import sys

default_intents = discord.Intents.default()
default_intents.members = True

from token_id import token_id
from flux import list_flux
from commande.list_commande import commande
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
            embed = discord.Embed(color=0x00ff00)
            number_flux = len(list_flux)
            embed.add_field(name="Liste des flux", value=f"nombre de flux ={number_flux}", inline=False)
            for flux in list_flux:
                embed.add_field(name=flux, value=list_flux[flux], inline=False)
            await message.channel.send(embed=embed)

            flux_choice = await self.wait_for('message', check=lambda message: message.author == message.author)
            choix = int(flux_choice.content)
            if choix in list_flux:
                await message.channel.send("Vous avez choisi le flux : {}".format(choix))
                await message.channel.send("Veuillez patienter...")
                title, link = feed_parser(list_flux[choix])
                await message.channel.send("{} \n{}".format(title, link))
            else:
                await message.channel.send("Votre choix n'est pas dans la liste")
        
        if message.content.startswith('add'):
            args = message.content.split(" ")
            args.pop(0)
            for arg in args:
                await message.channel.send(f"Vous avez ajouté le flux : {arg}")
                list_flux[len(list_flux)+1] = arg
                await message.channel.send("Votre flux a été ajouté avec succès")

        if message.content.startswith('list'):
            embed = discord.Embed(color=0x00ff00)
            number_flux = len(list_flux)
            embed.add_field(name="Liste des flux", value=f"nombre de flux ={number_flux}", inline=False)
            for flux in list_flux:
                embed.add_field(name=flux, value=list_flux[flux], inline=False)
            await message.channel.send(embed=embed)
        
        if message.content.startswith('remove'):
            await message.channel.send("Entrez le flux que vous voulez supprimer :")
            flux_remove = await self.wait_for('message', check=lambda message: message.author == message.author)
            flux_remove = int(flux_remove.content)
            await message.channel.send("Vous avez supprimé le flux : {}".format(flux_remove))
            del list_flux[flux_remove]
            await message.channel.send("Votre flux a été supprimé avec succès")

        if message.content.startswith('help'):
            embed = discord.Embed(color=0x00ff00)
            for command in commande:
                embed.add_field(name=command, value=commande[command], inline=False)
            await message.channel.send(embed=embed)
        
        if message.content.startswith('exit'):
            await message.channel.send("Au revoir !")
            await self.logout()
            sys.exit()

        if message.content.startswith('parse'):
            await message.channel.send("Entrez le flux que vous voulez lire :")
            flux_parse = await self.wait_for('message', check=lambda message: message.author == message.author)
            flux_parse = int(flux_parse.content)
            await message.channel.send("Vous avez choisi le flux : {}".format(flux_parse))
            await message.channel.send("Veuillez patienter...")
            feed = feedparser.parse(list_flux[flux_parse])
            for entry in feed.entries:
                await message.channel.send(f"{entry['title']} \n{entry['link']}")

client = MyClient()
client.run(token_id)