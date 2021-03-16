import discord
import requests
import json
import random
import string
import time
from discord.ext import commands
from vars import *
from validate_email import validate_email
import db


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(
    '~', description="Helper Bot for Devspace 2021", intents=intents)
client.remove_command('help')
env = json.load(open("env.json", "r"))


@client.command(name="invite")
async def showInvite(context):
    await context.message.channel.send(env["invite"])


@client.command(name="cf")
async def coinflip(context):
    await context.message.channel.send(random.choice(["Yes","No"]))

@client.command(name="8ball")
async def eightball(context, *args):
    if not(args):
        myEmbed = discord.Embed(
            title="Idiot",
            description="Send the question",
            color=devBlue)
        await context.message.channel.send(embed=myEmbed)
        return
    question = ' '.join(args)
    answer = requests.get(r"https://8ball.delegator.com/magic/JSON/Heya")
    data = json.loads(answer.text)
    myEmbed = discord.Embed(
        title="Q: "+question,
        description="A: "+data["magic"]["answer"],
        color=devBlue)
    await context.message.channel.send(embed=myEmbed)


@client.event
async def on_ready():
    if not env.get("invite", False):
        discord_guild = client.get_channel(813379544848400384).guild
        invite = await discord_guild.text_channels[0].create_invite(max_age=0, max_uses=0)
        print(invite.url)
        env["invite"] = invite.url
        json.dump(env, open("env.json", "w"), indent=4)
    db.rmvTemp("temp")


@client.command(name="faq")
async def faq(context):
    myEmbed = discord.Embed(
        title="FAQ",
        description="",
        color=devBlue)
    myEmbed.set_image(url=devBanner)
    for _ in FAQ.items():
        myEmbed.add_field(name=_[0], value=_[1], inline=False)
    myEmbed.set_footer(text="End of FAQ section", icon_url=devURL)
    await context.message.channel.send(embed=myEmbed)


@client.command(name="help")
async def help_(context):
    myEmbed = discord.Embed(
        title="Help",
        description="Summary of all available commands",
        color=devBlue)
    myEmbed.set_thumbnail(url=devURL)
    myEmbed.add_field(
        name="~faq", value="Shows Frequently Asked Questions about Devspace", inline=False)
    
    myEmbed.add_field(name="~8ball <question>",
                      value="Ask the real questions of life to the magical 8-Ball!", inline=False)

    myEmbed.add_field(name="~cf <question>",
                      value="Flip a coin!", inline=False)
    
    myEmbed.add_field(
        name="~invite", value="Show invite link for this discord server", inline=False)
    
    myEmbed.set_footer(text="End of Help Section", icon_url=devURL)
    await context.message.channel.send(embed=myEmbed)


@client.event
async def on_message(message):
    if "ooo" == message.content[:3]:
        await message.channel.send("O"*random.randint(8, 30))
        return
    await client.process_commands(message)


def referral_generator():
    ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    if db.checkRefRandom(ref):
        referral_generator()
    else:
        return ref


async def ask_referral(payload):
    await client.get_user(int(payload.user_id)).send("Do you have a referral code? (yes/no)")
    response = await client.wait_for('message', check=lambda message: message.author == client.get_user(int(payload.user_id)) and str(message.channel.type) == 'private')
    if response.content.lower() == 'yes':
        await client.get_user(int(payload.user_id)).send("Please provide your referral code")
        while True:
            ref = await client.wait_for('message', check=lambda message: message.author == client.get_user(int(payload.user_id)) and str(message.channel.type) == 'private')
            if ref.content.lower() == 'no':
                break
            refCheck = db.checkRef(str(ref.content))
            if refCheck[0]:
                await client.get_user(int(refCheck[1])).send("Someone joined using your referral code \nNoice!!")
                break
            else:
                await client.get_user(int(payload.user_id)).send("Incorrect referral code!")
                await client.get_user(int(payload.user_id)).send("Please provide correct Referral code or reply with 'no' to quit!")
    elif response.content.lower() == 'no':
        await client.get_user(int(payload.user_id)).send("Okay")
    else:
        await client.get_user(int(payload.user_id)).send("Incorrect message syntax")
        await ask_referral(payload)

reaction_message_ids = [
    # Referral channel
    '820601793989705758',
    # Shivansh rules
    '813385193406201896'
]
reaction_emojis = ['👍', '✅']

lfg_message_ids = [821293558224519200]
lfg_emojis = ['👍', '✅']
role_id = 821034296579457044

@client.event
async def on_raw_reaction_add(payload):
    main_user = payload.user_id
    message_id = payload.message_id
    
    if(message_id in lfg_message_ids and str(payload.emoji) in lfg_emojis):
        roles = [role.id for role in payload.member.roles]
        if role_id not in roles:
            role = client.get_guild(payload.guild_id).get_role(role_id)
            await payload.member.add_roles(role)
    
    if(db.checkUser(payload.user_id)):
        print("User already present")
        return
    db.addUser("temp", "temp", payload.user_id)
    print(payload.emoji)
    if (str(message_id) in reaction_message_ids) and (str(payload.emoji) in reaction_emojis):
        msgintro = "Hi I'm Spacey The official Devspace bot :)"

        await client.get_user(int(payload.user_id)).send(msgintro + "\nPlease provide your email address registered with hackerearth")
        email = await client.wait_for('message', check=lambda message: message.author == client.get_user(int(payload.user_id)) and str(message.channel.type) == 'private')
        if validate_email(email.content):
            await ask_referral(payload)
            referral = referral_generator()
            await client.get_user(int(payload.user_id)).send("Your referral code is **"+referral+"**")
            await client.get_user(int(payload.user_id)).send("""
Register for Devspace with your friends to create a ton of memories over the weekend. Share the unique code generated above by me and stand to win exciting prizes!
- You can share your token with your friends and ask them to register with it.
- As more people register with your token, the higher are your chances for winning a special prize!""")
            db.removeUser(
                payload.user_id)
            db.addUser(
                email.content, referral, payload.user_id)
        else:
            await client.get_user(int(payload.user_id)).send("Please enter a valid email")
            db.removeUser(payload.user_id)
            await on_raw_reaction_add(payload)

@client.event
async def on_raw_reaction_remove(payload):
    user = payload.user_id
    message_id = payload.message_id
    if(message_id in lfg_message_ids and str(payload.emoji) in lfg_emojis):
        member = client.get_guild(payload.guild_id).get_member(payload.user_id)
        roles = [role.id for role in member.roles]
        if role_id in roles:
            role = client.get_guild(payload.guild_id).get_role(role_id)
            await member.remove_roles(role)

client.run(env["token"])
