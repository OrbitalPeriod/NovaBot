import discord
import commands.submit

prefix = "!"

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

def runBot():
    token = ""
    with open("token") as f:
        token = f.read()
    client.run(token)
