#!flask/bin/python
#from user import User
from sampleObjects.User import User
from datetime import datetime
from sampleObjects.DetectionPoint import DetectionPoint

import time, requests, random

def requestGenerator():
    userObject = randomUser()
    detectionPointObject = randomDetectionPoint()

    req = requests.post('http://localhost:5000/addevent', json = {"User": userObject.__dict__, "DetectionPoint" : detectionPointObject.__dict__, "Time" : str(datetime.now().isoformat())})
    print (str(datetime.now().isoformat()))

    print(req.status_code)

def randomUser():
    user = random.randint(1,2)
    attacker=0
    print (user)
    if (user==1):
        attacker = User("Phillipo", "255.255.255.101")
    elif (user==2):
        attacker = User("Sergio", "109.123.234.1")

    return attacker



def randomDetectionPoint():
    rand = random.randint(1,2)
    dp=0
    print (rand)
    if (rand==1):
        dp = DetectionPoint("HTTP Verb", "GET Request used where POST is expected")
    elif (rand==2):
        dp = DetectionPoint("Login Page", "Hidden field altered within the login form")

    return dp


for i in range (10):
    requestGenerator()
    time.sleep(2)
