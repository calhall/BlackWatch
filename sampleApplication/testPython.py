from datetime import datetime, timedelta


currentTime = datetime.now().isoformat()
currentTimeDT = datetime.strptime(currentTime, "%Y-%m-%dT%H:%M:%S.%f")

sampleTime = "2018-03-17T17:23:43.635745"
sampleTimeDT = datetime.strptime(sampleTime, "%Y-%m-%dT%H:%M:%S.%f")

difference = currentTimeDT - sampleTimeDT
print (difference.total_seconds() / 600)

