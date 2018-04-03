import pprint, pymongo
from datetime import datetime, timedelta
from pymongo import MongoClient
from BlackWatch.reputationBased import checkReputation, increaseReputation
from BlackWatch.responseHandler import addResponse

def AnalyseEvent(BlackWatch, event, socketio):

# Event information ---------------------------------------------
    DetectionPoint = event['DetectionPoint']
    dpName = DetectionPoint['dpName']
    User = event['User']
    username = User['username']
    ipAddress = User['ipAddress']
    sessionID = User['sessionID']

    strTime = event['Time']
    strippedTime = strTime[0:19] #Only take the necessary time information)
    Time = datetime.strptime(strippedTime, "%Y-%m-%dT%H:%M:%S") #Simplified ISO 8601 time format

# ---------------------------------------------------------------


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
        response = PredeterminedDP['Response']
        Threshold = Time - timedelta(seconds = int(timeLimit))


        # If the detection point is found, check to see if this event indicates an attack


        if (username != None and username != "Anonymous"): # Make sure the username isn't blank (or all unauthenticated users will match)
            numberofUserEvents = BlackWatch.find({"User.username": username, "DetectionPoint.dpName": dpName,
                                                  "Time": {'$gte': Threshold.isoformat()}}).count()  # Using dot notation (User.username) allows us to search nested objects

            increaseReputation(event, username, strTime, severity, socketio, client) # Add this event to the users reputation
            numberofSessionEvents = 0 #No point checking sessionID as it will be the same as authenticated user
        else:
            numberofUserEvents=0
            increaseReputation(event, sessionID, strTime, severity, socketio, client) # Add this event to the users reputation
            numberofSessionEvents = BlackWatch.find({"User.sessionID": sessionID, "DetectionPoint.dpName": dpName,
                                                     "Time": {'$gte': Threshold.isoformat()}}).count()  # Using dot notation (User.username) allows us to search nested objects


        if (numberofUserEvents >= int(countLimit)):
            print ("Attack Identified - " + username + " - " + dpName)
            socketio.emit('attack',
                          {'detectionPoint': dpName, 'username': username, 'ipAddress': ipAddress, 'Time': strTime,
                           'Session': sessionID})  # Send the attack to the reporting agent
            addResponse(username, sessionID, ipAddress, dpName, response, Time, socketio)

        elif (numberofSessionEvents >= int(countLimit)): # Incase the attacker is not authenticated under a user
            print ("Attack Identified - " + username + " - " + dpName)
            socketio.emit('attack',
                          {'detectionPoint': dpName, 'username': 'Anonymous', 'ipAddress': ipAddress, 'Time': strTime,
                           'Session': sessionID})  # Send the attack to the reporting agent
            addResponse(None, sessionID, ipAddress, dpName, response, Time, socketio)
        else:
            checkReputation(event, Time, socketio, client)

    except Exception as exc:
        print ("Detection point not properly configured. - " and exc)

# ---------------------------------------------------------------


