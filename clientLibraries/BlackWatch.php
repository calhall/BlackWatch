<?php
/**
 * Created by PhpStorm.
 * User: calum
 * Date: 24/02/2018
 * Time: 11:30
 */
function sendEvent($dpName, $description){

    //Gain session information --------------------------------------
    try
    {
        $dvwaSession = $_SESSION[ 'dvwa' ];
    }
    catch(Exception $exception)
    {
        $dvwaSession = null;
    }
    try
    {
        $username = $dvwaSession[ 'username' ];
    }
    catch(Exception $exception)
    {
        $username = "Anonymous";
    }
    try
    {
        $ipAddress = $_SERVER['REMOTE_ADDR'];
        if ($ipAddress=="::1")
        {
            $ipAddress = "127.0.0.1";
        }
    }
    catch(Exception $exception)
    {
        $ipAddress = "0.0.0.0";
    }
    try
    {
        $sessionID = $_SESSION[ 'session_token' ];
    }
    catch(Exception $exception)
    {
        $sessionID = "Unknown";
    }
    //---------------------------------------------------------------


    //Create the event using the information given ------------------
    //The formatting of events is very important, check the README.md for further details ----------

    $User = array("username" => $username, "ipAddress" => $ipAddress, "sessionID" => $sessionID);
    $DetectionPoint = array("dpName" => $dpName, "description" => $description);
    $Time = date (c);
    $Event = array("User" => $User, "DetectionPoint" => $DetectionPoint, "Time" => $Time);

    $data_string = json_encode($Event);

    //Send the event in json format
    //By default this is sent to the url below, this is a default local flask server
    //Change this to fit your environment suitable

    $ch = curl_init('http://127.0.0.1:5000/addevent');
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Content-Length: ' . strlen($data_string))
    );

    $result = curl_exec($ch);
    curl_close($ch);


    //The $result variable can be checked to ensure the event has been recieved successfully

    getResponse();
}


function getResponse()
{


    try
    {
        $dvwaSession = $_SESSION[ 'dvwa' ];
    }
    catch(Exception $exception)
    {
        $dvwaSession = null;
    }

    try
    {
        $username = $dvwaSession[ 'username' ];
    }
    catch(Exception $exception)
    {
        $username = "Anonymous";
    }
    try
    {
        $sessionID = $_SESSION[ 'session_token' ];
    }
    catch(Exception $exception)
    {
        $sessionID = "Unknown";
    }


    $query = http_build_query([
        'username' => $username,
        'sessionID' => $sessionID
    ]);


    $curl = curl_init();
// Set some options - we are passing in a useragent too here
    curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => 'http://localhost:5000/getResponses?'.$query,
        CURLOPT_USERAGENT => 'Test'
    ));
// Send the request & save response to $resp
    $resp = curl_exec($curl);
// Close request to clear up some resources
    curl_close($curl);
    $responseArray = json_decode($resp, true);

    //echo $resp;
    for ($i = 0; $i < count($responseArray); $i++)
    {
        $item = $responseArray[$i];
        $sessiontokill = $item['SessionID'];
        //echo "----".$item['Response']."----";
        if ($item['Response']=="Logout") // THERE IS A SPACE FOR SOME REASON?
        {

            session_unset();
            session_destroy();

            header("Location: ../../login.php");
        }
        else if ($item['Response']=='Warn User')
        {
            echo '<script type="text/javascript">alert("Your activity is being watched, stop attacking this application.");</script>';
        }
        else if ((strpos($item['Response'], 'Redirect')) !== false)
        {
            $splitString = explode(' ',$item['Response']);
            $redirectURL = $splitString[1];
            header('Location: '.$redirectURL);
        }
        else if ($item['Response']=='False output')
        {

            echo "ID: 1";
            echo "<br>";
            echo "Username = JackRoss1877";
            echo "<br>";
            echo "Password = 75170fc230cd88f32e475ff4087f81d9";
        }
    }

}

function getSQLCommands(){
    $sqlCommands = array("ALTER TABLE", "AND", "AS", "AVG", "BETWEEN", "COUNT", "CREATE TABLE", "DELETE", "GROUP BY", "INNER JOIN",
        "INSERT", "LIKE", "LIMIT", "MAX", "MIN", "OR", "ORDER BY", "OUTER JOIN", "ROUND", "SELECT", "SUM", "UPDATE",
        "WHERE");
    return $sqlCommands;
}

function getXSSCommands(){
    $xssCommands = array("script", "img", "alert("); // Add more to make this more effective
    return $xssCommands;
}
?>
