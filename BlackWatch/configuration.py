from pymongo import MongoClient
import json

def GetConfiguration():

    detectionPointList = []

    try:
        client = MongoClient()
        db = client.Configuration

        # Get all detection points from the configuration database

        DPConfig = db.DetectionPoints
        allDetectionPoints = DPConfig.find()

        for dp in allDetectionPoints:
            try:
                name = dp['dpName']
                countLimit = dp['Limit']
                timeLimit = dp['Period']
                response = dp['Response']
                severity = dp['Severity']

                print (name)
                if ',' in response:
                    responses = response.split(',')
                    dpObject = {"Name" : name, "Count" : countLimit, "Time" : timeLimit, "Response" : responses, 'Severity' : severity} #multiple responses
                else:
                    dpObject = {"Name" : name, "Count" : countLimit, "Time" : timeLimit, "Response" : response, 'Severity' : severity} #single response
                detectionPointList.append(dpObject) #Add the necessary information to the list
            except:
                print ("Missing information from document (DP)")
                
        return detectionPointList
    except:
        print ("Failed to connect to configuration database")


# Add a new detection point

def addDP(rawdp):

    dp = json.loads(rawdp)
    try:
        client = MongoClient()
        db = client.Configuration
        ConfigurationDB = db.DetectionPoints
        if (ConfigurationDB.find({ 'dpName' : dp['dpName']}).count() > 0):
            return "This detection point name is already taken."
        else:
            ConfigurationDB.insert_one(dp)
            return "DP added successfully"
    except Exception as e:
        return "Failed to add DP"

# Remove a detection point

def RemoveDP(dpName):

    try:
        client = MongoClient()
        db = client.Configuration
        ConfigurationDB = db.DetectionPoints
        ConfigurationDB.remove({ "dpName" : dpName} )
        return "DP deleted successfully"
    except:
        print ("FAILED")

        return "Failed to add DP"