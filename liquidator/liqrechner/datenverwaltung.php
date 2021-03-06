<html>
	<head>
		<title>Aromen/Liquid-Datenbank</title>
		<meta charset="UTF-8">
		<?php require ('vars.php'); ?> 

		<script type="text/javascript">
			var marken = <?php echo json_encode($ds_marken); ?>;
			var aromen = <?php echo json_encode($ds_aromen); ?>;
			var liquids = <?php echo json_encode($ds_liquids); ?>;
		</script>
		<script src='general.js' defer></script>
		<script src='liqdb.js' defer></script>
		<link id="style" rel="stylesheet" href="heller_style.css">
		<link rel="stylesheet" href="datenbank.css">
	</head>
	<body>

		<div class="header">
			<h1>Liquid-Datenbank</h1>
		</div>

		<div class="main_column">
			<div id="upper_part" class="large_table_div" style="float:left; clear:right">
				<div id="hersteller_div" class="small_table_div" style="float:left">
					<h2 class="headline">Hersteller</h2>

					<form method="post" name="manufacturers" action="vars.php" target="phpm">
						<!-- onSubmit="manual_reload()" -->  
						<table id="herstellertabelle" class="smalltable borderlein">
							<tr>
								<th>Tag</th>
								<th>Hersteller</th>
								<th></th>
						</table>
					</form>
				</div>

				<div id="aromen_div" class="small_table_div" style="float:left; clear:right">
					<h2 class="headline">Aromen</h2>
					<table id="aromenliste" class="smalltable borderlein">
						<tr></tr>
						<tr>
							<th>Marke</th>
							<th>Aroma</th>
							<th>ml</th>
							<th></th>
							<th></th>
						</tr>

					</table>
				</div>
				<iframe id="phpm" name="phpm" class="errorlog">
				</iframe>
			</div>
		</div>

			<div id="liquids" class="large_table_div">
				<h2 class="headline">Liquids</h2>
				<table id="liquidliste" class="smalltable borderlein">

				</table>
			</div>

			<div id="zumCalc" class="db_link">
				<a href="index.php">zum Rechner</a>
					<span class="styleswtch">style: <input type="button" class="pushbuttonr" style="width:50px" value="bright" onclick="styleswitch(this)" />
					</span>
			</div>
	</body>
</html>
