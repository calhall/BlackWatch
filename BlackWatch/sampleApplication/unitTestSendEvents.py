#!flask/bin/python
#from user import User
from sampleObjects.User import User
from datetime import datetime
from sampleObjects.DetectionPoint import DetectionPoint

import time, requests, random, atexit, unittest

class TestClient(unittest.TestCase):

    global detectionPointObject
    detectionPointObject = DetectionPoint("Login Page", "Hidden field altered within the login form")
    global userObject
    userObject = User("Test", "192.101.12.1", "xxxx")

    def testCorrect(self):

        self.assertEqual(sendEvent(userObject, detectionPointObject), "Event is being added") #Acceptable format

    def testIPWrong(self):

        userObjectWrong = User("1234", "192.299.12.1", "empty")
        self.assertEqual(sendEvent(userObjectWrong, detectionPointObject), "Incorrect formatting within POST request") #Incorrect IP

    def testDPWrong(self):

        detectionPointObjectWrong = DetectionPoint("Incorrect DP", "This doesn't exist")
        self.assertEqual(sendEvent(userObject, detectionPointObjectWrong), "Incorrect formatting within POST request") #Acceptable format



def sendEvent(user, dp):
    req = requests.post('http://localhost:5000/addevent', json = {"User": user.__dict__, "DetectionPoint" : dp.__dict__, "Time" : str(datetime.now().isoformat())})
    return req.text

def closingTime():
    print ("Exiting")


if __name__ == '__main__':
    unittest.main()

atexit.register(closingTime)
