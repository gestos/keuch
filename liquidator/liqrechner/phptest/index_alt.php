<!DOCTYPE html>
<html lang="de">
	<head>
<?php
require ('vars.php');
?> 
		<title>Liquid- und Aromenrechner</title>
		<meta charset="UTF-8">

<script type="text/javascript">
var marken = <?php echo json_encode($ds_marken); ?>;
var aromen = <?php echo json_encode($ds_aromen); ?>;
var liquids = <?php echo json_encode($ds_liquids); ?>;
</script>
				<script src='liqdb.js' defer></script>
				<script src='new_liq.js' defer></script>
				<script src='etiketten.js' defer></script>
				<link rel="stylesheet" href="heller_style_neu.css">
	</head>
	<body>
		<div id="outercontainer">
			<div class="header">
				<h1>Liquidrechner</h1>
			</div>
			<div id="main_column">
				<div id="einleitung" class="floater borderlein">
					<h2>Hinweise zur Benutzung</h2>
					<p><a id="klapper" class="klapper" onclick="collapse('erklaerbaer')">klick zum Ein/Ausblenden</a></p>
					<div id="erklaerbaer" >
						<p>Der Liquidrechner hat 3 Abschnitte, die "aufeinander aufbauen" ;-). Der erste Rechner soll beim Zusammenmischen von Ausgangsstoffen helfen, wenn man also eine 
						Basis ohne Nikotin aus reinem VG und PG zusammenkippen möchte. Hier kann man entweder die gewünschten Prozentanteile und die gewünschte Ergebnismenge in ml angeben,
						oder mit dem "switch" Knöpfchen umstellen und Mengenangaben der Ausgangsstoffe eingeben und sich dann die %-Mischung anzeigen lassen.</p>
						<p>Der zweite Rechner berechnet einem, wieviel Nikotinbasis man mit (s)einer Ausgangsbasis (z.B. der im ersten Schritt angemischten...) zusammenkippen muß, um auf eine
						gewünschte Nikotinmenge zu mischen. Hier kann man auch wieder mit dem "switch" Knöpfchen umschalten und entweder einfach das Mischverhältnis anzeigen lassen, oder unten
						ein gewünschtes Verhältnis angeben und sich anzeigen lassen, welches Verhältnis die Nullerbase haben müßte, um beim gewünschten Nikotingehalt auf das gewünschte Mischverhältnis
						zu kommen. Ich gehe davon aus, daß die Bunkerbase in ihrer Zusammensetzung fix ist.</p>
						<p>Im dritten Rechner gibt man an, welches Grundliquid (z.B. das im vorangegangenen Rechner zusammengkippte...) man hat und wie viel Aroma man beigeben will und bekommt dann
						die jeweils benötigten ml angezeigt. Auch hier kann man den Rechenweg umkehren und unten das gewünschte Mischverhältnis vorgeben, um sich oben anzeigen zu lassen, welche
						Grundwerte man bräuchte, um am Ende z.B. ein Liquid, das, nach Beigabe des Aromas, genau ein Verhältnis 70/30 bei X mg Nikotin hat, zu bekommen.</p>
						<p>Im letzten Rechner kann man dann noch seine Aromakomposition zusammenrechnen und z.B. als Menge ein Fläschchen a 50ml vorgeben.</p>
						<p>Die Werte der einzelnen Rechner können jeweils in beide Richtungen übertragen werden; der Hintergedanke war, daß ich ein aromatisiertes Liquid mit einem genauen
						Mischverhältnis PG/VG/Zusatz bekommen wollte, und mich von dort aus rückwärts zu den reinen Ausgangsstoffen zurückrechnen kann ;), da die Aromen und Bunkerbasen ja immer
						die % für PG vorgeben.</p>
						<p>Das Feld "Alk" kann genutzt werden, wenn man in der Art der "Tradizionale"-Basis Wasser oder Alkohol beigeben möchte, oder zB für Menthol, das ja auch in Alkohol
						gelöst sein kann</p>
						<table class="grund klein">
							<tr>
								<td>Legende</td>
								<td><input readonly /></td><td>ist ein reines Ausgabefeld, in dem Ergebnisse angezeigt werden</td>
								<td><input /></td><td>ist ein normales Eingabefeld</td>
							</tr>
							<tr>
								<td></td>
								<td><input class="failfeld" /></td><td>Feld muß noch geändert oder befüllt werden, um rechnen zu können</td>
								<td><input class="okfeld" /></td><td>In diesen Feldern sind die Werte o.k.</td>
							</tr>
							<tr>
								<td></td>
								<td><input class="grund ausgangswert"></td><td>Wert aus diesen Feldern werden in...</td>
								<td><input class="grund zielwert"></td><td>...diese Felder übertragen, wenn man aufs Übertragen-knöpfchen drückt</td>
							</tr>
						</table>
					</div>
				</div>
				<div id="grundstoffe" class="floater borderlein">
					<h2>Nullerbasis aus Grundstoffen mischen</h2>
					<table class="grund" style="font-size: 12px">
						<tr>
							<th class="left">Grundstoff</th> <th>PG</th> <th>VG</th> <th>Alk</th> <th>Menge</th>
						</tr>
						<tr id="pg">
							<td class="left">PG</td>
							<td>100%</td>
							<td></td>
							<td></td>
							<td><input id="pg_rein" readonly />ml</td>
						</tr>
						<tr id="vg">
							<td class="left">VG</td>
							<td></td>
							<td>100%</td>
							<td></td>
							<td><input id="vg_rein" readonly />ml</td>
						</tr>
						<tr id="alk">
							<td class="left">Alk</td>
							<td></td>
							<td></td>
							<td>100%</td>
							<td><input id="alkrein" readonly />ml</td>
						</tr>
						<tr id="zielbase">
							<td class="left">Mischung</td>
							<td><input id="pgz"  onchange="chkgrund()" />%</td>
							<td><input id="vgz"  onchange="chkgrund()" />%</td>
							<td><input id="alkz"  onchange="chkgrund()" />%</td>
							<td><input id="mlz"  onchange="chkgrund()" />ml</td>
						</tr>
						<tr>
							<td><label>switch<input id="switcher1" class="cbinput" type="checkbox" onchange="switchgrund()"></label></td>
							<td colspan="4"><input id="go1" type="button" value="berechnen" disabled onclick="calc_grund()" /></td>
						</tr>
					</table>
				</div>
				<div id="zwischenschritt" class="floater">
					<h2>Werte übernehmen</h2>
					<input id="slider1" class="slidesmall" type="range" min="0" max="2" step="1" value="1" oninput="slideopt(this)" />
					<label id="slider1_label" class="schiebelabel" for="slider1">-</label>
					<input id="ubertrag1" class="pushbutton" type="button" value="übernehmen" disabled  onclick="ubernehm(this)" />
				</div>
				<div id="nikotinmische" class="floater borderlein">
					<h2>Nullerbasis mit Nikotinbasis mischen</h2>
					<table id="basen" class="grund" style="font-size: 12px;" >
						<tr>
							<th>Base</th><th>PG</th><th>VG</th><th>Alk</th><th>Nic./ml</th><th>Menge</th>
						</tr>
						<tr id="misch_nuller">
							<td>Nullerbase</td>
							<td><input id="pgb1"  onblur="chkvalid()" />%</td>
							<td><input id="vgb1"  onblur="chkvalid()" />%</td>
							<td><input id="alk1"  onblur="chkvalid()" />%</td>
							<td><input  value="0" readonly />mg</td>
							<td><input id="ml1"  readonly />ml</td>
						</tr>
						<tr id="base2">
							<td>Bunkerbase</td>
							<td><input id="pgb2"  onblur="chkvalid()" />%</td>
							<td><input id="vgb2"  onblur="chkvalid()" />%</td>
							<td><input id="alk2"  onblur="chkvalid()" />%</td>
							<td><input id="nic2"  onblur="chkvalid()" />mg</td>
							<td><input id="ml2"  readonly />ml</td>
						</tr>
						<tr id="misch_ziel">
							<td>Mischung</td>
							<td><input id="pgbz"  onblur="chkvalid()" readonly />%</td>
							<td><input id="vgbz"  onblur="chkvalid()" readonly />%</td>
							<td><input id="alkz1" onblur="chkvalid()" readonly />%</td>
							<td><input id="nicz" class="zielfeld"  onblur="chkvalid()" />mg</td>
							<td><input id="mlliq" class="zielfeld" onblur="chkvalid()" />ml</td>
						</tr>
						<tr>
							<td><label>switch<input id="switcher2" class="cbinput" type="checkbox" onchange="switch2()"></label></td>
							<td colspan="5"><input type="button" id="go" value="berechnen" onclick="calculate_liq()" disabled /></td>
						</tr>
					</table>
				</div>
				<!-- ##### Werte von Nikotinmischung nach Aromaliquid und vice versa ##### -->
				<div id="zwischenschritt2" class="floater">
					<h2>Werte übernehmen</h2>
					<input id="slider2" class="slidesmall" type="range" min="0" max="2" step="1" value="1" oninput="slideopt(this)" />
					<label id="slider2_label" class="schiebelabel" for="slider2">-</label>
					<input id="ubertrag2" class="pushbutton" type="button" value="übernehmen" disabled  onclick="ubernehm(this)" />
				</div>
				<!-- ##### Aromaliquid ##### -->
				<div id="Aromatisierung" class="floater borderlein">
					<h2>Nikotinliquid aromatisieren</h2>
					<table id="aroma" class="grund" style="font-size: 12px;" >
						<tr>
							<th>Base</th><th>PG</th><th>VG</th><th>Alk</th><th>Nic./ml</th><th>Aroma</th><th>Menge</th>
						</tr>
						<tr id="Liq3">
							<td>Basis-Liquid</td>
							<td><input id="pg_3"  onblur="chkvalid2()" />%</td>
							<td><input id="vg_3"  onblur="chkvalid2()" />%</td>
							<td><input id="alk3"  onblur="chkvalid2()" />%</td>
							<td><input id="nic3"  onblur="chkvalid2()" />mg</td>
							<td><input value="0" readonly />%</td>
							<td><input id="ml3"  readonly />ml</td>
						</tr>
						<tr id="Aroma0">
							<td>Aroma</td>
							<td><input id="pg_4"  onblur="chkvalid2()" />%</td>
							<td><input id="vg_4"  onblur="chkvalid2()" />%</td>
							<td><input id="alk4"  onblur="chkvalid2()" />%</td>
							<td><input id="nic4" value="-" readonly />mg</td>
							<td><input id="arpct_4" value="-"  readonly />%</td>
							<td><input id="ml4"  readonly />ml</td>
						</tr>
						<tr id="Ergebnis3">
							<td>fertiges Liquid</td>
							<td><input id="pg_5"  onblur="chkvalid2()" readonly />%</td>
							<td><input id="vg_5"  onblur="chkvalid2()" readonly />%</td>
							<td><input id="alk_5"  onblur="chkvalid2()" readonly />%</td>
							<td><input id="nic_5"  onblur="chkvalid2()" readonly />mg</td>
							<td><input id="arpct_5" class="zielfeld"  onblur="chkvalid2()" />%</td>
							<td><input id="ml_5" class="zielfeld"  onblur="chkvalid2()" />ml</td>
						</tr>
						<tr>
							<td><label>switch<input id="switcher3" class="cbinput" type="checkbox" onchange="switch3()"></label></td>
							<td colspan="6"><input type="button" id="go2" value="berechnen" onclick="calculate_liq2()" disabled /></td>
						</tr>
					</table>
				</div>
				<!-- ##### Werte von Aromaliquid nach Komposition übernehmen ##### -->
				<div id="zwischenschritt3" class="floater">
					<h2>Werte übernehmen</h2>
					<input id="slider3" class="slidesmall" type="range" min="0" max="2" step="1" value="1" oninput="slideopt(this)" />
					<label id="slider3_label" class="schiebelabel" for="slider3">-</label>
					<input id="ubertrag3" class="pushbutton" type="button" value="übernehmen" disabled  onclick="ubernehm(this)" />
				</div>
				<!-- ##### Aromenkomposition ##### -->
				<div id="Aromenkomposition" class="floater borderlein">
					<h2>Aromen komponieren</h2>
					<table class="kopf grund" style="font-size: 12px;" >
						<tr>
							<td>Menge:</td>
							<td><input id="einzelmenge" size="3" onblur="chk100_2()" />ml</td>
							<td></td>
							<td></td>
						</tr>
						<tr>
							<td>Anteil Aroma:</td>
							<td><input id="aromagesamt" size="3" onblur="chk100_2()" />%</td>
							<td></td>
							<td></td>
						</tr>
					</table>
					<table id="komponieren" class="grund" style="font-size: 12px;" >
						<tr>
							<td>Aroma 1:</td>
							<td class="aromaname"><input id="ar1" onblur="chk100_2()" placeholder="Erdbeere FA" /></td>
							<td><input id="aroma1pct" class="arpct" size="3" onblur="chk100_2()" />%</td>
							<td><input id="aroma1ml" class="arml" size="3" readonly />ml</td>
						</tr>
						<tr>
							<td>Aroma 2:</td>
							<td class="aromaname"><input id="ar2" onblur="chk100_2()" placeholder="Vanille Cap"/></td>
							<td><input id="aroma2pct" class="arpct"  size="3" onblur="chk100_2()" />%</td>
							<td><input id="aroma2ml" class="arml" size="3" readonly />ml</td>
						</tr>
						<tr>
							<td>Aroma 3:</td>
							<td class="aromaname"><input id="ar3" onblur="chk100_2()" placeholder="Haselnuss FA"/></td>
							<td><input id="aroma3pct" class="arpct"  size="3" onblur="chk100_2()" />%</td>
							<td><input id="aroma3ml" class="arml" size="3" readonly />ml</td>
						</tr>
						<tr>
							<td>Aroma 4:</td>
							<td class="aromaname"><input id="ar4" onblur="chk100_2()" placeholder="Kirsche Ina"/></td>
							<td><input id="aroma4pct" class="arpct"  size="3" onblur="chk100_2()" />%</td>
							<td><input id="aroma4ml" class="arml" size="3" readonly />ml</td>
						</tr>
						<tr>
							<td>Aroma 5:</td>
							<td class="aromaname"><input id="ar5" onblur="chk100_2()" placeholder="Gurke FA" /></td>
							<td><input id="aroma5pct" class="arpct"  size="3" onblur="chk100_2()" />%</td>
							<td><input id="aroma5ml" class="arml" size="3" readonly />ml</td>
						</tr>
						<tr>
							<td></td>
							<td>Summe:</td>
							<td><input id="sum" size="3" readonly />%</td>
							<td><input id="aromagesamtml" size="3" readonly />ml</td>
						</tr>
						<tr>
							<td><input id="shooter" class="pushbuttonr" type="button" value="Etikett erstellen" onclick="shoot()" /></td>
						</tr>
					</table>
<p>Druckansicht anpassen / Felder streichen ; Verwaltungsseite gestalten + liquid-delete</p>
				</div>
				<div id="etiketten" class="floater borderlein">
					<h2>Labels</h2>

					<div id="etikettenliste">
					</div>
					<input class="pushbuttonr" type="button" value="Liste drucken" onclick="print(etikettenliste)" />

					<form method="post" name="db_save" action="vars.php" target="php_messages">
				<div id="jsondiv" style="display:none">
					<input class="json_input" id="jsonvalues" name="jsonified" size="150" type="text" />
				</div>
					<input class="pushbuttonr" type="submit" name="save_to_db" onclick="return validate_form()" value="markierte Liquids in DB speichern" />
					</form>
				</div>
<iframe id="php_messages" name="php_messages" class="floater borderlein errorlog"></iframe>
			</div>











			<div class="footer">
			</div>
	</body> 
</html>
