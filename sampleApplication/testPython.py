from datetime import datetime, timedelta


currentTime = datetime.now().isoformat()
currentTimeDT = datetime.strptime(currentTime, "%Y-%m-%dT%H:%M:%S.%f")

fakeTime = currentTimeDT - timedelta(minutes = 35)
if currentTimeDT > fakeTime + timedelta(minutes = 30):
    print ("FUCK THE WORLD")
else:

    print ("fucked it")

