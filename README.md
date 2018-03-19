# README.
#HonorsNotes

# BlackWatch
The BlackWatch application was developed to encourage developers to implement attack awareness techniques into their applications. The following instructions should provide users the guidance required to set up a basic instance of the BlackWatch application.

## MongoDB Setup

MongoDB is the default database used alongside the BlackWatch application. The following steps should be followed to set up the relevant databases:
 
### Install MongoDB

Linux & Mac OS

Install MongoDB [Install MongoDB Community Edition on Ubuntu — MongoDB Manual 3.6](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

* Ensure that the service is running - `sudo service mongod status` 
	* If the service has stopped run - `sudo service mongod start`

### To do - Windows installation

### Configure the necessary databases.

* To enter the MongoDB terminal type `mongo` within the standard terminal. 
* Type `show dbs` to view the current databases present - by default this will usually be ‘local’ 

#### BlackWatch Events Database

* To create the database enter  `use BlackWatch`  and then add the necessary collections:
    
    * Events collection - `db.createCollection('BlackWatch')`
    * Suspicious user collection - `db.createCollection('Watchlist')`
    * Malicious user collection - `db.createCollection('Prison')`
    

#### Configuration Database

Here we will create a separate database containing two example detection points. (HTTP Verb & Login Page)

To create the database enter  `use Configuration`  and then add a single record to initiate the database.
* db.createCollection('DetectionPoints')
* Create record - `dp1 = {dpName : "HTTP Verb", Limit : "2", Period : "60", Severity : "Low"}`
* Create record - `dp2 = {dpName : "Login Page", Limit : "3", Period : "30", Severity : "Low"}`
* Add the record - `db.DetectionPoints.insert(dp1);`
* Add the record - `db.DetectionPoints.insert(dp2);`

**Ensure that the records added into the configuration database match those above, this will ensure that they pass the unit tests.**
