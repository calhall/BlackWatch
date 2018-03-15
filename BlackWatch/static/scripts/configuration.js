    var responseText = null;
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            responseText = xmlHttp.responseText;
            if (responseText != null) {
                displayDPs(JSON.parse(responseText));
            }
    }
    xmlHttp.open("GET", 'http://localhost:5000/getConfiguration', true); // true for asynchronous
    xmlHttp.send(null);

    function displayDPs(response)
    {
        for (var i = 0; i < response.length; i++) {

            //Create jumbotron div for each detection point
            var detectionPointObj = response[i];
            var div = document.createElement("div");
            div.classList = "jumbotron";
            div.style.backgroundColor = "#eee";
            div.style.color = "#141414";

            //Create three divs for columns within the main div
            var div1 = document.createElement("div");
            div1.style.width = "25%";
            div1.style.cssFloat = "left";
            div1.style.marginTop = "-24px";

            var div2 = document.createElement("div");
            div2.style.width = "25%";
            div2.style.cssFloat = "left";
            div2.style.marginTop = "-24px";


            var div3 = document.createElement("div");
            div3.style.width = "25%";
            div3.style.cssFloat = "left";
            div3.style.marginTop = "-24px";

            var div4 = document.createElement("div");
            div4.style.width = "25%";
            div4.style.cssFloat = "right";
            div4.style.marginTop = "-24px";


            //Add Name
            var headerName = document.createElement("H3");
            headerName.innerText = detectionPointObj['Name'];
            headerName.style.textAlign = "center";

            var severityHeader = document.createElement("H4");
            severityHeader.style.marginTop = "-5px";
            severityHeader.style.color = "#b9bbbf";
            severityHeader.style.textAlign = "center";
            severityHeader.innerText = detectionPointObj['Severity'];

            div1.appendChild(headerName);
            div1.appendChild(severityHeader);

            //Add threshold
            var threshold = document.createElement("H3");
            threshold.innerText = detectionPointObj['Count'];
            threshold.style.textAlign = "center";
            div2.appendChild(threshold);

            //Add timelimit
            var timelimit = document.createElement("H3");
            timelimit.innerText = detectionPointObj['Time'];
            timelimit.style.textAlign = "center";
            div3.appendChild(timelimit);

            // Add response or responses
            var responseObject = detectionPointObj['Response'];

            if (responseObject.constructor === Array) {
                for (var resp=0; resp < responseObject.length; resp++) {

                    var responseHeader = document.createElement("H3"); // Create Response header
                    responseHeader.style.textAlign = "center";

                    if (responseObject[resp].includes("(")){ //If the response contains a time in brackets then take it and delete the brackets
                        var startposition = responseObject[resp].indexOf('(') + 1;
                        var endposition = responseObject[resp].indexOf(')');
                        var timeLength = responseObject[resp].substring(startposition, endposition);
                        var timeHeader = document.createElement("H4");
                        timeHeader.style.marginTop = "-5px";
                        timeHeader.style.color = "#b9bbbf";
                        timeHeader.style.textAlign = "center";
                        timeHeader.innerText = timeLength + " seconds";

                        var splitText = responseObject[resp].replace(responseObject[resp].substring(startposition-1, endposition+1), '');
                        responseHeader.innerText = splitText;

                        div4.appendChild(responseHeader);
                        div4.appendChild(timeHeader);
                    }
                    else
                    {
                        responseHeader.innerText = responseObject[resp];
                        div4.appendChild(responseHeader);
                    }


                }
            }
            else
            {
                var responseHeader = document.createElement("H3");
                responseHeader.innerText = responseObject;
                responseHeader.style.textAlign = "center";
                div4.appendChild(responseHeader);
            }

            var deleteIcon = document.createElement("input"); //<input type="image" src="{{ url_for('static', filename='images/plus.png') }}" id="newDP" class="custom-image">
            deleteIcon.type = "image";
            deleteIcon.src = "/static/images/close.png";
            deleteIcon.id = detectionPointObj['Name'];
            deleteIcon.classList="custom-image2";
            deleteIcon.onclick = function() { //Send a DELETE request

                var dp = JSON.stringify({"dpName" : $(this).attr("id")});

                var xhr = new XMLHttpRequest();
                var url = "http://localhost:5000/deleteDP";
                xhr.open("POST", url, true);
                xhr.setRequestHeader("Content-type", "application/json");
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        //alert(xhr.responseText);
                    }
                };
            xhr.send(dp);
                location.reload();

            };

            div.appendChild(deleteIcon);
            div.appendChild(div1);
            div.appendChild(div2);
            div.appendChild(div3);
            div.appendChild(div4);
            document.getElementById("main").appendChild(div);
        }
    }


