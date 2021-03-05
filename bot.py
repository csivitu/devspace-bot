import discord, requests, json, random, string
from discord.ext import commands
from vars import *
import db


intents = discord.Intents.default()
intents.members = True
client = commands.Bot('~', description="Helper Bot for Devspace 2021", intents = intents)
client.remove_command('help')
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
	myEmbed = discord.Embed(
		title = "Q: "+question,
		description = "A: "+data["magic"]["answer"],
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
	print("Bot is ready for use")

@client.command(name="faq")
async def faq(context):
	myEmbed = discord.Embed(
		title = "FAQ",
		description = "", 
		color = devBlue)
	myEmbed.set_image(url = devBanner)
	for _ in FAQ.items():
		myEmbed.add_field(name=_[0], value=_[1], inline=False)
	myEmbed.set_footer(text="End of FAQ section", icon_url=devURL)
	await context.message.channel.send(embed = myEmbed)

@client.command(name="help")
async def help_(context):
	myEmbed = discord.Embed(
		title = "Help",
		description = "Summary of all available commands", 
		color = devBlue)
	myEmbed.set_thumbnail(url = devURL)
	myEmbed.add_field(name="~faq", value="Shows Frequently Asked Questions about Devspace", inline=False)
	myEmbed.add_field(name="~8ball <question>", value="Ask the real questions of life to the magical 8-Ball!", inline=False)
	myEmbed.add_field(name="~invite", value="Show invite link for this discord server → Admin Command", inline=False)
	myEmbed.set_footer(text="End of Help Section", icon_url=devURL)
	await context.message.channel.send(embed = myEmbed)

@client.event
async def on_message(message):
	if "ooo" == message.content[:3]:
		await message.channel.send("O"*random.randint(8,30))
		return
	await client.process_commands(message)

def referral_generator():
	ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 15))
	if db.checkRefRandom(ref):
		referral_generator()
	else:
		return ref

reaction_message_id = '817278322559680543'
reaction_emoji = '👍'

@client.event
async def on_raw_reaction_add(payload):
	print("1")
	main_user = payload.user_id
	message_id = payload.message_id
	print(main_user, message_id, payload.emoji)
	#checks if the user is present in the database
	if(db.checkUser(main_user)):
		print("User already present")
		return
	#check if the message id and reaction emoji match
	if str(message_id) == reaction_message_id and str(payload.emoji) == reaction_emoji:
		print(2)
		while True:
			#Send DM asking if the user has a referral code or not
			await client.get_user(int(payload.user_id)).send("Do you have a referral code? (yes/no)")
			#Accept the response from the user
			response = await client.wait_for('message') #TODO: add check as the second parameter
			print(response.content)
			#Checks if the response's content is yes or no
			if response.content.lower() == 'yes':
				#Takes the referral code until the correct referral is given or 'no' is entered
				await client.get_user(int(payload.user_id)).send("Please provide your referral code")
				while True:
					ref = await client.wait_for('message')
					print(ref.content)
					if ref.content.lower() == 'no':
						break
					if db.checkRef(str(ref.content)):
						break
					else:
						await client.get_user(int(payload.user_id)).send("Incorrect referral code!")
						await client.get_user(int(payload.user_id)).send("Please provide correct Referral code or reply with 'no' to quit!")
				break
			elif response.content.lower() == 'no':
				await client.get_user(int(payload.user_id)).send("Okay")
				break
			else:
				await client.get_user(int(payload.user_id)).send("Incorrect message syntax")
		while True:
			#Ask for referral competition
			await client.get_user(int(payload.user_id)).send("Do you want to take part in referral competition?")
			response = await client.wait_for('message')
			if response.content.lower() == 'yes':
				#Takes email address
				await client.get_user(int(payload.user_id)).send("Please provide your email address")
				email = await client.wait_for('message')
				print(email.content)
				#Generates referral code
				referral = referral_generator()
				#Send the referral code
				await client.get_user(int(payload.user_id)).send("Your referral code is " + referral)
				await client.get_user(int(payload.user_id)).send("Thank you for your time")
				#Adds the user email address, referral code and user id to database
				db.addUser(email.content, referral, main_user)
				break
			elif response.content.lower() == 'no':
				await client.get_user(int(payload.user_id)).send("Thank you for your time")
				break
			else:
				await client.get_user(int(payload.user_id)).send("Incorrect message syntax")

#TO-DO: Prevent multiple reacts


client.run(env["token"])
