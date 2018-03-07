
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

        });
