import pprint, pymongo
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import Flask
from flask_socketio import SocketIO


def checkReputation(BlackWatch, event, socketio):


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

#----------------------------------------------------------------


# Detection Point information -----------------------------------


#---------------------------------------------------------------


