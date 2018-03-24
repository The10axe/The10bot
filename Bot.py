import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Message
import logging
import asyncio
import datetime


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
date=datetime.datetime.now().strftime("%d-%m-%Y %Hh %Mm %Ss")
handler = logging.FileHandler(filename="Log\\Bot "+date+".log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

Client = discord.Client()
bot_prefix= "§"
client = commands.Bot(command_prefix=bot_prefix)
@client.event
async def on_ready():
	print("Bot online and ready!")
	print("Nom: ",client.user.name)
	print("ID: ",client.user.id)
	await client.change_presence(game=discord.Game(name="in v: 2.0.0"))
	print("")

@client.command(pass_context=True)
async def ping(ctx):
	embed = discord.Embed(title="I saw chu!", description="Chu forgot to say \"Pong!\"", color=0x00ff00)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	print("Commande \"Ping\" effectué")
	print("")

@client.command(pass_context=True)
async def game(ctx, *, Message : str):
	if Message == None:
		return
	else:
		if ctx.message.author.id == "178566165206007808":
			await client.change_presence(game=discord.Game(name=Message))
			embed = discord.Embed(title="User: "+ctx.message.author.id, description="Game changed with success!", color=0x00ff00)
			embed.add_field(name="New game", value=Message, inline=False)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
			print("Game setted to: ", Message)
			print("")
			return
		else:
			print(ctx.message.author.id, "tried to set game")
			embed = discord.Embed(title="An error occured", description="You have no right to do that!", color=0xff0000)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
			return
			
@client.command(pass_context=True)
async def stop(ctx):
	if ctx.message.author.id == "178566165206007808":
		embed = discord.Embed(title="Good bye!", description="Stopping bot!", color=0x00ff00)
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		print("Stopping!")
		exit()
		return
	else:
		print(ctx.message.author.id, "tried to set game")
		embed = discord.Embed(title="An error occured", description="You have no right to do that!", color=0xff0000)
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		return
		

client.run("Your Discord Bot token here")
