import json, subprocess, os


jsonfile = "output.json"
rattletrapLocation = "./utils/rattletrap"

def createJson(file):
    os.system(f"{rattletrapLocation} -i {file} -o {jsonfile} -f")
    return

def returnGameStats(replayfile):
    createJson(replayfile)
    gameData = {}
    with open(jsonfile) as f:
        gameData = json.loads(f.read())
    playersJSON = gameData["header"]["body"]["properties"]["value"]["PlayerStats"]["value"]["array"]
    
    playerList = []
    for playerJSON in playersJSON:
        player = Player()
        player.fromJson(playerJSON)
        playerList.append(player)

    teamList = [Team(0), Team(1)]
    for player in playerList:
        team = ""
        if player.Team == 0:
            team = teamList[0]
        elif player.Team == 1:
            team = teamList[1]
        else:
            continue
        team.Goals = team.Goals + player.Goals
        team.Score = team.Score + player.Score
        team.Assists = team.Assists + player.Assists
        team.Saves = team.Saves + player.Saves
        team.Shots = team.Shots + player.Shots
        team.Members.append(player.Name)
        team.Games = 1
    
    if teamList[0].Goals > teamList[1].Goals:
        teamList[0].setGameWin()
    else:
        teamList[1].setGameWin()

    return playerList, teamList
        
class Player:
    def __init__(self):
        self.Name = ""
        self.Goals = 0
        self.Platform = ""
        self.Team = -1
        self.Score = 0
        self.Assists = 0
        self.Saves = 0
        self.Shots = 0
        self.Games = 0
    def fromJson(self, jsonDic):
        self.Name = jsonDic["value"]["Name"]["value"]["str"]
        self.Goals = jsonDic["value"]["Goals"]["value"]["int"]
        self.Platform = jsonDic["value"]["Platform"]["value"]["byte"][1]
        self.Team = jsonDic["value"]["Team"]["value"]["int"]
        self.Score = jsonDic["value"]["Score"]["value"]["int"]
        self.Assists = jsonDic["value"]["Assists"]["value"]["int"]
        self.Saves = jsonDic["value"]["Assists"]["value"]["int"]
        self.Shots = jsonDic["value"]["Shots"]["value"]["int"]
        self.Games = 1

class Team:
    def __init__(self, intn):
        self.teamN = intn
        self.Goals = 0
        self.Score = 0
        self.Assists = 0
        self.Saves = 0
        self.Shots = 0
        self.Games = 0
        self.GameWins = 0
        self.SeriesWin = False
        self.Members = []
        self.Name = ""
    def setSeriesWin(self):
        self.SeriesWin = True
    def setGameWin(self):
        self.GameWins = self.GameWins + 1

