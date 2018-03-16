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

    if (watchlist.find({'UserID' : username}).count() > 0):
        userCursor = watchlist.find({'UserID' : username})

        for document in userCursor:
            reputation = document['Reputation']
            print (reputation)
        if (reputation >= 10):
            socketio.emit('attack',
                          {'detectionPoint': "Multiple", 'username': username, 'ipAddress': ipAddress, 'Time': strTime,
                           'Session': sessionID})  # Send the attack to the reporting agent
            addResponse(username, sessionID, ipAddress, "Multiple", "Warn User", Time, socketio)



    elif (watchlist.find({'UserID' : sessionID}).count() > 0):
        userCursor = watchlist.find({'UserID' : sessionID})

        for document in userCursor:
            reputation = document['Reputation']

        if (reputation >= 10):
            socketio.emit('attack',
                          {'detectionPoint': "Multiple", 'username': 'Anonymous', 'ipAddress': ipAddress, 'Time': strTime,
                           'Session': sessionID})  # Send the attack to the reporting agent
            addResponse(None, sessionID, ipAddress, "Multiple", "Warn User", Time, socketio)


def increaseReputation(event, userID, Time, severity, socketio, client):

    # Convert severity to an integer
    # This can be configured to alter the strictness of the attack detection
    try:
        BlackWatch = client.BlackWatch
        watchlist = BlackWatch.Watchlist

        severityInt=0
        if (severity=="Low"):
            severityInt = 2
        elif (severity=="Medium"):
            severityInt = 4
        elif (severity=="High"):
            severityInt = 8
        if (watchlist.find({'UserID' : userID}).count() > 0):
            # TODO add in IF statement here so there is a max reputation you can have
            watchlist.update({'UserID' : userID}, { '$inc': { 'Reputation' : severityInt}}) #{'LastChecked' : datetime.now().isoformat()}
            #watchlist.update({'UserID' : userID}, {'LastChecked' : datetime.now().isoformat()}, True)

        else:
            watchlist.insert_one({'UserID' : userID, 'Reputation' : severityInt})
    except Exception as exc:
        print (exc)

    checkReputation(event, Time, socketio, client)
    #print("User under watch - " + watchlist.find({'UserID' : userID}))
# Detection Point information -----------------------------------


#---------------------------------------------------------------


