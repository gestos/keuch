<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$server = "localhost";
$user = "keuch";
$pass = "fearless";
$dbase = "liquids_base";
// Create connection
// echo "db... ";
$conn = new mysqli($server, $user, $pass, $dbase);
// Check connection
if ($conn->connect_error) { die("Connection failed: " . $conn->connect_error); }
// echo "ok<br>";



if ($_SERVER["REQUEST_METHOD"] == "POST") {

	if (array_key_exists('del_man', $_POST)) {
		$to_delete =  $_POST['del_man'];
		$del_sql = "DELETE FROM Hersteller WHERE tag = '$to_delete'";

		if ($conn->query($del_sql) === TRUE) {
			echo "'$to_delete' was removed from db <br>";
		} else {
			echo "Error: " . $del_sql . "<br>" . $conn->error;
		}

	} elseif ($_POST['new_manu']) {
		$tag = $_POST['tag'];
		$firma = $_POST['firma'];

		if ($tag == '' || $firma == '') {
			echo "strings must not be empty";
		} 
		elseif (strlen($tag) > 3) {
			echo "tag must not be longer than 3 characters";
		}
		elseif (strlen($firma) > 50) {
			echo "firma must not be longer than 50 characters";
		}
		else {
			$sql = "INSERT INTO Hersteller (firma, tag) VALUES ('$firma', '$tag')";
			if ($conn->query($sql) === TRUE) {
				echo "New record for '$firma' created successfully";
			} else {
				echo "Error: " . $sql . "<br>" . $conn->error;
			}
		}

	} else {
		echo "no idea what this is <br>";
	}
}

// query for manufacturer db and turn into array
$obj_marken = $conn->query("select firma, tag from Hersteller order by firma asc") or die("Fehler: " . $conn->error);
// echo gettype($obj_marken)."<br>";
$ds_marken = $obj_marken->fetch_all(MYSQLI_ASSOC);
// echo gettype($ds_marken)."<br>";


// nach Häufigkeit sortiert wie hier: https://stackoverflow.com/questions/8467997/order-sql-query-records-by-frequency
$obj_aromen = $conn->query("select hersteller, geschmack from Aromen inner join ( select hersteller, count(1) as freq from Aromen group by 1 ) derived using (hersteller) order by derived.freq desc") or die("Fehler: " . $conn->error);
$ds_aromen = $obj_aromen->fetch_all(MYSQLI_ASSOC);

$obj_liquids = $conn->query("select * from Liquids") or die("Fehler: " . $conn->error);
$ds_liquids = $obj_liquids->fetch_all(MYSQLI_ASSOC);

?>
