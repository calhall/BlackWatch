class User(object):
    username = ""
    ipAddress = "0.0.0.0"
    sessionID = "empty"

    def __init__(self, username, ipAddress, sessionID):
        self.username = username
        self.ipAddress = ipAddress
        self.sessionID = sessionID

    def makeUser(username, ipAddress, sessionID):
        user = User(username, ipAddress, sessionID)
        return user
