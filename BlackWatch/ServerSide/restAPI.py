#!flask/bin/python

import sys, json, socket, pymongo, atexit, threading, time

from analysis.rulebased import AnalyseEvent
from pymongo import MongoClient
from flask import Flask, request, Response
from flask_restful import Resource, Api

app = Flask(__name__)
#api = Api(app)


#Connect to database -----------------
try:
    client = MongoClient()
    db = client.BlackWatch
    print ("Database connected")
except:
    print ("Failed to connect to database")
    sys.exit() #If database can not be connected to - exit
# ------------------------------------


#Handle a user event
@app.route('/addevent', methods = ['POST'])
def addEvent():
    event = request.data
    Result = ParseEvent(event) #Send post data to be filtered
    return Result



def ParseEvent(event):
    decoded = json.loads(event)
    user = decoded['User']
    dp = decoded['DetectionPoint']
    print ("Event Triggered by - " + user['username'] + " at detection point - " + dp['dpName'])
    if (checkIP(str(user['ipAddress']))):
        thread = threading.Thread(target=databaseAdd, args=(decoded,)) #the arguments formatting is odd, however this ensures that only one parameter is passed
        thread.start()
        #Do I need to use threading? Or should I just allow tasks to be completed prior to responding to the request
        #databaseAdd(decoded)
        return ("Event is being added")
    else:
        print("Invalid IP + " + str(user['ipAddress']))
        return ("Invalid IP given")
    detectionPoint = decoded['DetectionPoint']


def databaseAdd(event):
    time.sleep(8)
    BlackWatch = db.BlackWatch
    eventID = BlackWatch.insert_one(event).inserted_id
    AnalyseEvent(BlackWatch, event)

def checkIP(IP):
    try:
        socket.inet_aton(IP)
        return True
        #legtimate IP
    except socket.error:
        print ("Incorrect IP Address")
        return False


def closingTime():
    client.close()
    print ("Cheerio")

atexit.register(closingTime)

if __name__ == 'main':
	app.run(debug=True, threaded=True)
