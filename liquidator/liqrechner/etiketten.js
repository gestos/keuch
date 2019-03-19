if(!marken){
	console.log("no db");
}
else{
	var marken_mapped = marken.reduce(function(obj,item){
		obj[item.firma] = item.tag; 
		return obj;
	}, {});
}
herstellerfelder=Object.keys(mapping_objekt);
function send_to_database() {
	console.log("send this to db");
}

function shoot() {

	function get_composite_names() {
		let componames=[], componame='', liq_her=[], liq_ges=[]; 
		for(feld of herstellerfelder){
			let her = dgby(feld).value;
			liq_her.push(her);
			if(dgby('db_freehand_switch').value === 'set freehand mode'){   // in database mode
				let ges = dgby(mapping_objekt[feld]).value || '';
				liq_ges.push(ges);
				if(her !== '' && ges !== ''){
					componame=marken_mapped[her]+" "+ges;
				}
				else {
					componame='';
				}
			}
			else {																													// in freehand mode
				componame = her;
			}
			componames.push(componame);
		}
		return [componames,liq_her,liq_ges];
	}
	let aromen_entries=get_composite_names()[0];
	let her=get_composite_names()[1];
	let ges=get_composite_names()[2];

	let a1 = aromen_entries[0] || '', h1 = her[0], g1 = ges[0];
	let a2 = aromen_entries[1] || '', h2 = her[1], g2 = ges[1];
	let a3 = aromen_entries[2] || '', h3 = her[2], g3 = ges[2];
	let a4 = aromen_entries[3] || '', h4 = her[3], g4 = ges[3];
	let a5 = aromen_entries[4] || '', h5 = her[4], g5 = ges[4];
	let a1p = dgby('aroma1pct').value || '';
	let a2p = dgby('aroma2pct').value || '';
	let a3p = dgby('aroma3pct').value || '';
	let a4p = dgby('aroma4pct').value || '';
	let a5p = dgby('aroma5pct').value || '';
	let a1m = dgby('aroma1ml').value || '';
	let a2m = dgby('aroma2ml').value || '';
	let a3m = dgby('aroma3ml').value || '';
	let a4m = dgby('aroma4ml').value || '';
	let a5m = dgby('aroma5ml').value || '';
	let flv_liq = String(dgby('arpct_5').value);
	let nic_liq = String(dgby('nic_5').value);
	let pg_liq = Number.parseFloat(dgby('pg_5').value).toFixed(1);
	let vg_liq = Number.parseFloat(dgby('vg_5').value).toFixed(1);
	let todai = new Date();
	let timestamp_id=Date.now();
	//let todate = todai.getDate()+'.'+todai.getMonth()+'.'+todai.getFullYear();
	let todate = todai.toISOString().substr(0,10);
	let labeldiv = dgby('etikettenliste'); // div, in den die tabelle kommt

	function makemarker(row) {
		// checkbox for save to db
		let milseconds=Date.now();
		let new_cell = row.insertCell();
		let new_chkbox = document.createElement("input");
		let label_db = document.createElement('label')
		new_chkbox.type="checkbox";
		new_chkbox.name="markir_box";
		new_chkbox.className="markirbox";
		new_cell.className="markirbox";
		new_chkbox.id=milseconds;
		label_db.htmlFor = milseconds;
		label_db.appendChild(document.createTextNode('markir fuer DB'));
		new_chkbox.onchange=create_json_db;
		new_cell.appendChild(new_chkbox);
		new_cell.appendChild(label_db);

		// checkbox for update ml
		let mlUpdateCell = row.insertCell();
		let mlUpdateBox = document.createElement("input");
		let label_ml = document.createElement('label')
		mlUpdateBox.type="checkbox";
		mlUpdateBox.name="mlupdate_box";
		mlUpdateBox.className="markirbox etiketten_input";
		mlUpdateBox.onchange=create_json_ml;
		mlUpdateCell.className="markirbox";
		label_ml.htmlFor = "update_ml";
		label_ml.appendChild(document.createTextNode('update ml in DB'));
		mlUpdateCell.appendChild(mlUpdateBox);
		mlUpdateCell.appendChild(label_ml);



		if (dgby('db_freehand_switch').value === 'set database mode'){
			new_cell.hidden = true;
			mlUpdateCell.hidden = true;
		}
		return new_cell;
	}

	function new_in(row, name, value) {
		let proz_regex = /.*proz$/
		let ml_regex = /.*(ml|her|ges)$/
		let pvg_regex = /^pvg.*proz$/
		let new_cell = row.insertCell();

		if (pvg_regex.test(name) == true) {
			let pg_input=document.createElement("input");
			let vg_input=document.createElement("input");
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
			new_input.size="14";
			new_input.name=name;
			new_input.value=value;
			new_input.className="etiketten_input";
			new_input.readOnly=true;
			new_cell.appendChild(new_input);
			if ( (proz_regex.test(name) == true) || (name == "nic") ) {
				new_input.size="2";
				if ( name == "nic")  {
					new_cell.append("mg");
				}
				else {
					new_cell.append("%");
				}
			}
			else if ( (ml_regex.test(name) == true) ) {
				new_input.hidden=true;
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
	aro1_ml=new_in(tr1,"aro1_ml",a1m);
	aro1_her=new_in(tr1,"aro1_her",h1);
	aro1_ges=new_in(tr1,"aro1_ges",g1);
	tr1.insertCell().className="trenner";
	aroG_name = tr1.insertCell().innerHTML="aroma";
	aroG_proz = new_in(tr1,"aroG_proz",flv_liq);
	tr1.insertCell().className="trenner2";
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
	aro2_ml=new_in(tr2,"aro2_ml",a2m);
	aro2_her=new_in(tr2,"aro2_her",h2);
	aro2_ges=new_in(tr2,"aro2_ges",g2);
	tr2.insertCell().className="trenner";
	pvg_name = tr2.insertCell().innerHTML="pvg";
	pvg_proz = new_in(tr2,"pvg_proz",pg_liq);
	tr2.insertCell().className="trenner2";

	tr3 = newtab.insertRow();
	aro3_name=new_in(tr3,"aro3_name",a3);
	aro3_proz=new_in(tr3,"aro3_proz",a3p);
	aro3_ml=new_in(tr3,"aro3_ml",a3m);
	aro3_her=new_in(tr3,"aro3_her",h3);
	aro3_ges=new_in(tr3,"aro3_ges",g3);
	tr3.insertCell().className="trenner";
	nic_name = tr3.insertCell().innerHTML="nic";
	nic_mg = new_in(tr3,"nic",nic_liq);
	tr3.insertCell().className="trenner2";

	tr4 = newtab.insertRow();
	aro4_name=new_in(tr4,"aro4_name",a4);
	aro4_proz=new_in(tr4,"aro4_proz",a4p);
	aro4_ml=new_in(tr4,"aro4_ml",a4m);
	aro4_her=new_in(tr4,"aro4_her",h4);
	aro4_ges=new_in(tr4,"aro4_ges",g4);
	tr4.insertCell().className="trenner";
	date_name = tr4.insertCell().innerHTML="date";
	date_date = new_in(tr4,"datum",todate);
	tr4.insertCell().className="trenner2";

	tr5 = newtab.insertRow();
	aro5_name=new_in(tr5,"aro5_name",a5);
	aro5_proz=new_in(tr5,"aro5_proz",a5p);
	aro5_ml=new_in(tr5,"aro5_ml",a5m);
	aro5_her=new_in(tr5,"aro5_her",h5);
	aro5_ges=new_in(tr5,"aro5_ges",g5);
	tr5.insertCell().className="trenner";
	namecell = tr5.insertCell().innerHTML="name";
	name_in = tr5.insertCell();
	namefiel=document.createElement("input");
	namefiel.type="text";
	namefiel.name="liquidname";
	namefiel.id="liqname";
	namefiel.size="11";
	namefiel.placeholder="optional";
	namefiel.className="etiketten_input";
	name_in.appendChild(namefiel);
	tr5.insertCell().className="trenner2";
	markirDB = makemarker(tr5);

	labeldiv.appendChild(newtab);
}

var liquidobjekte = [];
dgby('jsonvalues').value='';
function create_json_db(clckparams) {
	checkbox_status=clckparams["target"]["checked"];
	if(checkbox_status === true) {
		let curr_table=dgby(clckparams["target"].parentNode.parentNode.parentNode.parentNode.id);
		let inputfelder=curr_table.querySelectorAll("input.etiketten_input");
		let lobjekt={};
		lobjekt["id"]=curr_table.id;
		for (let feld of inputfelder.values()) {
			let eigenschaft=feld.name;
			lobjekt[eigenschaft]=feld.value;
			console.log(eigenschaft+": "+lobjekt[eigenschaft]);
		}
		liquidobjekte.push(lobjekt);
	}
	else {
		curr_table=dgby(clckparams["target"].parentNode.parentNode.parentNode.parentNode.id);
		let found_indexes = liquidobjekte.findIndex(x => x.id === curr_table.id);
		if (found_indexes === undefined || found_indexes.length == 0) {
			window.alert("item to be removed is not there");
		}
		else {
			liquidobjekte.splice(found_indexes,1);
		}
	}
	//console.log(liquidobjekte);
	let jsonvalue=dgby('jsonvalues');
	jsonvalue.value=JSON.stringify(liquidobjekte);
}
var mlobjekte = [];
dgby('jsonvalues_ml').value='';
function create_json_ml(clckparams) {
	checkbox_status=clckparams["target"]["checked"];
	if(checkbox_status === true) {
		let curr_table=dgby(clckparams["target"].parentNode.parentNode.parentNode.parentNode.id);
		let inputfelder=curr_table.querySelectorAll("input.etiketten_input");
		let ml_objekt={};
		ml_objekt["id"]=curr_table.id;
		for (let feld of inputfelder.values()) {
			let eigenschaft=feld.name;
			ml_objekt[eigenschaft]=feld.value;
			console.log(eigenschaft+": "+ml_objekt[eigenschaft]);
		}
		mlobjekte.push(ml_objekt);
	}
	else {
		let curr_table=dgby(clckparams["target"].parentNode.parentNode.parentNode.parentNode.id);
		let found_indexes = liquidobjekte.findIndex(x => x.id === curr_table.id);
		if (found_indexes === undefined || found_indexes.length == 0) {
			window.alert("item to be removed is not there");
		}
		else {
			mlobjekte.splice(found_indexes,1);
		}
	}
	//console.log(liquidobjekte);
	let jsonvalue_ml=dgby('jsonvalues_ml');
	jsonvalue_ml.value=JSON.stringify(mlobjekte);
}

function validate_form() {
	let objs=liquidobjekte;
	let ml_objs=mlobjekte;
	if ( (!objs || !objs.length) && (!ml_objs || !ml_objs.length) ) {
		alert('nothing to do');
		return false;
	}
	else if (objs || objs.length) {
		aromen_namen=[];
		aromen_prozente=[];
		for(elem of ['aro1_name', 'aro2_name', 'aro3_name', 'aro4_name', 'aro5_name']) {
			wert=objs[0][elem];
			if (wert) { aromen_namen.push(objs[0][elem]); }
		}
		for(elem of ['aro1_proz', 'aro2_proz', 'aro3_proz', 'aro4_proz', 'aro5_proz']) {
			wert=objs[0][elem];
			if (wert) { aromen_prozente.push(objs[0][elem]); }
		}
		if ( (!aromen_namen || !aromen_namen.length) || (!aromen_prozente || !aromen_prozente.length) ) {
			alert('please provide at least one flavour');
			return false;
		}
		else {
			return true;
		}
		return true;
	}
}

function print(div_mit_liquids) {
	var oldhtml=dgby(div_mit_liquids).cloneNode(true);
	var printwin = window.open('');
	printwin.document.write('<html><head><title>Etikettendruck</title>');
	printwin.document.write('<link rel="stylesheet" href="druck.css">');
	printwin.document.write('</head><body>');
	printwin.document.body.appendChild(oldhtml);
	printwin.document.write('</body></html>');
	printwin.document.close();
	return true;
}
