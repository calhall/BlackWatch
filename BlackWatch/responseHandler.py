# This file is used to handle the responses that have been set for attacks
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
responses = []

def addResponse(username, sessionID, ipAddress, dpName, response, Time, socketio):

    try:
        client = MongoClient()
        BlackWatch = client.BlackWatch
        prison = BlackWatch.Prison # This variable will be passed throughout these methods for communicating with the DB

    except Exception as dbException:
        print (dbException)

    # Add the malicious user to a list (for monitoring and for incrementing responses)
    if (username):
        finalResponse = determineResponse(username, dpName, response, prison)
        attackObject = {'attackerID' : username, 'dpName' : dpName, 'Time' : datetime.now().isoformat()}
        prison.insert_one(attackObject) # Send the attacker to jail

        socketio.emit('response',
                      {'detectionPoint': dpName, 'username': username, 'ipAddress': ipAddress, 'Time': str(Time),
                       'Session': sessionID})

    elif (sessionID != None):
        finalResponse = determineResponse(sessionID, dpName, response, prison)

        attackObject = {'attackerID': username, 'dpName': dpName, 'Time' : datetime.now().isoformat()}
        prison.insert_one(attackObject)

        socketio.emit('response',
                      {'detectionPoint': dpName, 'username': 'Anonymous', 'ipAddress': ipAddress, 'Time': str(Time),
                       'Session': sessionID})

    responseObject = {'Username' : username, 'Detection Point' : dpName, 'SessionID' : sessionID, 'Response' : finalResponse}
    responses.append(responseObject) # Maybe add this to a db? Realistically... do I need to? Should be accessed very regularly

def getResponses():
    formattedResponses = json.dumps(responses)
    responses.clear()
    return formattedResponses


def determineResponse(attacker, dpName, responseRaw, prison):

    deleteOld(prison)

    try:
        if ',' in responseRaw: #If there are multiple responses, then increment the response
            multipleResponses = responseRaw.split(',')
            numResponses = len(multipleResponses)
            attackCount = checkmaliciousUsers(attacker, dpName, prison)

            if (attackCount >= numResponses):
                return multipleResponses[numResponses-1] # return the greatest response possible
            else:
                return multipleResponses[attackCount] # return the relevant response based on level of attack
        else:
            return responseRaw # There only is one response
    except Exception as broke:
        print (broke)


def checkmaliciousUsers(user, dpName, prison):

    # Delete users from this list after 30 minutes
    try:
        return prison.find({'attackerID' : user, 'dpName' : dpName}).count()
    except Exception as oddExc:
        print (oddExc)
        return "Failed to check malicious users" + oddExc

def deleteOld(prison): # Delete any users from the malicious users array after 30 minutes of no bad behaviour

    currentTime = datetime.now().isoformat()
    currentTimeDT = datetime.strptime(currentTime, "%Y-%m-%dT%H:%M:%S.%f")
    timesUp = currentTimeDT - timedelta(minutes=30)

    prison.remove({"Time": {'$lt': timesUp.isoformat()}})

    # TODO Delete this when done

    #for object in maliciousUsers:
    #    formattedTime = datetime.strptime(object['Time'], "%Y-%m-%dT%H:%M:%S.%f")
    #    if (currentTimeDT > formattedTime + timedelta(minutes=30)):
    #        maliciousUsers.remove(object)