import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Message
import logging
import asyncio
import datetime

gamemode = ["play", "stream", "listen", "watch"]

date=datetime.datetime.now().strftime("%Y-%m-%d %Hh %Mm %Ss")
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log\\Discord Bot log '+date+'.log', encoding='utf-8', mode='w', delay=None)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(stream_handler)


Client = discord.Client()
bot_prefix= ">"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

@client.event
async def on_ready():
	print("Bot en ligne et prêt!")
	print("Nom: ",client.user.name)
	print("ID: ",client.user.id)
	await client.change_presence(game=discord.Game(name="in v: Alpha Test"))
	print("")

@client.command(pass_context=True)
async def ping(ctx):
	embed = discord.Embed(title="I saw chu!", description="Chu forgot to say \"Pong!\"", color=0x00ff00)
	embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	print("Commande \"Ping\" effectué")
	print("")

@client.command(pass_context=True)
async def game(ctx): #require arg
	if ctx.message.author.id == "178566165206007808":
		Message = ctx.message.content
		Message = Message.split()
		if len(Message) == 1:
			embed = discord.Embed(title="Correct syntax:", description="§game Value Game_Name", color=0xff0000)
			embed.add_field(name="Value", value="""
play
stream
listen
watch
			""", inline=True)
			embed.add_field(name="Game_Name", value="The game name", inline=True)
			embed.set_author(name="Syntax error: "+str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
			return
		if str.casefold(Message[1]) == "help":
			embed = discord.Embed(title="Correct syntax:", description="§game Value Game_Name", color=0xff8000)
			embed.add_field(name="Value", value="""
play
stream
listen
watch
			""", inline=True)
			embed.add_field(name="Game_Name", value="The game name", inline=True)
			embed.set_author(name="Help for: "+str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
			return
		index = 0
		for value in range(0,4):
			index = index+1
			if str.casefold(Message[1]) == gamemode[value]:
				if value == 1:
					await client.change_presence(game=discord.Game(name="{}".format(" ".join(Message[2:])),type=value,url="https://twitch.tv/the10axe"))
				else:
					await client.change_presence(game=discord.Game(name="{}".format(" ".join(Message[2:])),type=value))
				embed = discord.Embed(title="Game change successfully", description="New "+gamemode[value]+": "+"{}".format(" ".join(Message[2:])), color=0x00ff00)
				embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
				await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
				print("Game setted to: ", "{}".format(" ".join(Message[2:])))
				print("")
				return
		if index==4:
			embed = discord.Embed(title="Correct syntax:", description="§game Value Game_Name", color=0xff0000)
			embed.add_field(name="Value", value="""
play
stream
listen
watch
			""", inline=True)
			embed.add_field(name="Game_Name", value="The game name", inline=True)
			embed.set_author(name="Syntax error: "+str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
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
		await client.change_presence(game=discord.Game(name="its end!",type=3))
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		print("Waiting for log out!")
		await client.logout()
		while True:
			if is_closed == True:
				print("Shutting down...")
				logging.shutdown()
				exit()			

	else:
		print(ctx.message.author.id, "tried to set game")
		embed = discord.Embed(title="An error occured", description="You have no right to do that!", color=0xff0000)
		embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		return

@client.command(pass_context=True)
async def parrot(ctx):
	embed = discord.Embed(title=None, description=ctx.message.content[8:], color=0x00ff00)
	embed.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	return
		

client.run(Token)
