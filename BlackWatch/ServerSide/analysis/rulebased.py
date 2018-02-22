import pprint, pymongo
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import Flask
from flask_socketio import SocketIO
import restAPI


app = Flask("main")
app.config['SECRET_KEY'] = 'blackwatch'
socketio = SocketIO(app)


def AnalyseEvent(BlackWatch, event):


    print ("Analysing")

# Event information ---------------------------------------------
    DetectionPoint = event['DetectionPoint']
    dpName = DetectionPoint['dpName']
    User = event['User']
    username = User['username']
    ipAddress = User['ipAddress']

    strTime = event['Time']
    Time = datetime.strptime(strTime, "%Y-%m-%dT%H:%M:%S.%f")
#----------------------------------------------------------------

# Detection Point information -----------------------------------
    try:
        client = MongoClient()
        db = client.Configuration
    except:
        print ("Failed to connect to configuration database")

    DPConfig = db.DetectionPoints
    PredeterminedDP = DPConfig.find_one({ "dpName" : dpName})
    countLimit = PredeterminedDP['Limit']
    print (countLimit)
    timeLimit = PredeterminedDP['Period']
    Threshold = Time - timedelta(seconds = int(timeLimit))
#---------------------------------------------------------------


    numberofEvents = BlackWatch.find({ "User.username" : username, "DetectionPoint.dpName" : dpName, "Time" : { '$gte' : Threshold.isoformat() }}).count() #Using dot notation (User.username) allows us to search nested objects
    if (numberofEvents >= int(countLimit)):
        #socketio.emit('attack', {'detectionPoint' : dpName, 'username' : username, 'ipAddress' : ipAddress, 'Time' : Time}) #Send the attack to the reporting agent
        sendAttack(dpName, username, ipAddress, Time)
        print ("-------------The user - " + User['username'] + " has triggered an attack at detection point - " + dpName + "-----------------")
