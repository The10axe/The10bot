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

@client.async_event
async def on_ready():
	print("Bot en ligne et prêt!")
	print("Nom: ",client.user.name)
	print("ID: ",client.user.id)
	await client.change_presence(game=discord.Game(name="in v: Github Release"))
	print("")
	
@client.command(pass_context=True)
async def help(ctx):
	if ctx.message.author.id != "178566165206007808":
		embed = discord.Embed(title="Help", description="Use `>` to use commands: \n", color=0x00ff00)
	if ctx.message.author.id == "178566165206007808":
		embed = discord.Embed(title="Bot Admin Help", description="Use `>` to use commands: \n", color=0x00ff00)
	# embed.add_field(name="\n", value="\n", inline=False)
	embed.add_field(name="help", value="Let me help you, and teach you how to use me, you lewdy!", inline=False)
	embed.add_field(name="ping", value="See by yourself how we play pong!", inline=False)
	embed.add_field(name="parrot #MESSAGE", value="Let me be your parrot!", inline=False)
	embed.add_field(name="me", value="Lets see some info about chu, I got 'em from some detective~", inline=False)
	embed.add_field(name="info #?@SOMEONE", value="Get some info about me, or spy chur friends info!", inline=False)
	if ctx.message.author.id == "178566165206007808":
		embed.add_field(name="game #help|VALUE #?game", value="Change the game displayed", inline=False)
		embed.add_field(name="stop", value="Will chu really kill me ;_;", inline=False)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	
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

@client.command(pass_context=True)
async def me(ctx):
	if ctx.message.server == None:
		embed = discord.Embed(title="Info about you", description=None, color=0x000000)
	else:
		embed = discord.Embed(title="Info about you", description=None, color=ctx.message.author.color)
	embed.add_field(name="User:", value=str(ctx.message.author)+" ("+str(ctx.message.author.id)+")", inline=False)
	embed.add_field(name="Created the:", value=str(ctx.message.author.created_at)[0:-7], inline=False)
	embed.set_image(url=ctx.message.author.avatar_url)
	if ctx.message.server != None:
		embed.add_field(name="Top role in this server:",value=str(ctx.message.author.top_role), inline=False)
		embed.add_field(name="Display name:", value=str(ctx.message.author.display_name), inline=False)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	
@client.command(pass_context=True)
async def info(ctx):
	mentions = ctx.message.mentions
	if len(mentions) == 1:
		mentions = mentions[0]
		if ctx.message.server != None:
			embed = discord.Embed(title="Info about "+str(mentions), description=None, color=mentions.color)
			embed.add_field(name="User:", value=str(mentions)+" ("+str(mentions.id)+")", inline=False)
			embed.add_field(name="Created the:", value=str(mentions.created_at)[0:-7], inline=False)
			embed.set_image(url=mentions.avatar_url)
			embed.add_field(name="Top role in this server:",value=str(mentions.top_role), inline=False)
			embed.add_field(name="Display name:", value=str(mentions.display_name), inline=False)
	if len(mentions) == 0:
		embed = discord.Embed(title="Info about myself (Click to add me)", description=None, color=0x000000, url="https://discordapp.com/oauth2/authorize?client_id=426478004298842113&permissions=2146958583&scope=bot")
		embed.add_field(name="User:", value=str(client.user)+" ("+str(client.user.id)+")", inline=False)
		embed.add_field(name="Created the:", value=str(client.user.created_at)[0:-7], inline=False)
		embed.add_field(name="Looking at",value=str(len(client.servers))+" servers", inline=False)
		embed.set_image(url=client.user.avatar_url)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		

client.run(Token)
