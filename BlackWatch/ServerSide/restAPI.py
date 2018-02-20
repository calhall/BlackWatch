#!flask/bin/python

import sys, json, socket, pymongo, atexit, threading, time, os

from analysis.rulebased import AnalyseEvent
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
    print ("Database connected")
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
        socketio.emit('event', {'detectionPoint' : dp['dpName'], 'username' : user['username'], 'ipAddress' : user['ipAddress'], 'Time' : decoded['Time']}) #Send the event to the reporting agent
        return ("Event is being added")
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


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message['data'])



def sendAttack(dp, un, ip, time):
    socketio.emit('attack', {'detectionPoint' : dp, 'username' : un, 'ipAddress' : ip, 'Time' : time}) #Send the attack to the reporting agent

atexit.register(closingTime)

if __name__ == 'main':
	socketio.run(app)
