        eventLabel = document.getElementById("eventCount");
        attackLabel = document.getElementById("attackCount");
        responseLabel = document.getElementById("responseCount");

        var eventCounter = 0;
        var attackCounter = 0;
        var responseCounter = 0;

        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function()
        {
          socket.emit('message', {data: 'Reporting agent is active'});
        });

        socket.on('event', function(json)
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
          eventCounter = eventCounter + 1;
          eventLabel.innerHTML = eventCounter;
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
          attackLabel.innerHTML = attackCounter;
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

          cell1.innerHTML = json['detectionPoint'];
          cell2.innerHTML = json['username'];
          cell3.innerHTML = json['ipAddress'];
          cell4.innerHTML = json['Time'];
          responseCounter++;
          responseLabel.innerHTML = responseCounter;
        });
