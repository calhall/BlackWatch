        eventLabel = document.getElementById("eventCount");
        attackLabel = document.getElementById("attackCount");
        responseLabel = document.getElementById("responseCount");

        var eventCounter = 0;
        var attackCounter = 0;
        var responseCounter = 0;

        var events = true;
        var attacks = true;
        var responses = false;

        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function()
        {
          socket.emit('message', {data: 'Reporting agent is active'});
        });

        socket.on('event', function(json)
        {
          if (events) 
          {
              var table = document.getElementById("eventsTable");
              table.deleteRow(8);

              var row = table.insertRow(1);
              var cell1 = row.insertCell(0);
              var cell2 = row.insertCell(1);
              var cell3 = row.insertCell(2);
              var cell4 = row.insertCell(3);

              cell1.innerHTML = json['detectionPoint'];
              cell2.innerHTML = json['username'];
              cell3.innerHTML = json['ipAddress'];
              cell4.innerHTML = json['Time'];
          }
              eventCounter = eventCounter + 1;
              eventLabel.innerHTML = eventCounter.toString();
        });

        socket.on('attack', function(json)
        {
          var table = document.getElementById("eventsTable");
          table.deleteRow(8);

          var row = table.insertRow(1);
          row.style.backgroundColor = "#1b4517";
          var cell1 = row.insertCell(0);
          var cell2 = row.insertCell(1);
          var cell3 = row.insertCell(2);
          var cell4 = row.insertCell(3);

          cell1.innerHTML = json['detectionPoint'];
          cell2.innerHTML = json['username'];
          cell3.innerHTML = json['ipAddress'];
          cell4.innerHTML = json['Time'];
          attackCounter++;
          attackLabel.innerHTML = attackCounter.toString();
        });

        socket.on('response', function(json)
        {
          var table = document.getElementById("eventsTable");
          table.deleteRow(8);

          var row = table.insertRow(1);
          row.style.backgroundColor = "#1a1a45";
          var cell1 = row.insertCell(0);
          var cell2 = row.insertCell(1);
          var cell3 = row.insertCell(2);
          var cell4 = row.insertCell(3);

          cell1.innerHTML = json['dpName'];
          cell2.innerHTML = json['username'];
          cell3.innerHTML = json['ipAddress'];
          cell4.innerHTML = json['Time'];
          responseCounter++;
          responseLabel.innerHTML = responseCounter.toString();
        });
        
        // Set some button listeners
        var btnAll = document.getElementById("btnAll");
        var btnAttacks = document.getElementById("btnAttacks");
        var btnResponses = document.getElementById("btnResponses");

        btnAll.onclick = function() {
            events = true;
            var third = document.getElementById("thirdColumn");
            third.innerText = "IP Address"
        };
        btnAttacks.onclick = function() {
            getAttacks();
        };
        btnResponses.onclick = function () {
            getResponses();
        };


        
function getAttacks() {    

    var third = document.getElementById("thirdColumn");

    third.innerText = "IP Address"
    events = false;
    var responseText = null;
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            responseText = xmlHttp.responseText;
            if (responseText != null) {
                displayAttacks(JSON.parse(responseText));
            }
    }
    xmlHttp.open("GET", 'http://localhost:5000/getAttacks', true); // true for asynchronous
    xmlHttp.send(null);
    
    }
    
    
    function displayAttacks(attacks) {

        var table = document.getElementById("eventsTable");

        for (i=0; i < attacks.length; i++)

        {
            json = attacks[i];
            table.deleteRow(1)
            var row = table.insertRow(8);
            row.style.backgroundColor = "#1b4517";
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);

            cell1.innerHTML = json['dpName'];
            cell2.innerHTML = json['attackerID'];
            cell3.innerHTML = json['ipAddress'];
            cell4.innerHTML = json['Time'];
        }

    }

    function getResponses() {

    events = false;
    attacks = false;

    var third = document.getElementById("thirdColumn");

    third.innerText = "Responses"

    var responseText = null;
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            responseText = xmlHttp.responseText;
            if (responseText != null) {
                displayResponses(JSON.parse(responseText));
            }
    }
    xmlHttp.open("GET", 'http://localhost:5000/getRecentResponses', true); // true for asynchronous
    xmlHttp.send(null);

    }


    function displayResponses(responses) {
        var table = document.getElementById("eventsTable");

        for (i=0; i < responses.length; i++)

        {
            json = responses[i];
            table.deleteRow(1)
            var row = table.insertRow(8);
            row.style.backgroundColor = "#1a1a45";
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);


            cell1.innerHTML = json['dpName'];
            cell2.innerHTML = json['username'];
            cell3.innerHTML = json['Response'];
            cell4.innerHTML = json['Time'];

        }

    }
