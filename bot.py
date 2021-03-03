import discord, requests, json, random
from discord.ext import commands
from vars import *
from tokens import *


client = commands.Bot('~', description="hello")
env = json.load(open("env.json", "r"))


@client.command(name="invite")
@commands.has_any_role(botMod, "admin")
async def showInvite(context):
	await context.message.channel.send(env["invite"])


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


@client.event
async def on_ready():
	if not env.get("invite", False):
		discord_guild = client.get_channel(816343424574685184).guild
		invite = await discord_guild.text_channels[0].create_invite(max_age=0, max_uses=0)
		print(invite.url)
		env["invite"] = invite.url
		json.dump(env, open("env.json", "w"), indent=4)


@client.command(name="faq")
async def faq(context, *args):
	myEmbed = discord.Embed(
		title = "FAQ",
		description = "", 
		color = devBlue)
	myEmbed.set_image(url = devBanner)
	for _ in FAQ.items():
		myEmbed.add_field(name=_[0], value=_[1], inline=False)
	myEmbed.set_footer(text="End of FAQ section", icon_url=devURL)
	await context.message.channel.send(embed = myEmbed)


@client.event
async def on_message(message):
	if "ooo" == message.content[:3]:
		await message.channel.send("OO"*random.randint(8,30))
		return
	await client.process_commands(message)


client.run(env["token"])
