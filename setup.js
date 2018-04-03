use BlackWatch
db.createCollection('BlackWatch')
db.createCollection('WatchList')
db.createCollection('Prison')
db.createCollection('Responses')
use Configuration
db.createCollection('DetectionPoints')
dp1 = {dpName : 'HTTP Verb', Limit : '2', Period : '20', Response : 'Logout', Severity : 'Low'}
dp2 = {dpName : 'Login Page', Limit : '3', Period : '30', Response : 'Lockout(30), Enable 2FA', Severity : 'Low'}
db.DetectionPoints.insert(dp1)
db.DetectionPoints.insert(dp2)
