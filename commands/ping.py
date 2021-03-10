import discord
import datetime
from utils.replayParser import Player

async def ping(message, client):

    embed = discord.Embed(title="Game statistics: ")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.description = "Please check these game statistics for any errors"
    embed.set_footer(text=message.author.name, icon_url=client.user.avatar_url)
    embed.timestamp = datetime.datetime.now()
    embed.add_field(name="Player statistics: ", value="**PlayerName**, goals, assists, saves, score\n**PlayerName**, goals, assists, saves, score")

    await message.channel.send(embed=embed)

    pass