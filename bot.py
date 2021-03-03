import discord
from discord.ext import commands
import random
from vars import *
from tokens import * # Fill your own token
import requests
import json


client = commands.Bot('~', description="hello")



discordInv = ""

@client.command(name="invite")
@commands.has_any_role(botMod, "admin") #<args>
async def createinvite(context):
	discord_guild = client.get_channel(816343424574685184).guild
	invite = await discord_guild.text_channels[0].create_invite(max_age=0)
	global discordInv
	discordInv = invite.url

	await context.message.channel.send(discordInv)


# Show invite
@client.command(name="showinvite")
@commands.has_any_role(botMod, "admin")
async def showInvite(context):
	global discordInv
	await context.message.channel.send(discordInv)


# 8 Ball
@client.command(name="8ball")
async def eightball(context, *args):
	if not(args):
		myEmbed = discord.Embed(
		title = "Idiot",
		description = "Send the question", 
		color = devBlue)
		await context.message.channel.send(embed = myEmbed)
		return
	question = ' '.join(args)	
	answer = requests.get(r"https://8ball.delegator.com/magic/JSON/Heya")
	data = json.loads(answer.text)
	print(data)
	myEmbed = discord.Embed(
		title = question,
		description = data["magic"]["answer"],
		color = devBlue)
	await context.message.channel.send(embed = myEmbed)


# Boot message
@client.event
async def on_ready():
	general_channel = client.get_channel(816343424574685184)

	myEmbed = discord.Embed(
		title = "Starting...",
		description = "Booted", 
		color = devBlue)

	await general_channel.send(embed = myEmbed)
	

# Show faq
@client.command(name="faq")
async def version(context, *args):
	myEmbed = discord.Embed(
		title = "FAQ",
		description = "", 
		color = devBlue)

	myEmbed.set_image(url = devBanner)
	#myEmbed.set_thumbnail(url = devURL)

	for _ in FAQ.items():
		myEmbed.add_field(name=_[0], value=_[1], inline=False)

	myEmbed.set_footer(text="End of FAQ section", icon_url=devURL)

	await context.message.channel.send(embed = myEmbed)


# Run commands
@client.event
async def on_message(message):
	if "ooo" == message.content[:3]:
		await message.channel.send("OO"*random.randint(8,30))
		return
	await client.process_commands(message)


client.run(token)





