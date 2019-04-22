#!/usr/bin/python
# -*- encoding: UTF-8 -*-
import logging
import asyncio
import datetime
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Message
from discord.utils import get
import random

ingame = False
nombre = -1
essai = 0
min = 0
max = 10000

message_pfc = None
joueur = []
action = []
host = None

owner = []
with open('./settings/owner.data') as file:
    owner = file.readlines()
a = 0
for i in owner:
	owner[a] = i.rstrip()
	a = a+1
print("Owner ID: "+str(owner))
file.close()

admin = []
with open('./settings/admin.data') as file:
    admin = file.readlines()
a = 0
for i in admin:
	admin[a] = i.rstrip()
	a = a+1
admin = admin + owner
print("Admin ID: "+str(admin))
file.close()

print()

gamemode = ["play", "stream", "listen", "watch"]

date=datetime.datetime.now().strftime("%Y-%m-%d %Hh %Mm %Ss")
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='./log/Discord Bot log '+date+'.log', encoding='utf-8', mode='w', delay=None)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
handler.setLevel(logging.INFO)
logger.addHandler(handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(stream_handler)


Client = discord.Client()
bot_prefix= ">"
client = commands.Bot(command_prefix=bot_prefix)
client.remove_command("help")

@client.async_event
async def on_reaction_add(reaction,user):
	if str(user.id) != "426478004298842113":
		global message_pfc
		global joueur
		global action
		global host
		if message_pfc != None and reaction.message.id == message_pfc.id:
			if reaction.emoji == "✅":
				if len(joueur) <= 2:
					joueur.append(user)
					await client.send_message(user,content="Vous êtes prêt!",tts=False,embed=None)
				if len(joueur) == 2:
					if joueur[0].id > joueur[1].id:
						buffer = joueur[1]
						joueur[1] = joueur[0]
						joueur[0] = buffer
					await client.send_message(host.channel, content="La partie a démarré:\n<@"+str(joueur[0].id)+"> VS <@"+str(joueur[1].id)+">",tts=False,embed=None)
					action = [-1,-1]
					for i in joueur:
						autre_joueur = None
						for z in joueur:
							if z != i:
								autre_joueur = z
						message = await client.send_message(i, content="Vous jouer contre "+str(autre_joueur)+" (Réagissez pour jouer):",tts=False,embed=None)
						scheme = ['✊','🖐','✌']
						for z in scheme:
							await client.add_reaction(message, z)
			elif reaction.emoji == "❌" and host != message_pfc:
				await client.send_message(host.channel, content="Le joueur a refuser le défi!",tts=False,embed=None)
				await client.send_message(message_pfc.channel, content="Vous avez refuser le défi!",tts=False,embed=None)
				message_pfc = None
				joueur = []
				action = []
				host = None
		elif user in joueur:
			if reaction.emoji == "✊": # 1
				action[joueur.index(user)] = 1
			elif reaction.emoji == "🖐": # 2
				action[joueur.index(user)] = 2
			elif reaction.emoji == "✌": # 3
				action[joueur.index(user)] = 3
			if action.count(-1) == 0:
				if action[0] == action[1]:
					status = "C'est une égalité!"
				elif action[0] == 3 and action[1] == 1:
					status = "<@"+str(joueur[1].id)+"> a gagné!"
				elif action[1] == 3 and action[0] == 1:
					status = "<@"+str(joueur[0].id)+"> a gagné!"
				elif action[0] > action[1]:
					status = "<@"+str(joueur[0].id)+"> a gagné!"
				elif action[1] > action[0]:
					status = "<@"+str(joueur[1].id)+"> a gagné!"
				a = 0
				for i in action:
					if i == 1:
						action[a] = "✊"
					elif i == 2:
						action[a] = "🖐"
					elif i == 3:
						action[a] = "✌"
					a = a + 1
				coucou = await client.send_message(host.channel, content="Voici la partie:\n<@"+str(joueur[0].id)+"> : "+str(action[0])+" VS "+str(action[1])+" : <@"+str(joueur[1].id)+">\n"+status,tts=False,embed=None)
				await client.add_reaction(coucou, "👏")
				await client.add_reaction(coucou, "👍")
				message_pfc = None
				joueur = []
				action = []
				host = None
			

@client.async_event
async def on_reaction_remove(reaction,user):
	global joueur
	if user in joueur:
		if reaction.emoji == "✅":
			joueur.remove(user)
			await client.send_message(user,content="Vous n'êtes plus prêt!",tts=False,embed=None)
			

@client.async_event
async def on_ready():
	print()
	print("Bot en ligne et prêt!")
	print("Nom: ",client.user.name)
	print("ID: ",client.user.id)
	await client.change_presence(game=discord.Game(name="in v: Alpha 1.0"))
	print()

print()
	
@client.command(pass_context=True)
async def help(ctx):
	global admin
	global owner
	if str(ctx.message.author.id) in owner:
		embed = discord.Embed(title="Bot Owner Help", description="Use `>` to use commands: \n", color=0x00ff00)
	elif str(ctx.message.author.id) in admin:
		embed = discord.Embed(title="Bot Admin Help", description="Use `>` to use commands: \n", color=0x00ff00)
	else:
		embed = discord.Embed(title="Help", description="Use `>` to use commands: \n", color=0x00ff00)
	# embed.add_field(name="\n", value="\n", inline=False)
	embed.add_field(name="help", value="Let me help you, and teach you how to use me, you lewdy!", inline=False)
	embed.add_field(name="ping", value="See by yourself how we play pong!", inline=False)
	embed.add_field(name="parrot #MESSAGE", value="Let me be your parrot!", inline=False)
	embed.add_field(name="me", value="Lets see some info about chu, I got 'em from some detective~", inline=False)
	embed.add_field(name="info #?@SOMEONE", value="Get some info about me, or spy chur friends info!", inline=False)
	if ctx.message.author.id in admin:
		embed.add_field(name="Beta Feature: guess", value="start | number | reset. Please signal error to bot owner", inline=False)
	else:
		embed.add_field(name="Beta Feature: guess", value="start | number. Please signal error to bot owner", inline=False)
	if ctx.message.author.id in owner:
		embed.add_field(name="game #help|VALUE #?game", value="Change the game displayed", inline=False)
		embed.add_field(name="stop", value="Will chu really kill me ;_;", inline=False)
	embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
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
	global owner
	if str(ctx.message.author.id) in owner:
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
			embed.set_author(name="Syntax error", icon_url="")
			embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
			return
		if str.casefold(Message[1]) == "help":
			embed = discord.Embed(title="Correct syntax:", description=">game Value Game_Name", color=0xff8000)
			embed.add_field(name="Value", value="""
play
stream
listen
watch
			""", inline=True)
			embed.add_field(name="Game_Name", value="The game name", inline=True)
			embed.set_author(name="Help", icon_url="")
			embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
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
				embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
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
			embed.set_author(name="Syntax error", icon_url="")
			embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
			await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	else:
		print(ctx.message.author.id, "tried to set game")
		embed = discord.Embed(title="An error occured", description="You have no right to do that!", color=0xff0000)
		embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		return
			
@client.command(pass_context=True)
async def stop(ctx):
	global owner
	if str(ctx.message.author.id) in owner:
		embed = discord.Embed(title="Good bye!", description="Stopping bot!", color=0x00ff00)
		embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
		await client.change_presence(game=discord.Game(name="its end!",type=3))
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		print("Waiting for log out!")
		await client.logout()
		print("Shutting down...")
		logging.shutdown()
		exit()			

	else:
		print(ctx.message.author.id, "tried to stop the bot")
		embed = discord.Embed(title="An error occured", description="You have no right to do that!", color=0xff0000)
		embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		return

@client.command(pass_context=True)
async def parrot(ctx):
	embed = discord.Embed(title=None, description=ctx.message.content[8:], color=0x00ff00)
	embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
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
	if str(ctx.message.author.id) in owner:
		embed.add_field(name="Is bot owner:", value="Yes", inline=False)
	elif str(ctx.message.author.id) in admin:
		embed.add_field(name="Is bot admin:", value="Yes", inline=False)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	
@client.command(pass_context=True)
async def info(ctx):
	global admin
	global owner
	mentions = ctx.message.mentions
	if len(mentions) == 0:
		embed = discord.Embed(title="Info about myself (Click to add me)", description=None, color=0x000000, url="https://discordapp.com/api/oauth2/authorize?client_id=426478004298842113&permissions=67360832&redirect_uri=http%3A%2F%2Fdiscordapp.com%2F&scope=bot")
		embed.add_field(name="User:", value=str(client.user)+" ("+str(client.user.id)+")", inline=False)
		embed.add_field(name="Created the:", value=str(client.user.created_at)[0:-7], inline=False)
		embed.add_field(name="Looking at",value=str(len(client.servers))+" servers", inline=False)
		embed.set_image(url=client.user.avatar_url)
	else:
		mentions = mentions[0]
		if ctx.message.server != None:
			embed = discord.Embed(title="Info about "+str(mentions), description=None, color=mentions.color)
			embed.add_field(name="User:", value=str(mentions)+" ("+str(mentions.id)+")", inline=False)
			embed.add_field(name="Created the:", value=str(mentions.created_at)[0:-7], inline=False)
			embed.set_image(url=mentions.avatar_url)
			embed.add_field(name="Top role in this server:",value=str(mentions.top_role), inline=False)
			embed.add_field(name="Display name:", value=str(mentions.display_name), inline=False)
			if str(mentions.id) in owner:
				embed.add_field(name="Is bot owner:", value="Yes", inline=False)
			elif str(mentions.id) in admin:
				embed.add_field(name="Is bot admin:", value="Yes", inline=False)
	embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
		
@client.command(pass_context=True)
async def guess(ctx, word):
	global ingame
	global nombre
	global essai
	global min
	global max
	global admin
	if word.lower() == "start":
		if ingame == False:
			nombre = random.randint(0,10000)
			essai = 0
			min = 0
			max = 10000
			embed = discord.Embed(title="The right price", description="A game has started", color=0x000000)
			embed.add_field(name="Ongoing game:", value=str(min)+" < ? < "+str(max), inline=False)
			embed.add_field(name="Number of try:",value=str(essai), inline=False)
			ingame = True
		elif ingame == True:
			embed = discord.Embed(title="The right price", description="The game is already started", color=0x000000)
			embed.add_field(name="Ongoing game:", value=str(min)+" < ? < "+str(max), inline=False)
			embed.add_field(name="Number of try:",value=str(essai), inline=False)
	elif word.lower() == "reset":
		if str(ctx.message.author.id) in admin:
			ingame = False
			nombre = -1
			essai = 0
			min = 0
			max = 10000
			embed = discord.Embed(title="The right price", description="Reseted game!", color=0xffff00)
		else:
			embed = discord.Embed(title="The right price", description="You have no right to do this!", color=0xff0000)
	elif ingame == True:
		word = int(word)
		if word == nombre:
			essai = essai + 1
			embed = discord.Embed(title="The right price", description="Victory!", color=0xffc200)
			embed.add_field(name="The value was:", value="0 < "+str(nombre)+" < 10000", inline=False)
			embed.add_field(name="Number of try:",value=str(essai), inline=False)
			ingame = False
		elif word > nombre:
			if word < max:
				max = word
				essai = essai + 1
			embed = discord.Embed(title="The right price", description="", color=0x00ff10)
			embed.add_field(name="Ongoing game:", value=str(min)+" < ? < "+str(max), inline=False)
			embed.add_field(name="Number of try:",value=str(essai), inline=False)
		elif word < nombre:
			if word > min:
				min = word
				essai = essai + 1
			embed = discord.Embed(title="The right price", description="", color=0x00ff10)
			embed.add_field(name="Ongoing game:", value=str(min)+" < ? < "+str(max), inline=False)
			embed.add_field(name="Number of try:",value=str(essai), inline=False)
		else:
			embed = discord.Embed(title="The right price", description="An error occured", color=0x000000)
			embed.add_field(name="Ongoing game:", value=str(min)+" < ? < "+str(max), inline=False)
			embed.add_field(name="Number of try:",value=str(essai), inline=False)
	elif ingame == False:
		if nombre == -1:
			embed = discord.Embed(title="The right price", description="No game is started", color=0x000000)
		else:
			embed = discord.Embed(title="The right price", description="No game is started", color=0x000000)
			embed.add_field(name="Last game:", value="0 < "+str(nombre)+" < 10000", inline=False)
			embed.add_field(name="Number of try:",value=str(essai), inline=False)
	else:
		embed = discord.Embed(title="The right price", description="An error occured", color=0x000000)
	embed.set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
	await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)

