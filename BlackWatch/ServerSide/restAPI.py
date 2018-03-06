#!flask/bin/python

import sys, json, socket, pymongo, atexit, threading, time, os

# noinspection PyUnresolvedReferences
from rulebased import AnalyseEvent #TODO Possibly check to see if I should be importing full directories
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


@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')


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
    eventID = BlackWatch.insert_one(event).inserted_id #Add the event into the MongoDB database - BlackWatch
    AnalyseEvent(BlackWatch, event, socketio)


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


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message['data'])



atexit.register(closingTime)

if __name__ == 'main':
    socketio.run(app)
