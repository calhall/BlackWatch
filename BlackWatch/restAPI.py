#!flask/bin/python

import sys, json, socket, pymongo, atexit, threading, time, os

from BlackWatch.rulebased import AnalyseEvent
from BlackWatch.configuration import GetConfiguration, addDP, RemoveDP
from BlackWatch.responseHandler import getResponses
from BlackWatch.reportingCharts import attacksbyDP, attacksbyUserType
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
    client = MongoClient(serverSelectionTimeoutMS=1) # Max one second timeout for database queries
                                                     # Increase this if necessary (shouldn't be)
    client.server_info()
    db = client.BlackWatch
    BlackWatch=db.BlackWatch

except:
    print ("Failed to connect to database")
    sys.exit() #If database can not be connected to - exit

# ------------------------------------

# Render the templates for the web reporting mechanism
@app.route('/', methods = ['GET'])
def dashboard():
    return render_template('index.html')

@app.route('/AttackSummary')
def chart():

    dpAttacks = attacksbyDP(client)
    userAttacks = attacksbyUserType(client)

    return render_template('chart.html', set=dpAttacks, pie2=userAttacks)



@app.route('/configuration', methods = ['GET'])
def configuration():
    return render_template('configuration.html')

# ------------------------------------


# Handle communication with the server

# Handle a user event
@app.route('/addevent', methods = ['POST'])
def addEvent():
    try:
        event = request.data.decode('utf-8')
        Result = ParseEvent(event) #Send post request data to be analysed
    except:
        Result = "Incorrect formatting within POST request"
    return Result


@app.route('/adddetectionpoint', methods = ['POST'])
def addDetectionPoint():
    detectionPoint = request.data.decode('utf-8')
    Result = dpdatabaseAdd(detectionPoint)

    print (Result)
    return Result


@app.route('/getConfiguration', methods = ['GET'])
def getConfig():
    configurationObject = GetConfiguration()
    print (configurationObject)
    return json.dumps(configurationObject)


@app.route('/getResponses', methods = ['GET'])
def sendResponses():
    username = request.args.get('username')
    sessionID = request.args.get('username')

    responses = getResponses(username, sessionID, db) #Return responses for that user
    return responses

@app.route('/getAttacks', methods = ['GET'])
def getAttacks():

    attackList = []
    try:
        attacksCursor = db.Prison.find().sort([('_id', 1)]).limit(10);
        for document in attacksCursor:
            del document['_id']
            print(document)
            attackList.append(document)
    except Exception as exc:
        print (exc)
    return json.dumps(attackList)


@app.route('/deleteDP', methods = ['POST'])
def deleteDP():
    jsondata = json.loads(request.data.decode('utf-8'))
    deleteName = jsondata['dpName']
    try:
        RemoveDP(deleteName)
        print ("Deleted")
        return "DP deleted"
    except:
        print ("Failed to delete DP")
        return "Failed to delete DP"

# -----------------------------

def ParseEvent(event):
    decoded = json.loads(event)
    user = decoded['User']
    dp = decoded['DetectionPoint']
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
        print ("Failed to analyse event " and e)

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


atexit.register(closingTime)

def run():
    socketio.run(app)
