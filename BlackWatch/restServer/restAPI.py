#!flask/bin/python

import pprint, json, socket, pymongo, atexit

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
    print ("Event Triggered by - " + user['username'])
    if (checkIP(str(user['ipAddress']))):
        print ("IP Address for " + user['username'] + " is " + str(user['ipAddress']))
        databaseAdd(decoded)
        return ("Event Created")
    else:
        print("Invalid IP + " + str(user['ipAddress']))
        return ("Invalid IP given")
    detectionPoint = decoded['DetectionPoint']


def databaseAdd(event):
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
	app.run(debug=True)
