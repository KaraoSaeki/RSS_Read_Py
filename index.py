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

            choix = int(flux_choice.content)
            if choix in list_flux:
                await message.channel.send("Vous avez choisi le flux : {}".format(choix))
                await message.channel.send("Veuillez patienter...")
                title, link = feed_parser(list_flux[choix])
                await message.channel.send("{} \n{}".format(title, link))
            else:
                await message.channel.send("Vous avez choisi le flux n°{}".format(choix))
                await message.channel.send(list_flux[choix])
        
        if message.content.startswith('add'):
            await message.channel.send("Entrez le lien que vous voulez ajouter :")
            flux_add = await self.wait_for('message', check=lambda message: message.author == message.author)
            await message.channel.send("Vous avez ajouté le flux : {}".format(flux_add.content))
            list_flux[len(list_flux)+1] = flux_add.content
            await message.channel.send("Veuillez patienter...")
            title, link = feed_parser(flux_add.content)
            await message.channel.send("{} \n{}".format(title, link))

        if message.content.startswith('list'):
            await message.channel.send("Voici la liste des flux :")
            for flux in list_flux:
                await message.channel.send(f"{flux} : {list_flux[flux]}")
        
        if message.content.startswith('remove'):
            await message.channel.send("Entrez le flux que vous voulez supprimer :")
            flux_remove = await self.wait_for('message', check=lambda message: message.author == message.author)
            flux_remove = int(flux_remove.content)
            await message.channel.send("Vous avez supprimé le flux : {}".format(flux_remove))
            del list_flux[flux_remove]
            await message.channel.send("Veuillez patienter...")
            title, link = feed_parser(flux_remove)
            await message.channel.send("{} \n{}".format(title, link))

        if message.content.startswith('help'):
            await message.channel.send("Voici la liste des commandes :")
            await message.channel.send("rss : affiche la liste des flux")
            await message.channel.send("add : ajoute un flux")
            await message.channel.send("remove : supprime un flux")
            await message.channel.send("list : affiche la liste des flux")
            await message.channel.send("help : affiche la liste des commandes")
            await message.channel.send("ping : pong")
        
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