@client.command(pass_context=True)
async def sncf(ctx):
	if ctx.message.author.voice_channel != None and client.is_voice_connected(ctx.message.server) != True:
		cc = client.get_channel(ctx.message.author.voice_channel.id)
		vc = await client.join_voice_channel(cc)
		player = vc.create_ffmpeg_player('./sound/SNCF.mp3', after=None)
		player.start()
		while not player.is_done():
			await asyncio.sleep(1)
		player.stop()
		await vc.disconnect()
		minutes = random.randint(5,360)
		if minutes < 60:
			messagea = "Le train TER n°"+str(random.randint(1000,999999))+" accuse un retard de "+str(minutes)+" minutes!"
		else:
			heures = 0
			while minutes > 59:
				heures = heures + 1
				minutes = minutes - 60
			if heures == 1:
				heure = "1 heure"
			else:
				heure = str(heures)+" heures"
			if minutes < 2:
				minute = str(minutes)+" minute"
			else:
				minute = str(minutes)+" minutes"
			messagea = "Le train TER n°"+str(random.randint(1000,999999))+" accuse un retard de "+heure+" et "+minute+"!"
		embed = discord.Embed(title="SNCF", description=messagea,color=0x000000)
		embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Logo_TER.svg/1920px-Logo_TER.svg.png")
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	elif ctx.message.author.voice_channel == None:
		minutes = random.randint(5,360)
		if minutes < 60:
			messagea = "Le train TER n°"+str(random.randint(1000,999999))+" accuse un retard de "+str(minutes)+" minutes!"
		else:
			heures = 0
			while minutes > 59:
				heures = heures + 1
				minutes = minutes - 60
			if heures == 1:
				heure = "1 heure"
			else:
				heure = str(heures)+" heures"
			if minutes < 2:
				minute = str(minutes)+" minute"
			else:
				minute = str(minutes)+" minutes"
			messagea = "Le train TER n°"+str(random.randint(1000,999999))+" accuse un retard de "+heure+" et "+minute+"!"
		embed = discord.Embed(title="SNCF", description=messagea,color=0x000000)
		embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Logo_TER.svg/1920px-Logo_TER.svg.png")
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)

