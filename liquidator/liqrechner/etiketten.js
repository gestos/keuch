var dgby=function( id ) { return document.getElementById( id ); };

function send_to_database() {
	console.log("send this to db");
}

function shoot() {
	var a1 = dgby('ar1').value || '';
	var a2 = dgby('ar2').value || '';
	var a3 = dgby('ar3').value || '';
	var a4 = dgby('ar4').value || '';
	var a5 = dgby('ar5').value || '';
	var a1p = dgby('aroma1pct').value || '';
	var a2p = dgby('aroma2pct').value || '';
	var a3p = dgby('aroma3pct').value || '';
	var a4p = dgby('aroma4pct').value || '';
	var a5p = dgby('aroma5pct').value || '';
	var flv_liq = String(dgby('arpct_5').value);
	var nic_liq = String(dgby('nic_5').value);
	var pg_liq = Number.parseFloat(dgby('pg_5').value).toFixed(1);
	var vg_liq = Number.parseFloat(dgby('vg_5').value).toFixed(1);
	var todai = new Date();
	var timestamp_id=Date.now();
	//var todate = todai.getDate()+'.'+todai.getMonth()+'.'+todai.getFullYear();
	var todate = todai.toISOString().substr(0,10);
	var labeldiv = dgby('etikettenliste'); // div, in den die tabelle kommt

	function makemarker(row) {
		var milseconds=Date.now();
		var new_cell = row.insertCell();
		var new_chkbox = document.createElement("input");
		new_chkbox.type="checkbox";
		new_chkbox.name="markir_box";
		new_chkbox.className="markirbox";
		new_chkbox.id=milseconds;

		var label = document.createElement('label')
		label.htmlFor = milseconds;
		label.appendChild(document.createTextNode('markir fuer DB'));
		new_chkbox.onchange=create_json;

		new_cell.appendChild(new_chkbox);
		new_cell.appendChild(label);
		return new_cell;
	}

	function new_in(row, name, value) {
		var proz_regex = /.*proz$/
		var pvg_regex = /^pvg.*proz$/
		var new_cell = row.insertCell();

		if (pvg_regex.test(name) == true) {
			var pg_input=document.createElement("input");
			var vg_input=document.createElement("input");
			pg_input.size="2";
			pg_input.name="pg_liq";
			pg_input.value=pg_liq;
			pg_input.className="etiketten_input";
			pg_input.readOnly=true;
			vg_input.size="2";
			vg_input.name="vg_liq";
			vg_input.value=vg_liq;
			vg_input.className="etiketten_input";
			vg_input.readOnly=true;
			new_cell.appendChild(pg_input);
			new_cell.append(" / ");
			new_cell.appendChild(vg_input);
			new_cell.append(" %");
		}
		else {
			var new_input=document.createElement("input");
			new_input.placeholder="leer";
			new_input.size="6";
			new_input.name=name;
			new_input.value=value;
			new_input.className="etiketten_input";
			new_input.readOnly=true;
			new_cell.appendChild(new_input);
			if ( (proz_regex.test(name) == true) || (name == "nic") ) {
				new_input.size="2";
				new_cell.append("%");
			}
		}
		return new_cell;
	}

	newtab = document.createElement('table'); // Tabelle mit 5 Reihen fuer Aromen etc
	newtab.className = 'labeltable';
	newtab.id = timestamp_id;

	tr1 = newtab.insertRow(); 
	aro1_name=new_in(tr1,"aro1_name",a1);
	aro1_proz=new_in(tr1,"aro1_proz",a1p);
	tr1.insertCell().className="trenner";
	aroG_name = tr1.insertCell().innerHTML="aroma";
	aroG_proz = new_in(tr1,"aroG_proz",flv_liq);
	tr1.insertCell().className="trenner";
	removal = tr1.insertCell();
	rembutton = document.createElement("input");
	rembutton.className="pushbuttonr";
	rembutton.type="button";
	rembutton.id="remover";
	rembutton.value="Etikett loeschen";
	rembutton.onclick=function(){
		this.parentElement.parentElement.parentElement.parentElement.remove();
		return false;
	}
	removal.appendChild(rembutton);

	tr2 = newtab.insertRow();
	aro2_name=new_in(tr2,"aro2_name",a2);
	aro2_proz=new_in(tr2,"aro2_proz",a2p);
	tr2.insertCell().className="trenner";
	pvg_name = tr2.insertCell().innerHTML="pvg";
	pvg_proz = new_in(tr2,"pvg_proz",pg_liq);
	tr2.insertCell().className="trenner";

	tr3 = newtab.insertRow();
	aro3_name=new_in(tr3,"aro3_name",a3);
	aro3_proz=new_in(tr3,"aro3_proz",a3p);
	tr3.insertCell().className="trenner";
	nic_name = tr3.insertCell().innerHTML="nic";
	nic_mg = new_in(tr3,"nic",nic_liq);
	tr3.insertCell().className="trenner";

	tr4 = newtab.insertRow();
	aro4_name=new_in(tr4,"aro4_name",a4);
	aro4_proz=new_in(tr4,"aro4_proz",a4p);
	tr4.insertCell().className="trenner";
	date_name = tr4.insertCell().innerHTML="date";
	date_date = new_in(tr4,"datum",todate);
	tr4.insertCell().className="trenner";

	tr5 = newtab.insertRow();
	aro5_name=new_in(tr5,"aro5_name",a5);
	aro5_proz=new_in(tr5,"aro5_proz",a5p);
	tr5.insertCell().className="trenner";
	namecell = tr5.insertCell().innerHTML="name";
	name_in = tr5.insertCell();
	namefiel=document.createElement("input");
	namefiel.type="text";
	namefiel.name="liquidname";
	namefiel.id="liqname";
	namefiel.size="6";
	namefiel.placeholder="optional";
	namefiel.className="etiketten_input";
	name_in.appendChild(namefiel);
	tr5.insertCell().className="trenner";
	markirDB = makemarker(tr5);

	labeldiv.appendChild(newtab);
}

var liquidobjekte = [];
function create_json(clckparams) {
	checkbox_status=clckparams["target"]["checked"];
	if(checkbox_status === true) {
		curr_table=dgby(clckparams["target"].parentNode.parentNode.parentNode.parentNode.id);
		var inputfelder=curr_table.querySelectorAll("input.etiketten_input");
		var lobjekt={};
		lobjekt["id"]=curr_table.id;
		for (var feld of inputfelder.values()) {
			var eigenschaft=feld.name;
			lobjekt[eigenschaft]=feld.value;
		}
		liquidobjekte.push(lobjekt);
	}
	else {
		curr_table=dgby(clckparams["target"].parentNode.parentNode.parentNode.parentNode.id);
		var found_indexes = liquidobjekte.findIndex(x => x.id === curr_table.id);
		if (found_indexes === undefined || found_indexes.length == 0) {
			window.alert("item to be removed is not there");
		}
		else {
			liquidobjekte.splice(found_indexes,1);
		}
	}
	console.log(liquidobjekte);
	var jsonvalue=dgby('jsonvalues');
	jsonvalue.value=JSON.stringify(liquidobjekte);
}

function print(tabelle) {
	var printwin = window.open('');
	printwin.document.write('<html><head><title>Etikettendruck</title>');
	printwin.document.write('<link rel="stylesheet" href="druck.css">');
	printwin.document.write('</head><body>');
	printwin.document.write(tabelle.outerHTML);
	printwin.document.write('</body></html>');
	printwin.document.close();
	return true;
}
