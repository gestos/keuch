<html>
<head>
<?php require ('vars.php'); ?> 

<script type="text/javascript">
var marken = <?php echo json_encode($ds_marken); ?>;
var aromen = <?php echo json_encode($ds_aromen); ?>;
var liquids = <?php echo json_encode($ds_liquids); ?>;
</script>
<script src='liqdb.js' defer></script>
<link rel="stylesheet" href="heller_style_neu.css">
<link rel="stylesheet" href="datenbank.css">
</head>
<body>

			<div class="header">
				<h1>Liquid-Datenbank</h1>
			</div>

<div class="small_table_div" style="float:left">
				<h2 class="small_table_div">Hersteller</h2>
<form method="post" name="manufacturers" action="vars.php" target="phpm">
<table id="herstellertabelle" class="smalltable borderlein">
<tr>
<th>Kürzel</th>
<th>Hersteller</th>
<th></th>
</table>
</form>
</div>

<!--
<div class="small_table_div" id="aromen" style="float:left">
<select id="aromaselect" onChange="load_aro(this)">
</select>
<select id="geschmack">
</select>
</div>
-->

<div class="small_table_div" style="float:left">
				<h2 class="small_table_div">Aromen</h2>
<table id="aromenliste" class="smalltable borderlein">
<tr></tr>
<tr>
<th>Hersteller</th>
<th>Geschmack</th>
<th></th>
<th></th>
</tr>

</table>
</div>

<div id="liquids" class="small_table_div">
				<h2 class="small_table_div">Liquids</h2>
<table id="liquidliste" class="smalltable borderlein">

</table>
</div>
<iframe id="phpm" name="phpm">
</iframe>

</body>
</html>
