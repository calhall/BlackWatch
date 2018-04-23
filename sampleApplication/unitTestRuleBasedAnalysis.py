#!flask/bin/python
#from user import User
from sampleObjects.User import User
from datetime import datetime
from sampleObjects.DetectionPoint import DetectionPoint

import time, requests, random, atexit, unittest

class TestClient(unittest.TestCase):


    def testCorrect(self):

        self.assertEqual(sendAttack(), "Response returned") #Acceptable format



def sendAttack():

    timeofAttack = datetime.now().isoformat()
    userObject = User("Anonymous", "192.101.12.1", "xxxx1234")
    userObject2 = User("Anonymous", "192.101.12.1", "xxxx1234")
    userObject3 = User("Stelios", "192.101.12.1", "xxxx")
    dp1 = DetectionPoint("Login Page", "Hidden field altered within the login form")


    requests.post('http://localhost:5000/addevent',
                  json = {"User": userObject.__dict__, "DetectionPoint" : dp1.__dict__, "Time" : timeofAttack})
    requests.post('http://localhost:5000/addevent',
                  json = {"User": userObject.__dict__, "DetectionPoint" : dp1.__dict__, "Time" : timeofAttack})
    requests.post('http://localhost:5000/addevent',
                  json = {"User": userObject2.__dict__, "DetectionPoint" : dp1.__dict__, "Time" : timeofAttack})


    requests.post('http://localhost:5000/addevent',
                  json={"User": userObject3.__dict__, "DetectionPoint": dp1.__dict__, "Time": timeofAttack})
    requests.post('http://localhost:5000/addevent',
                  json={"User": userObject3.__dict__, "DetectionPoint": dp1.__dict__, "Time": timeofAttack})
    requests.post('http://localhost:5000/addevent',
                  json={"User": userObject3.__dict__, "DetectionPoint": dp1.__dict__, "Time": timeofAttack})
    time.sleep(1)
    checkResp = requests.get('http://localhost:5000/getResponses?username=' + "Anonymous" + "&" + "sessionID=" + "xxxx1234")
    checkResp2 = requests.get('http://localhost:5000/getResponses?username=' + "Stelios" + "&" + "sessionID=" + "xxxx")

    if (('{"username": "Anonymous", "Session": "xxxx1234", "Response": "Lockout(30)"}' in checkResp.text)
        or ('{"username": "Anonymous", "Session": "xxxx1234", "Response": "Enable 2FA"}' in checkResp.text)) \
            and (('{"username": "Stelios", "Session": "xxxx", "Response": "Lockout(30)"}' in checkResp2.text)
        or ('{"username": "Stelios", "Session": "xxxx", "Response": "Enable 2FA"}' in checkResp2.text)):
        return "Response returned"
    else:
        return "Failed"

def closingTime():
    print ("Exiting")


if __name__ == '__main__':
    unittest.main()

atexit.register(closingTime)
