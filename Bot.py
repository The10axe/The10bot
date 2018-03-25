import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Message
import logging
import asyncio
import datetime

date=datetime.datetime.now().strftime("%d-%m-%Y %Hh %Mm %Ss")
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='Discord Bot log '+date+'.log', encoding='utf-8', mode='w', delay=None)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
handler.setLevel(logging.INFO)
logger.addHandler(handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


Client = discord.Client()
bot_prefix= "§"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

@client.event
async def on_ready():
	print("Bot en ligne et prêt!")
	print("Nom: ",client.user.name)
	print("ID: ",client.user.id)
	await client.change_presence(game=discord.Game(name="in v: 2.0.0"))
	print("")

@client.command(pass_context=True)
async def ping(ctx):
	embed = discord.Embed(title="I saw chu!", description="Chu forgot to say \"Pong!\"", color=0x00ff00)
	embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
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
			embed = discord.Embed(title="Game change successfully", description="New game: "+Message, color=0x00ff00)
			embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
			print("Game setted to: ", Message)
			print("")
			return
		else:
			print(ctx.message.author.id, "tried to set game")
			embed = discord.Embed(title="An error occured", description="You have no right to do that!", color=0xff0000)
			embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
			return
			
@client.command(pass_context=True)
async def stop(ctx):
	if ctx.message.author.id == "178566165206007808":
		embed = discord.Embed(title="Good bye!", description="Stopping bot!", color=0x00ff00)
		embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		print("Stopping!")
		logging.shutdown()
		exit()
	else:
		print(ctx.message.author.id, "tried to set game")
		embed = discord.Embed(title="An error occured", description="You have no right to do that!", color=0xff0000)
		embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		return
		

client.run("Your Token")
