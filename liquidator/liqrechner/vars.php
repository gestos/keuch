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
$connection = mysqli_connect($server, $user, $pass, $dbase);
// Check connection
if ($conn->connect_error) { die("Connection failed: " . $conn->connect_error); }
// echo "ok<br>";


/*if ($_SERVER["REQUEST_METHOD"] == "POST") {
	print_r($_POST);
}
 */
function shitHead($param) {
	$server = "localhost";
	$user = "keuch";
	$pass = "fearless";
	$dbase = "liquids_base";
	//$connection = mysqli_connect($server, $user, $pass, $dbase);

	$columns = implode(", ",array_keys($param));
	$param["Datum"] = $param["datum"];
	$param["Name"] = $param["liquidname"];
	$param["pg_pct"] = $param["pg_liq"];
	$param["vg_pct"] = $param["vg_liq"];
	$param["nic_mg"] = $param["nic"];
	$param["AromaG_pct"] = $param["aroG_proz"];
	$param["Aroma1"] = $param["aro1_name"];
	$param["Aroma1_pct"] = $param["aro1_proz"];
	$param["Aroma2"] = $param["aro2_name"];
	$param["Aroma2_pct"] = $param["aro2_proz"];
	$param["Aroma3"] = $param["aro3_name"];
	$param["Aroma3_pct"] = $param["aro3_proz"];
	$param["Aroma4"] = $param["aro4_name"];
	$param["Aroma4_pct"] = $param["aro4_proz"];
	$param["Aroma5"] = $param["aro5_name"];
	$param["Aroma5_pct"] = $param["aro5_proz"];
	unset ($param["aro1_name"]);
	unset ($param["aro2_name"]);
	unset ($param["aro3_name"]);
	unset ($param["aro4_name"]);
	unset ($param["aro5_name"]);
	unset ($param["aro1_proz"]);
	unset ($param["aro2_proz"]);
	unset ($param["aro3_proz"]);
	unset ($param["aro4_proz"]);
	unset ($param["aro5_proz"]);
	unset ($param["datum"]);
	unset ($param["pg_liq"]);
	unset ($param["vg_liq"]);
	unset ($param["nic"]);
	unset ($param["liquidname"]);
	unset ($param["aroG_proz"]);
	unset ($param["id"]);

	$connection = new mysqli($server, $user, $pass, $dbase);
	if($connection->connect_error) {
		  exit('Error connecting to database'); //Should be a message a typical user could understand in production
	}

	foreach (array_keys($param) as &$mykey) {
		$param[$mykey] = $connection->real_escape_string($param[$mykey]);
	}

	$columns = implode(", ",array_keys($param));
	echo $columns."<br>";
	$values  = implode(", ",array_values($param));
	echo $values."<br>";

	$stmt = $connection->prepare("INSERT INTO Liquids (Datum, Name, pg_pct, vg_pct, nic_mg, AromaG_pct, Aroma1, Aroma1_pct, Aroma2, Aroma2_pct, Aroma3, Aroma3_pct, Aroma4, Aroma4_pct, Aroma5, Aroma5_pct) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
	$stmt->bind_param("ssddddsdsdsdsdsd", $param['Datum'], $param['Name'], $param['pg_pct'], $param['vg_pct'], $param['nic_mg'], $param['AromaG_pct'], $param['Aroma1'], $param['Aroma1_pct'], $param['Aroma2'], $param['Aroma2_pct'], $param['Aroma3'], $param['Aroma3_pct'], $param['Aroma4'], $param['Aroma4_pct'], $param['Aroma5'], $param['Aroma5_pct']);
	$stmt->execute();
	$stmt->close();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {

	if (array_key_exists('del_man', $_POST)) {
		$to_delete =  $_POST['del_man'];
		$del_sql = "DELETE FROM Hersteller WHERE tag = '$to_delete'";

		if ($conn->query($del_sql) === TRUE) {
			echo "'$to_delete' was removed from db <br>";
		} else {
			echo "Error: " . $del_sql . "<br>" . $conn->error;
		}

	} 
	elseif (array_key_exists('jsonified',$_POST)) {
		echo "oho, ein paar neue liquids!<br>";
		$json_content = json_decode($_POST['jsonified'], true);
		foreach ($json_content as &$liq_array) {
			shitHead($liq_array);
		}

	}
	elseif (array_key_exists('new_manu',$_POST)) {
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

	}
	elseif (array_key_exists('new_liq',$_POST)) {
		echo "new liquid to add";
		print_r($_POST);
	}
	else {
		echo "no idea what this is <br>";
		print_r($_POST);
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

$obj_liquids = $conn->query("select * from Liquids order by Datum desc") or die("Fehler: " . $conn->error);
$ds_liquids = $obj_liquids->fetch_all(MYSQLI_ASSOC);
?>

