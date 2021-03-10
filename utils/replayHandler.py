import utils.replayParser as replayParser
from utils.replayParser import Player
from utils.replayParser import Team
from utils.sqlManager import getMemberandTeam
import utils.logger as logger

def processReplays(replayList):         #gets team and player data, returns 6* player class and 2* team class
    playerList = []
    teamList = []

    for replay in replayList:                               
        pla, team = replayParser.returnGameStats(replay)
        playerList = playerList + pla
        teamList = teamList + team                      #gets player and team objects from replay parser
                                                        #player.Team not yet set
        
    players = _getPlayerData(playerList)                #returns 6 Player objects, Player.Team set
    teams = sortTeams(teamList)                                 #returns 2 team objects, name not done yet
    del playerList
    del teamList

    if teams[0].GameWins > teams[1].GameWins:           #determine which team won
        teams[0].setSeriesWin()
    else:
        teams[1].setSeriesWin()

    memAndTeam = getMemberandTeam()
    for team in teams:
        for member in team.Members:
            try:
                teamname = memAndTeam[member]
            except:
                continue
            team.Name = teamname[0]
            break


    return players, teams

def _getPlayerData(playerList):             #returns 6 Player objects, Player.Team set
    players = {}
    memberTeamDic = getMemberandTeam()

    for player in playerList:                                                   #create player object for each player
        players[player.Name] = Player()

    for player in playerList:                                                       #combines player stats
        players[player.Name].Name = player.Name
        players[player.Name].Platform = player.Platform
        players[player.Name].Team = player.Team                
                                
        players[player.Name].Goals = player.Goals + players[player.Name].Goals
        players[player.Name].Score = player.Score + players[player.Name].Score
        players[player.Name].Assists = player.Assists + players[player.Name].Assists
        players[player.Name].Saves = player.Saves + players[player.Name].Saves
        players[player.Name].Shots = player.Shots + players[player.Name].Shots
        players[player.Name].Games = player.Games + players[player.Name].Games
        try:
            players[player.Name].Team = memberTeamDic[player.Name][0]
        except:
            pass

    
    return players

def sortTeams(teamList):
    teams = []
    for u in [0, 1]:
        tempTeamlist = teamList.copy()
        teams.append(teamList[0])
        teamList.pop(0)
        popped = 0
        for i in range(1, len(tempTeamlist)):
            similarity = 0
            for member in tempTeamlist[i].Members:
                if member in teams[u].Members:
                    similarity = similarity + 1
            if similarity > 1:
                teams[u].Goals = teams[u].Goals + tempTeamlist[i].Goals
                teams[u].Score = teams[u].Score + tempTeamlist[i].Score
                teams[u].Assists = teams[u].Assists + tempTeamlist[i].Assists
                teams[u].Saves = teams[u].Saves + tempTeamlist[i].Saves
                teams[u].Shots = teams[u].Shots + tempTeamlist[i].Shots
                teams[u].Games = teams[u].Games + tempTeamlist[i].Games
                teams[u].GameWins = teams[u].GameWins + tempTeamlist[i].GameWins
                teams[u].Members = tempTeamlist[u].Members
                teamList.pop(i - popped)
                popped = popped + 1
    return teams