@client.command(pass_context=True)
async def reload(ctx):
	global owner
	global admin
	if str(ctx.message.author.id) in owner:
		embed = discord.Embed(title="Reload", description=None,color=0x00ff00)
		owner = []
		with open('./settings/owner.data') as file:
			owner = file.readlines()
		a = 0
		for i in owner:
			owner[a] = i.rstrip()
			a = a+1
		print("Reloaded Owner ID: "+str(owner))
		embed.add_field(name="Owner:", value=str(owner), inline=False)
		file.close()
		admin = []
		with open('./settings/admin.data') as file:
			admin = file.readlines()
		a = 0
		for i in admin:
			admin[a] = i.rstrip()
			a = a+1
		admin = admin + owner
		print("Reloaded Admin ID: "+str(admin))
		embed.add_field(name="Admin:", value=str(admin), inline=False)
		file.close()
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)
	else:
		embed = discord.Embed(title="Reload", description="You have no right to do this!",color=0xFF0000)
		await client.send_message(ctx.message.channel,content=None,tts=False,embed=embed)

@client.command(pass_context=True)
async def pfc(ctx):
	global message_pfc
	global joueur
	global host
	global action
	joueur = []
	action = []
	host = None
	mentions = ctx.message.mentions
	if len(mentions) == 0:
		host = await client.send_message(ctx.message.channel,content="Clicker sur la coche ci-dessous pour jouer au Pierre Feuille Ciseaux",tts=False,embed=None)
		message_pfc = host
	else:
		mentions = mentions[0]
		if mentions != ctx.message.author:
			host = await client.send_message(ctx.message.channel,content="<@"+str(ctx.message.author.id)+"> a défier <@"+str(mentions.id)+"> au Pierre Feuille Ciseaux",tts=False,embed=None)
			message_pfc = await client.send_message(mentions,content="<@"+str(ctx.message.author.id)+'> vous a défier au Pierre Feuille Ciseaux sur le serveur "'+str(ctx.message.server)+'" dans le channel: #'+str(ctx.message.channel),tts=False,embed=None)
			joueur.append(ctx.message.author)
			await client.send_message(ctx.message.author,content="Vous êtes prêt!",tts=False,embed=None)
			await client.add_reaction(message_pfc, "❌")
	await client.add_reaction(message_pfc, '✅')
		
file = open("./settings/token.id", "r")
Token = file.readline()
file.close()
print("Token: "+str(Token))
print()
client.run(Token)