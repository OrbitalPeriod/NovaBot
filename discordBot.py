import discord
import commands.submit
import commands.ping

prefix = ">"

client = discord.Client()
@client.event
async def on_ready():
    print("Bot online as: {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content == prefix + "submit":
        await commands.submit.submit(message, client)
    elif message.content == prefix + "ping":
        await commands.ping.ping(message, client)

def runBot():
    token = ""
    with open("token") as f:
        token = f.read()
    client.run(token)

def ErrorFound(message):
    pass

