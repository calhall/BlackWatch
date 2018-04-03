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
    userObject = User("repTest", "192.101.12.1", "xxxx")
    dp1 = DetectionPoint("Login Page", "Hidden field altered within the login form")
    dp2 = DetectionPoint("HTTP Verb", "Hidden field altered within the login form")
    dp3 = DetectionPoint("Malicious File Upload", "Hidden field altered within the login form")


    requests.post('http://localhost:5000/addevent', json = {"User": userObject.__dict__, "DetectionPoint" : dp1.__dict__, "Time" : timeofAttack})
    requests.post('http://localhost:5000/addevent', json = {"User": userObject.__dict__, "DetectionPoint" : dp2.__dict__, "Time" : timeofAttack})
    requests.post('http://localhost:5000/addevent', json = {"User": userObject.__dict__, "DetectionPoint" : dp3.__dict__, "Time" : timeofAttack})
    time.sleep(1)
    checkResp = requests.get('http://localhost:5000/getResponses?username=' + "repTest" + "&" + "sessionID=" + "xxxx")
    print (checkResp.text)

    if '{"Username": "repTest", "Detection Point": "Multiple", "SessionID": "xxxx", "Response": "Warn User"}' in checkResp.text:
        return "Response returned"
    elif '{"Username": "repTest", "Detection Point": "Multiple", "SessionID": "xxxx", "Response": " Logout"}' in checkResp.text:
        return "Response returned"
    else:
        return "Failed"

def closingTime():
    print ("Exiting")


if __name__ == '__main__':
    unittest.main()

atexit.register(closingTime)
