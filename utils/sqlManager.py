import mysql.connector

def startConnection():

    with open("SQLData") as f:
        token = f.readlines()

    return mysql.connector.connect(host = "localhost",user = token[0] ,password = token[1], database = "novaleague")

def getTeamMembers():               # get dictionary of teamname as key and array of members as value
    mydb = startConnection()
    cursor = mydb.cursor()

    template = "SELECT teamname, membername FROM teamMembers;"
    cursor.execute(template)
    TeamAndMembers = cursor.fetchall()
    mydb.close()

    teamMembers = {}
    for turp in TeamAndMembers:
        try:
            teamMembers[turp[0]]
        except:
            teamMembers[turp[0]] = []
    
    for turp in TeamAndMembers:
        teamMembers[turp[0]].append(turp[1])

    return teamMembers

def getMemberandTeam():                                 # get dictionary of playernames as key and team as value
    mydb = startConnection()
    cursor = mydb.cursor()

    template = "SELECT membername, teamname FROM teamMembers;"
    cursor.execute(template)
    TeamAndMembers = cursor.fetchall()
    mydb.close()

    teamMembers = {}
    for turp in TeamAndMembers:
        try:
            teamMembers[turp[0]]
        except:
            teamMembers[turp[0]] = []
    
    for turp in TeamAndMembers:
        teamMembers[turp[0]].append(turp[1])

    return teamMembers

def instertMembers(team, memberlist):                           #insets members into team
    mydb = startConnection()

    cursor = mydb.cursor()
    template = "INSERT INTO teamMembers (teamname, membername) VALUES (%s, %s)"
    for member in memberlist:
        cursor.execute(template, (team, member, ))
    mydb.commit()
    mydb.close()

def teamList():
    mydb = startConnection()

    cursor = mydb.cursor()
    template = "SELECT name FROM team;"
    cursor.execute(template)
    teams = cursor.fetchall()
    mydb.close()

    teamlist = []
    for turp in teams:
        teamlist.append(turp[0])

    return teamlist

def matchMatch(team, week):
    mydb = startConnection()
    cursor = mydb.cursor()

    template = "SELECT id, teamHome, teamAway, bestOutOf FROM Matches WHERE (teamHome=%s OR teamAway=%s) AND week=%s;"
    cursor.execute(template, (team, team, week,))
    matchMatches = cursor.fetchall()

    mydb.close()
    return matchMatches
        
