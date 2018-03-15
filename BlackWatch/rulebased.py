import pprint, pymongo
from datetime import datetime, timedelta
from pymongo import MongoClient
from .reputationBased import checkReputation
from flask import Flask
from flask_socketio import SocketIO


def AnalyseEvent(BlackWatch, event, socketio):


    print ("Analysing")

# Event information ---------------------------------------------
    DetectionPoint = event['DetectionPoint']
    dpName = DetectionPoint['dpName']
    dpDescription = DetectionPoint['description']
    User = event['User']
    username = User['username']
    ipAddress = User['ipAddress']
    sessionID = User['sessionID']

    strTime = event['Time']
    strippedTime = strTime[0:19] #Only take the necessary time information)
    Time = datetime.strptime(strippedTime, "%Y-%m-%dT%H:%M:%S") #Simplified ISO 8601 time format

# ----------------------------------------------------------------


# Detection Point information -----------------------------------
    try:
        client = MongoClient()
        db = client.Configuration
    except:
        print ("Failed to connect to configuration database")

    try:
        DPConfig = db.DetectionPoints
        PredeterminedDP = DPConfig.find_one({ "dpName" : dpName})
        countLimit = PredeterminedDP['Limit']
        timeLimit = PredeterminedDP['Period']
        severity = PredeterminedDP['Severity']
        Threshold = Time - timedelta(seconds = int(timeLimit))

        #If the detection point is found, check to see if this event indicates an attack
        numberofUserEvents = BlackWatch.find({"User.username": username, "DetectionPoint.dpName": dpName, "Time": {'$gte': Threshold.isoformat()}}).count()  # Using dot notation (User.username) allows us to search nested objects
        numberofSessionEvents = BlackWatch.find({"User.sessionID": sessionID, "DetectionPoint.dpName": dpName, "Time": {'$gte': Threshold.isoformat()}}).count()  # Using dot notation (User.username) allows us to search nested objects

        if (numberofUserEvents >= int(countLimit)):
            socketio.emit('attack',
                          {'detectionPoint': dpName, 'username': username, 'ipAddress': ipAddress, 'Time': str(Time),
                           'Session': sessionID,
                           'description': dpDescription})  # Send the attack to the reporting agent
        elif (numberofSessionEvents >= int(countLimit)): # Incase the attacker is not authenticated under a user
            socketio.emit('attack',
                          {'detectionPoint': dpName, 'username': 'Anonymous', 'ipAddress': ipAddress, 'Time': str(Time),
                           'Session': sessionID,
                           'description': dpDescription})  # Send the attack to the reporting agent    except:
        else:
            # If the previous types of analysis have not identified an attack, move onto different methods
            checkReputation(BlackWatch, event, socketio)
    except:
        print ("Detection point not properly configured.")

# ---------------------------------------------------------------


