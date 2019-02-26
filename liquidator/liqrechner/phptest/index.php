<html>
<head>
<?php
require ('vars.php');
?> 

<script type="text/javascript">
var marken = <?php echo json_encode($ds_marken); ?>;
var aromen = <?php echo json_encode($ds_aromen); ?>;
var liquids = <?php echo json_encode($ds_liquids); ?>;
</script>
<script src='liqdb.js' defer></script>
</head>
<body>

<table id="herstellertabelle" style="float:left">
<tr>
<th>Kürzel</th>
<th>Hersteller</th>
<th></th>
</tr>

<tr colspan="3" id="manuf_plus">
<td><a id="add1" onclick="toggle('in_row')">+</a></td>
</tr>

<tr id="in_row" style="visibility:collapse">
<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
<td><input id="in_tag" type="text" name="tag"></td>
<td><input id="in_fir" type="text" name="firma"></td>
<td><input name="new_manu" type="submit" value="add"></td>
</form>
</tr>
</table>

<div id="aromen" style="float:left">
<select id="aromaselect" onChange="load_aro(this)">
</select>
<select id="geschmack">
</select>
</div>

<div>
<table id="aromenliste">
<tr colspan="2"><td>komplette Liste</td></tr>
<tr>
<th>Hersteller</th>
<th>Geschmack</th>
</tr>

</table>
</div>

<div id="liquids">
<table id="liquidliste">

</table>




</div>

</body>
</html>
