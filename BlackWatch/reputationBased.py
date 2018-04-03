from datetime import datetime, timedelta
from BlackWatch.responseHandler import addResponse



def checkReputation(event, Time, socketio, client):


# Event information ---------------------------------------------
    DetectionPoint = event['DetectionPoint']
    strTime = event['Time']
    dpName = DetectionPoint['dpName']
    User = event['User']
    username = User['username']
    ipAddress = User['ipAddress']
    sessionID = User['sessionID']


#----------------------------------------------------------------

    BlackWatch = client.BlackWatch
    watchlist = BlackWatch.Watchlist

    currentTime = datetime.now().isoformat()
    currentTimeDT = datetime.strptime(currentTime, "%Y-%m-%dT%H:%M:%S.%f")

    if (watchlist.find({'UserID' : username}).count() > 0):
        userCursor = watchlist.find({'UserID' : username})

        for document in userCursor:
            reputation = document['Reputation']
            lastChecked = document['LastChecked']



        lastCheckedDT = datetime.strptime(lastChecked, "%Y-%m-%dT%H:%M:%S.%f")

        difference = currentTimeDT - lastCheckedDT #Get the total difference in time between last checked and now

        for x in range (0, int(difference.total_seconds()/600)): # Every ten minutes since last event, decrement the users reputation by one
            if (reputation==0) :
                break
            else:
                reputation = reputation - 1

            watchlist.update({'UserID': username}, {'$set': {'Reputation': reputation}})
            watchlist.update({'UserID': username}, {'$set': {'LastChecked': currentTime}})
        if (reputation >= 10):
            socketio.emit('attack',
                          {'detectionPoint': "Multiple", 'username': username, 'ipAddress': ipAddress, 'Time': strTime,
                           'Session': sessionID})  # Send the attack to the reporting agent
            addResponse(username, sessionID, ipAddress, "Multiple", "Warn User, Manual Response", Time, socketio)



    elif (watchlist.find({'UserID' : sessionID}).count() > 0):
        userCursor = watchlist.find({'UserID' : sessionID})

        for document in userCursor:
            reputation = document['Reputation']
            lastChecked = document['LastChecked']

            lastCheckedDT = datetime.strptime(lastChecked, "%Y-%m-%dT%H:%M:%S.%f")

            difference = currentTimeDT - lastCheckedDT  # Get the total difference in time between last checked and now

            while (reputation > 0):
                for x in range(0, int(
                        difference.total_seconds() / 600)):  # Every ten minutes since last event, decrement the users reputation by one
                    if (reputation == 0):
                        break
                    else:
                        reputation = reputation - 1

                watchlist.update({'UserID': sessionID}, {'$set': {'Reputation': reputation}})
                watchlist.update({'UserID': sessionID}, {'$set': {'LastChecked': currentTime}})


        if (reputation >= 10):
            socketio.emit('attack',
                          {'detectionPoint': "Multiple", 'username': 'Anonymous', 'ipAddress': ipAddress, 'Time': strTime,
                           'Session': sessionID})  # Send the attack to the reporting agent
            addResponse(None, sessionID, ipAddress, "Multiple", "Warn User, Manual Response", Time, socketio)


def increaseReputation(event, userID, Time, severity, socketio, client):

    # Convert severity to an integer
    # This can be configured to alter the strictness of the attack detection
    try:
        BlackWatch = client.BlackWatch
        watchlist = BlackWatch.Watchlist

        severityInt=0
        if (severity=="Very Low"):
            severityInt = 1
        if (severity=="Low"):
            severityInt = 2
        elif (severity=="Medium"):
            severityInt = 4
        elif (severity=="High"):
            severityInt = 8
        if (watchlist.find({'UserID' : userID}).count() > 0):
            user = watchlist.find({'UserID' : userID})
            for doc in user:
                reputation = doc['Reputation']

            if (reputation <= 15): # Ensures that a user's reputation can only get so high
                watchlist.update({'UserID' : userID}, { '$inc': { 'Reputation' : severityInt}})
                watchlist.update({'UserID' : userID}, { '$set': {'LastChecked' : datetime.now().isoformat()}})

        else:
            watchlist.insert_one({'UserID' : userID, 'Reputation' : severityInt, 'LastChecked' : datetime.now().isoformat()})
    except Exception as exc:
        print (exc)



