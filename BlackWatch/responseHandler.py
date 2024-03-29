# This file is used to handle the responses that have been set for attacks
import json
from datetime import datetime, timedelta
from pymongo import MongoClient


responses = []

client = MongoClient()

def addResponse(username, sessionID, ipAddress, dpName, response, Time, socketio): # TODO Manual responses must be added

    try:
        BlackWatch = client.BlackWatch
        prison = BlackWatch.Prison # This variable will be passed throughout these methods for communicating with the DB
        responseDB = BlackWatch.Responses
    except Exception as dbException:
        print (dbException)

    # Add the malicious user to a list (for monitoring and for incrementing responses)
    if (username):
        finalResponse = determineResponse(username, dpName, response, prison)
        if (finalResponse[0] == ' '):  # If the user has entered multiple responses, and has used a space after the comma
            finalResponse = finalResponse[1:]

        attackObject = {'attackerID' : username, 'dpName' : dpName, 'sessionID' : sessionID, 'ipAddress' : ipAddress, 'Time' : datetime.now().isoformat()}
        responseObject = {'dpName': dpName, 'username': username, 'ipAddress': ipAddress, 'Time': Time.isoformat(),
                       'Session': sessionID, 'Response' : finalResponse}
        socketio.emit('response', responseObject)
        prison.insert_one(attackObject) # Send the attacker to jail
        responseDB.insert_one(responseObject)

    elif (sessionID != None):
        finalResponse = determineResponse(sessionID, dpName, response, prison)
        if (finalResponse[0] == ' '):  # If the user has entered multiple responses, and has used a space after the comma
            finalResponse = finalResponse[1:]

        attackObject = {'attackerID': username, 'dpName': dpName, 'sessionID' : sessionID, 'ipAddress' : ipAddress, 'Time' : datetime.now().isoformat()}
        responseObject = {'dpName': dpName, 'username': 'Anonymous', 'ipAddress': ipAddress, 'Time': Time.isoformat(),
                       'Session': sessionID, 'Response' : finalResponse}
        socketio.emit('response', responseObject)
        prison.insert_one(attackObject)
        responseDB.insert_one(responseObject)


    if (finalResponse != "Manual Response"):
        respObject = {'Username' : username, 'Detection Point' : dpName, 'SessionID' : sessionID, 'Response' : finalResponse}
        responses.append(respObject) # Maybe add this to a db? Realistically... do I need to? Should be accessed very regularly



def getResponses(username, sessionID, db):
    responseDB = db.Responses

    if (username=="Anonymous" or username=="None" or username=="Null" or username==""):
        recentRespones = responseDB.find({"Session" : sessionID})
    else:
        recentRespones = responseDB.find({"username" : username})

    responseList = []
    try:
        for document in recentRespones:
            if (document['Response'] != "Manual Response"):
                del document['_id']
                del document['ipAddress']
                del document['dpName']
                del document['Time']
                print(document)
                responseList.append(document)
    except Exception as exc:
        print(exc)

    if (username=="Anonymous" or username=="None" or username=="Null" or username==""):
        responseDB.delete_many({"Session" : sessionID})
    else:
        responseDB.delete_many({"username" : username})


    return json.dumps(responseList)



def determineResponse(attacker, dpName, responseRaw, prison):

    deleteOld(prison) # Ensure the list is up-to-date

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
