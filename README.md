# README.


# BlackWatch
The BlackWatch application was developed to encourage developers to implement attack awareness techniques into their applications. The following instructions should provide users with the guidance required to set up a basic instance of the BlackWatch application.

## Download the BlackWatch Application

Download the BlackWatch application by issuing the following command whilst in your intended installation directory - `git clone https://github.com/chall68/BlackWatch`


## MongoDB Setup

MongoDB is the default database used alongside the BlackWatch application. The following steps should be followed to set up the relevant databases:
 
### Install MongoDB

**Linux and Mac OS**

Follow the instructions provided by MongoDB to install the necessary database software.

Install MongoDB [Install MongoDB Community Edition on Ubuntu — MongoDB Manual 3.6](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

* Ensure that the service is running - `sudo service mongod status` 
	* If the service has stopped run - `sudo service mongod start`

### Configure the necessary databases.

* MongoDB allows users the ability to configure databases using pre-written creation scripts.
* Within the top directory of the BlackWatch that has been downloaded there is a 'setup.js' file.
    * To execute this file issue the following command - `mongo < setup.js`
    

## Setting up the BlackWatch Application

At this stage it is recommended that a virtual environment is created using python. This will ensure that any modules/dependencies that are downloaded are specific to the BlackWatch's environment rather than the systems default Python environment.

* To do this execute the following command - `python3 -m venv (path to the BlackWatch project folder)/env`
* Now activate this virtual environment by executing the following `source (path to BlackWatch project folder)/env/bin/activate`

Now that you are working within a virtual environment we can install the necessary dependencies.

* Whilst in the BlackWatch project folder execute - `pip install -r requirements.txt` this will install all required modules.
* Now from within the BlackWatch project folder simply run - `python run.py` and the BlackWatch application will be active.
* To access the applications web interface navigate to `http://localhost:5000`

### Testing Setup

Firstly open a new terminal and navigate to the BlackWatch project folder. Once there activate the virtual environment by sourcing the recently created `env/bin/activate` - the virtual environment we have previously created.
To ensure everything has been set up correctly navigate to the sampleApplications directory within the BlackWatch project and run the `clientGenerator.py` file. This should populate the web interface with some sample data. 


### Configuration

Implementing this solution to work alongside web applications will vary in approach for each web application. Within this project's main directory there is a folder `clientLibraries` that contains pre-written BlackWatch client side libraries. There will be unique instructions on how to implement each specific library into your application.

Adding new detection points to the BlackWatch solution can be easily done by accessing the Configurations page within the web interface.


*Note* - As of the time of writing, there is currently only one client side library that aids in the implementation process. Contributions to this area will be greatly appreciated.


## DISCLAIMER

It is important to note that this project is still very much in development, and is therefore likely to contain a number of security flaws as well as application bugs. Improvements and recommendations are welcome.
