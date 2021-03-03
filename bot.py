import discord
from discord.ext import commands
import random
from vars import *
from tokens import * # Fill your own token


client = commands.Bot('~', description="hello")


## Extra functionality

# Show invite
@client.command(name="showinvite")
@commands.has_any_role(botMod, "admin")
async def showInvite(context):
	global discordInv
	await context.message.channel.send(discordInv)



###

discordInv = ""

@client.command(name="invite")
@commands.has_any_role(botMod, "admin") #<args>
async def createinvite(context):
	discord_guild = client.get_channel(816343424574685184).guild
	invite = await discord_guild.text_channels[0].create_invite(max_age=0)
	global discordInv
	discordInv = invite.url

	await context.message.channel.send(discordInv)
	

# Boot message
@client.event
async def on_ready():
	general_channel = client.get_channel(816343424574685184)

	myEmbed = discord.Embed(
		title = "Starting...",
		description = "Booted", 
		color = devBlue)

	await general_channel.send(embed = myEmbed)


# Test Embed
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
	await client.process_commands(message)


client.run(token)





