#!flask/bin/python
#from user import User
from sampleObjects.User import User
from datetime import datetime
from sampleObjects.DetectionPoint import DetectionPoint

import time, requests, random, atexit, unittest

class TestClient(unittest.TestCase):

    global detectionPointObject
    detectionPointObject = DetectionPoint("<script>alert(1)</script>", "Hidden field altered within the login form")
    global userObject
    userObject = User("Test", "192.101.12.1", "xxxx")
    global isoformatTime
    isoformatTime = str(datetime.now().isoformat());

    def testCorrect(self):

        self.assertEqual(sendEvent(userObject, detectionPointObject, isoformatTime), "Event is being added") #Acceptable format

    def testIPWrong(self):

        userObjectWrong = User("1234", "192.299.12.1", "empty")
        self.assertEqual(sendEvent(userObjectWrong, detectionPointObject, isoformatTime), "Incorrect formatting within POST request") #Incorrect IP

    def testTimeFormat(self):

        self.assertEqual(sendEvent(userObject, detectionPointObject, "2018-03-01T07:55:26-08:00"), "Event is being added") #Acceptable format
        #Python's default ISO time looks like - 2018-03-01T08:04:35.867121
        #PHP uses ISO 8601 which looks like   - 2018-03-01T07:55:26-08:00

def sendEvent(user, dp, time):
    req = requests.post('http://localhost:5000/addevent', json = {"User": user.__dict__, "DetectionPoint" : dp.__dict__, "Time" : time})
    return req.text

def closingTime():
    print ("Exiting")


if __name__ == '__main__':
    unittest.main()

atexit.register(closingTime)
