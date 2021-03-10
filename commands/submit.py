import discord
import utils.replayHandler as replayHandler
from utils.sqlManager import matchMatch
from utils.sqlManager import teamList
import datetime
from utils.logger import logAction
from utils.logger import logError
from utils.sqlManager import discordAndTeam

async def submit(message, client):

    team = await getTeam(message, client)                       #get team variable
    match = await getMatchDetails(team, message, client)        #get details on match using week and team variable
    if match == 0:
        return

    await message.channel.send("Do you wish to submit replays of the match: '{0} Vs {1}'? ['Y'/'N']".format(match[0][1], match[0][2]))
    while True:
        msg = await client.wait_for("message", timeout=30)
        if msg.content.lower() not in ['y', 'n']:
            await message.channel.send("Invalid input")
        else:
            break

    if msg.content.lower() == "n":
        await message.channel.send("OK")
        return

    attachmentlist = await getReplays(message, client)

    if len(attachmentlist) < 2:
        await message.channel.send("Not enough files, exiting operation.")
        logError("NOT ENOUGH FILES FOR SUBMIT BY {0}".format(message.author.name))
        return
    
    players, teams = replayHandler.processReplays(attachmentlist)

    embed = discord.Embed(title="Game statistics: ")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.description = "Please check these game statistics for any errors"
    embed.set_footer(text=message.author.name, icon_url=client.user.avatar_url)
    embed.timestamp = datetime.datetime.now()

    fieldString = ""
    for player in players.values():
        fieldString = fieldString + "**{0}**: Goals: {1}, Platform: {2}, Team: {3}, Score: {4}, Assists: {5}, Saves: {6}, Shots: {7}, Games: {8}\n".format(player.Name, player.Goals, player.Platform, player.Team, player.Score, player.Assists, player.Saves, player.Shots, player.Games)
    
    embed.add_field(name="Player statistics: ", value=fieldString)
    await message.channel.send(embed=embed)

    pass

async def getReplays(message, client):
    def check(msg):
        return msg.author == message.author and msg.channel == message.channel or msg.content.lower() == "-e"

    attachments = []

    for numeration in ["first", "second", "third", "fourth", "firth", "sixth", "severth"]:
        await message.channel.send("send in your {0} replay. (use -e to confirm all replays have been send in)".format(numeration))
        while True:
            msg = await client.wait_for("message", timeout=60, check=check)
            if msg.content == "-e":
                return attachments
            elif len(msg.attachments) != 1:
                await message.channel.send("Invalid file input")
                continue
            else:
                break
        attachments.append(msg.attachments[0].url)

async def getMatchDetails(team, message, client):     #id, teamhome, teamaway, bestOustOf    
    weeklist = ["week 1", "week 2", "week 3", "week 4", "week 5", "week 6", "week 7", "week 8", "week 9","week 10" ,"week 11" ,"week 12", "week 13"]

    await message.channel.send("What week was this match supposed to be played it? (for example, 'week 1')")
    while True:
        msg = await client.wait_for("message", timeout = 60)
        if not (message.channel == msg.channel and message.author == msg.author):
            continue
        elif msg.content.lower() not in weeklist:
            await message.channel.send("Invalid team name")
            continue
        else:
            week = msg.content
            break
    
    match = matchMatch(team, week)      #id, teamhome, teamaway, bestOustOf
    if len(match) == 0:
        await message.channel.send("Match not found, contact an administrator")
        await logError("Match by {0} in week {1}".format(team, week))
        return 0
    return match

async def getTeam(message, client):
    teams = teamList()
    potTeam = discordAndTeam(message.author.id)
    if potTeam != None:
        return potTeam

    await message.channel.send("What team do you represent?")
    while True:
        msg = await client.wait_for("message", timeout = 60)
        if not (message.channel == msg.channel and message.author == msg.author):
            continue
        elif msg.content not in teams:
            await message.channel.send("Invalid team name")
            continue
        else:
            team = msg.content
            break
    return team