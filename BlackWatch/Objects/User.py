class User(object):
    username = ""
    ipAddress = 0

    def __init__(self, username, ipAddress):
        self.username = username
        self.ipAddress = ipAddress

    def makeUser(username, ipAddress):
        user = User(username, ipAddress)
        return user
