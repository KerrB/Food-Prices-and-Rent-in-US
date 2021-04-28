<?php
$mysqli = new mysqli("mysql.eecs.ku.edu", "kerr712", "basohR7h", "kerr712");

/* check connection */
if ($mysqli->connect_errno) {
    printf("Connect failed: %s\n", $mysqli->connect_error);
    exit();
}

$query = "SELECT CRUISENUM FROM CRUISE";
if ($result = $mysqli->query($query)) {
     /* fetch associative array */
     while ($row = $result->fetch_assoc()) {
        echo $row["CRUISENUM"] . "<br>";
    }


    /* free result set */
    $result->free();
}

/* close connection */ 
$mysqli->close();
?>
