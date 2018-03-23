import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Message
import logging
import asyncio

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord###.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

Client = discord.Client()
bot_prefix= "§"
client = commands.Bot(command_prefix=bot_prefix)
@client.event
async def on_ready():
	print("Bot en ligne et prêt!")
	print("Nom: ",client.user.name)
	print("ID: ",client.user.id)
	await client.change_presence(game=discord.Game(name="in v: 1.0.0"))
	print("")

@client.command(pass_context=True)
async def ping(ctx):
	await client.say("I saw chu! Chu forgot to say \"Pong\"!")
	print("Commande \"Ping\" effectué")
	print("")

@client.command(pass_context=True)
async def game(ctx, *, Message : str):
	if Message == None:
		return
	else:
		if ctx.message.author.id == "178566165206007808":
			await client.change_presence(game=discord.Game(name=Message))
			await client.say("Game changed with success!")
			print("Game setted to: ", Message)
			print("")
			return
		else:
			print(ctx.message.author.id, "tried to set game")
			await client.say("You have no right to do that!")
			return
		

client.run("You'll never know HAHA!!!!")
