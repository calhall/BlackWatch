#!flask/bin/python

import sys, json, socket, pymongo, atexit, threading, time, os

from BlackWatch.rulebased import AnalyseEvent
from BlackWatch.configuration import GetConfiguration, addDP, RemoveDP
 #TODO Possibly check to see if I should be importing full directories
from pymongo import MongoClient
from flask import Flask, request, Response, render_template
from flask_restful import Resource, Api
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blackwatch'
socketio = SocketIO(app)


#Connect to database -----------------

try:
    client = MongoClient()
    db = client.BlackWatch
    BlackWatch=db.BlackWatch

except:
    print ("Failed to connect to database")
    sys.exit() #If database can not be connected to - exit

# ------------------------------------


#Handle a user event
@app.route('/addevent', methods = ['POST'])
def addEvent():
    try:
        event = request.data
        Result = ParseEvent(event) #Send post data to be filtered
    except:
        Result = "Incorrect formatting within POST request"
    print (Result)
    return Result


@app.route('/adddetectionpoint', methods = ['POST'])
def addDetectionPoint():
    detectionPoint = request.data
    Result = dpdatabaseAdd(detectionPoint)

    print (Result)
    return Result


@app.route('/getConfiguration', methods = ['GET'])
def getConfig():
    configurationObject = GetConfiguration();
    print (configurationObject)
    return json.dumps(configurationObject)

@app.route('/deleteDP', methods = ['POST'])
def deleteDP():
    jsondata = json.loads(request.data)
    deleteName = jsondata['dpName']
    try:
        RemoveDP(deleteName)
        print ("Deleted")
        return "DP deleted"
    except:
        print ("Failed to delete DP")
        return "Failed to delete DP"

def ParseEvent(event):
    decoded = json.loads(event)
    user = decoded['User']
    dp = decoded['DetectionPoint']
    print ("Event Triggered by - " + user['username'] + " at detection point - " + dp['dpName'])
    if (checkIP(str(user['ipAddress']))):

        #thread = threading.Thread(target=databaseAdd, args=(decoded,)) #the arguments formatting is odd, however this ensures that only one parameter is passed
        #thread.start()
        #Threading has been temporarily disabled
        #This is to allow the socketio communications (reporting) to work, as it does like threading without a queue
        #TODO Implement RabbitMQ Queuing service

        socketio.emit('event', {'detectionPoint' : dp['dpName'], 'username' : user['username'], 'ipAddress' : user['ipAddress'], 'Time' : decoded['Time']}) #Send the event to the reporting agent
        databaseAdd(decoded)
        return ("Event is being added")
    else:
        print("Invalid IP + " + str(user['ipAddress']))
        return ("Incorrect formatting within POST request")



def databaseAdd(event):
    BlackWatch = db.BlackWatch
    BlackWatch.insert_one(event) #Add the event into the MongoDB database - BlackWatch
    try:
        AnalyseEvent(BlackWatch, event, socketio)
    except Exception as e:
        print (e)

def dpdatabaseAdd(dp):
    addResult = addDP(dp)
    return addResult

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


@app.route('/', methods = ['GET'])
def dashboard():
    return render_template('index.html')


@app.route('/configuration', methods = ['GET'])
def configuration():
    return render_template('configuration.html')


atexit.register(closingTime)

def run():
    socketio.run(app)
