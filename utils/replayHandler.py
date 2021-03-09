import utils.replayParser as replayParser
from utils.replayParser import Player
from utils.replayParser import Team
from utils.sqlManager import getMemberandTeam

def processReplays(replayList):         #gets team and player data, returns 6* player class and 2* team class
    playerList = []
    teamList = []

    for replay in replayList:                               
        pla, team = replayParser.returnGameStats(replay)
        playerList = playerList + pla
        teamList = teamList + team
        
        
    players = {}
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

    teams = {0 : Team(0), 1 : Team(1)}
    for team in teamList:                                                               #combines team stats
        teams[team.teamN].Goals = teams[team.teamN].Goals + team.Goals
        teams[team.teamN].Score = teams[team.teamN].Score + team.Score
        teams[team.teamN].Assists = teams[team.teamN].Assists + team.Assists
        teams[team.teamN].Saves = teams[team.teamN].Saves + team.Saves
        teams[team.teamN].Shots = teams[team.teamN].Shots + team.Shots
        teams[team.teamN].Games = teams[team.teamN].Games + team.Games
        teams[team.teamN].GameWins = teams[team.teamN].GameWins + team.GameWins
        teams[team.teamN].Members  = team.Members
    
    memberlist = getMemberandTeam()

    for member in teams[0].Members:
        try:
            team = memberlist[member]
            teams[0].Name = team
            break
        except:
            pass
    
    for member in teams[1].Members:
        try:
            team = memberlist[member]
            teams[1].Name = team
            break
        except:
            pass

    if teams[0].GameWins > teams[1].GameWins:
        teams[0].setSeriesWin()
    else:
        teams[1].setSeriesWin()

    return players, teams
