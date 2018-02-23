#!flask/bin/python
#from user import User
from pymongo import MongoClient
import time, requests, random, atexit, unittest

class TestDB(unittest.TestCase):

    #Tests to make sure the MongoDB database is properly configured

    global client
    client = MongoClient()

    def testConfigDB(self): #Tests to see if the configuration database (eg. where detection points are stored) is active/properly configured

        self.assertEqual(configDBConnect(), "Successful connection") #Acceptable format

    def testBlackWatchDB(self):  # Tests to see if the BlackWatch database (eg. where events are stored) is active/properly configured

        self.assertEqual(BlackWatchDBConnect(), "Successful connection")  # Acceptable format


def configDBConnect():
    try:
        db = client.Configuration #Create a connection with the Configuration database
        return ("Successful connection")
    except:
        return ("Failed to connect")

def BlackWatchDBConnect():
    try:
        db = client.BlackWatch #Create a connection with the BlackWatch database
        return ("Successful connection")
    except:
        return ("Failed to connect")


def closingTime():
    print ("Exiting")


if __name__ == '__main__':
    unittest.main()

atexit.register(closingTime)
