<html>
	<head>
		<meta charset="UTF-8">
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
	</body>

</html>
