<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$server = "localhost";$user = "keuch";$pass = "fearless";$dbase = "liquids_base";
$conn = new mysqli($server, $user, $pass, $dbase);
if ($conn->connect_error) { die("Connection failed: " . $conn->connect_error); }

// query for manufacturer db and turn into array
$obj_marken = $conn->query("select firma, tag from Hersteller order by firma asc") or die("Fehler: " . $conn->error);
$ds_marken = $obj_marken->fetch_all(MYSQLI_ASSOC);
// nach Häufigkeit sortiert wie hier: https://stackoverflow.com/questions/8467997/order-sql-query-records-by-frequency
$obj_aromen = $conn->query("select hersteller, geschmack, id, hash from Aromen inner join ( select hersteller, count(1) as freq from Aromen group by 1 ) derived using (hersteller) order by derived.freq desc") or die("Fehler: " . $conn->error);
$ds_aromen = $obj_aromen->fetch_all(MYSQLI_ASSOC);

$obj_liquids = $conn->query("select * from Liquids order by Datum desc") or die("Fehler: " . $conn->error);
$ds_liquids = $obj_liquids->fetch_all(MYSQLI_ASSOC);
function saveLiquid($param, $conn) {
	//$server = "localhost"; $user = "keuch";	$pass = "fearless";	$dbase = "liquids_base";
	//$conn = new mysqli($server, $user, $pass, $dbase);
	//if ($conn->connect_error) { die("Connection failed: " . $conn->connect_error); }

	// string escaping
	foreach (array_keys($param) as &$mykey) {
		$param[$mykey] = $conn->real_escape_string($param[$mykey]);
	}
	// set empty strings to NULL
	$LiqKeys = array('aro1_name', 'aro2_name', 'aro3_name', 'aro4_name', 'aro5_name', 'aro1_proz', 'aro2_proz', 'aro3_proz', 'aro4_proz', 'aro5_proz', 'datum', 'pg_liq', 'vg_liq', 'nic', 'liquidname', 'aroG_proz', 'id');
	foreach($LiqKeys as $key) {
		if($param[$key] == '' || ! $param[$key]) {
			$param[$key] = null;
		}
	}
	// rename columns
	$param["Datum"] = $param["datum"];	$param["Name"] = $param["liquidname"];	$param["pg_pct"] = $param["pg_liq"];	$param["vg_pct"] = $param["vg_liq"];	$param["nic_mg"] = $param["nic"];
	$param["AromaG_pct"] = $param["aroG_proz"];	$param["Aroma1"] = $param["aro1_name"];	$param["Aroma1_pct"] = $param["aro1_proz"];	$param["Aroma2"] = $param["aro2_name"];
	$param["Aroma2_pct"] = $param["aro2_proz"];	$param["Aroma3"] = $param["aro3_name"];	$param["Aroma3_pct"] = $param["aro3_proz"];	$param["Aroma4"] = $param["aro4_name"];
	$param["Aroma4_pct"] = $param["aro4_proz"];	$param["Aroma5"] = $param["aro5_name"];
	$param["Aroma5_pct"] = $param["aro5_proz"];
	// unset former column names
	foreach($LiqKeys as $key) {
		unset ($param[$key]);
	}
	// generate hash from relevant columns
	$liqhash = sha1($param['Aroma1'].$param['Aroma1_pct'].$param['Aroma2'].$param['Aroma2_pct'].$param['Aroma3'].$param['Aroma3_pct'].$param['Aroma4'].$param['Aroma4_pct'].$param['Aroma5'].$param['Aroma5_pct']);
	echo $liqhash;
	// sumbit to DB
	$stmt = $conn->prepare("INSERT INTO Liquids (hash, Datum, Name, pg_pct, vg_pct, nic_mg, AromaG_pct, Aroma1, Aroma1_pct, Aroma2, Aroma2_pct, Aroma3, Aroma3_pct, Aroma4, Aroma4_pct, Aroma5, Aroma5_pct) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
	$stmt->bind_param("sssddddsdsdsdsdsd",$liqhash, $param['Datum'], $param['Name'], $param['pg_pct'], $param['vg_pct'], $param['nic_mg'], $param['AromaG_pct'], $param['Aroma1'], $param['Aroma1_pct'], $param['Aroma2'], $param['Aroma2_pct'], $param['Aroma3'], $param['Aroma3_pct'], $param['Aroma4'], $param['Aroma4_pct'], $param['Aroma5'], $param['Aroma5_pct']);
	$stmt->execute();
	if($stmt->error) {
		printf("Error: %s.\n", $stmt->error);
	}
	else {
		printf('<div class="floater borderlein">');
		printf("Liquids zu DB hinzugefügt <br>");
		printf('<a href="datenverwaltung.php" target="_blank">Datenbank mit Liquids + Herstellern bearbeiten</a>');
		printf("</div>");
	}
	$stmt->close();
}
function add_flavour($conn, $postarray) {
	$manmap = json_decode($_POST['hidden_map'], true);
	// string escaping
	foreach (array_keys($postarray) as &$mykey) {
		$postarray[$mykey] = $conn->real_escape_string($postarray[$mykey]);
		$postarray[$mykey] = ucwords($postarray[$mykey]);
	}

	$flavor = rtrim($postarray['Geschmack']);
	$brand = mb_strtolower(rtrim($postarray['brand']), 'UTF-8');
	$brandname = rtrim($manmap[$brand]);

	echo "flavor ".$flavor;
	echo "brand ".$brand;
	echo "brandname ".$brandname;

	if ($flavor == '' || $brand == '') {
		echo "strings must not be empty";
	} 
	elseif (strlen($flavor) > 50 || strlen($brandname) > 50) {
		echo "input must not be longer than 50 characters";
	}
	else {
		$aro_hash = sha1(preg_replace('!\s+!', ' ',mb_strtolower($flavor.$brandname, 'UTF-8'))); // lowercasing and so on is mostly for the hash
		$sql = "INSERT INTO Aromen (hersteller, geschmack, hash) VALUES ('$brandname', '$flavor', '$aro_hash')";
		if ($conn->query($sql) === TRUE) {
			echo "<script>console.log(this[0]);</script>";
			echo "New record for '$brand' '$flavor' created successfully";
		} else {
			echo "Error: " . $sql . "<br>" . $conn->error;
		}
	}
			//header("Location: ?page=successfulsending");
      //	header("Location: http://liq.keuch/datenverwaltung.php");
}
function add_manufacturer($conn, $postarray) {
	// string escaping
	foreach (array_keys($postarray) as &$mykey) {
		$postarray[$mykey] = $conn->real_escape_string($postarray[$mykey]);
	}
	echo $postarray['tag'];
	echo $postarray['firma'];
	$postarray['tag'] = mb_strtolower($postarray['tag']);
	$postarray['firma'] = ucwords(mb_strtolower($postarray['firma']));
	$tag = $postarray['tag'];
	$firma = $postarray['firma'];

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
		$query = "DELETE FROM Aromen WHERE id = ?";
		$query = "INSERT INTO Hersteller (firma, tag) VALUES (?, ?)";
		/* prepare statement */
		if ($stmt = $conn->prepare($query)) {
			/* Bind variable for placeholder */
			$stmt->bind_param("ss", $firma, $tag);
			/* execute statement */
			if ($stmt->execute()) {
				echo "New record for '$firma' created successfully<br>";
				printf("rows created: %d\n", $stmt->affected_rows);
				/* close statement */
			}
			else {
				echo "Error: " . $sql . "<br>" . $conn->error;
			}
			$stmt->close();
		}
	}
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
		elseif (array_key_exists('del_flav', $_POST)) {
			$delete_id =  $_POST['aroma_id'];
			$query = "DELETE FROM Aromen WHERE id = ?";
			/* prepare statement */
			if ($stmt = $conn->prepare($query)) {
				/* Bind variable for placeholder */
				$stmt->bind_param("i", $delete_id);
				/* execute statement */
				$stmt->execute();
				printf("rows deleted: %d\n", $stmt->affected_rows);
				/* close statement */
				$stmt->close();
			}
		} 
		elseif (array_key_exists('jsonified',$_POST)) {
			$json_content = json_decode($_POST['jsonified'], true);
			foreach ($json_content as &$liq_array) {
				saveLiquid($liq_array, $conn);
			}

		}
		elseif (array_key_exists('new_manu',$_POST)) {
			add_manufacturer($conn, $_POST);
		}
		elseif (array_key_exists('new_flav',$_POST)) {
			add_flavour($conn, $_POST);
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
// header("Refresh: 0; url=index.php");
//$page = $_SERVER['PHP_SELF'];
//$sec = "10";
//header("Refresh: $sec; url=$page");
// echo '<meta http-equiv="refresh" content="0" url=http://liq.keuch/datenverwaltung.php>';

?>

