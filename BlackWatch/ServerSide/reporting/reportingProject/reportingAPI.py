#!flask/bin/python

import sys, json, socket, pymongo, atexit, threading, time

from pymongo import MongoClient
from flask import Flask, request, Response, render_template
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
@app.route('/home', methods = ['GET'])
def getInfo():
    return render_template('home.html', details="There has been an event triggered")


def closingTime():
    client.close()
    print ("Cheerio")

atexit.register(closingTime)

if __name__ == 'main':
	app.run(debug=True, threaded=True, host='0.0.0.0', port=4600)
