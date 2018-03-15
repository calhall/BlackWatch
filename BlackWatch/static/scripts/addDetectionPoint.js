var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("newDP");

//Submit detection point button
var submitbtn = document.getElementById("add");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

submitbtn.onclick = function () {
    var name = document.getElementById("name").value;
    var count = document.getElementById("count").value;
    var period = document.getElementById("period").value;
    var responses = document.getElementById("response").value;
    var severity = document.getElementById("severity");
    var severityChoice = severity.options[severity.selectedIndex].text;
    var correctFormat = false;

    if (name == "" || count == "" || period == "" || responses == "")
    {
        alert("Please fill in all fields.");
    }
    else
    {
        if (isNaN(count))
        {
            alert("Numbers only for event count")
        }
        else
        {
            if (count.indexOf('+') > -1)
            {
                count.replace('+', '');
            }
            else if (count.indexOf ('-') > -1)
            {
                count.replace('-', '');
            }
            correctFormat = true;

        }

        if (isNaN(period))
        {
            alert("Numbers only for time period")
        }
        else
        {
            if (period.indexOf('+') > -1)
            {
                period.replace('+', '');
            }
            else if (period.indexOf ('-') > -1)
            {
                period.replace('-', '');
            }
            correctFormat = true;
        }

        if (correctFormat===true) {
            addDetectionPoint(name, count, period, responses, severityChoice);
        }
    }
}

function addDetectionPoint(name, count, period, responses, severityChoice) {

    var dp = JSON.stringify({"dpName" : name, "Limit" : count, "Period" : period, "Response" : responses, "Severity" : severityChoice});

    var xhr = new XMLHttpRequest();
    var url = "http://localhost:5000/adddetectionpoint";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            alert(xhr.responseText);
        }
    };
xhr.send(dp);
location.reload();
}
