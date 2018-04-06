from BlackWatch.configuration import GetConfiguration
from datetime import datetime, timedelta
import random

def attacksbyDP(client):

    detectionPoints = GetConfiguration() # Get all detection points

    db = client.BlackWatch
    BlackWatch = db.BlackWatch

    nameList = []
    colourList = []
    attackList = []

    Time = datetime.strptime(datetime.now().isoformat()[0:19], "%Y-%m-%dT%H:%M:%S")
    timeYesterday = Time - timedelta(hours=24)
    timeYesterday = str(timeYesterday).replace(' ', 'T')

    for detectionPoint in detectionPoints:

        print (timeYesterday)
        name = detectionPoint['Name']
        count = BlackWatch.find({"DetectionPoint.dpName": name,
                                "Time": {'$gte': timeYesterday}}).count()
        r = lambda: random.randint(0, 255)
        colour = ('#%02X%02X%02X' % (r(), r(), r()))

        nameList.append(str(name))
        attackList.append(count)
        colourList.append(colour)

    return zip(attackList, nameList, colourList)

def attacksbyUserType(client):

    colourList = []

    db = client.BlackWatch
    BlackWatch = db.BlackWatch

    Time = datetime.strptime(datetime.now().isoformat()[0:19], "%Y-%m-%dT%H:%M:%S")
    timeYesterday = Time - timedelta(hours=24)
    timeYesterday = str(timeYesterday).replace(' ', 'T')

    anonymousAttacks = BlackWatch.find({'$or': [{'User.username' : 'Anonymous'}, {'User.username' : 'anonymous'},
                                                {'User.username' : 'None'}, {'User.username' : 'none'},
                                                {'User.username' : 'Null'}, {'User.username' : 'null'}],
                                        "Time": {'$gte': timeYesterday}}).count()

    authenticatedAttacks = BlackWatch.find({"Time": {'$gte': timeYesterday}}).count() - anonymousAttacks

    labels = ['Authenticated Users', 'Anonymous Users']
    allUsers = [authenticatedAttacks, anonymousAttacks]

    for i in range(0,2):
        r = lambda: random.randint(0, 255)
        colour = ('#%02X%02X%02X' % (r(), r(), r()))
        colourList.append(colour)
    return zip(allUsers, labels, colourList)