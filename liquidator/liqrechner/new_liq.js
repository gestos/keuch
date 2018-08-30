var dgby=function( id ) { return document.getElementById( id ); };


// ALLGEMEINE FUNKTIONEN
// check several values for 100
function chk100(pg,vg,alk,nic) {
	var1 = Number(dgby(pg).value);
	var2 = Number(dgby(vg).value);
	var3 = Number(dgby(alk).value);
	summe=var1+var2+var3;
	if (summe !== 100) {
		col100(pg,vg,alk,'#ffd4ca')
	} else {
		col100(pg,vg,alk,'honeydew')
	}
	return summe;
}

// color fields according to checked sum
function col100(val1,val2,val3,col) {
	dgby(val1).style.background = col;
	dgby(val2).style.background = col;
	dgby(val3).style.background = col;
}

// GRUNDMISCHUNG
// check fuer grundstoffe
function chkgrund() {
	let ml = Number(dgby('mlz').value);
	grundsumme=chk100('pgz','vgz','alkz');
	if (grundsumme == 100 && ml >= 10) {
		dgby('go1').disabled=false;
	} else {
		dgby('go1').disabled=true;
	}
}
// richtung lesen
function flick(switcher) {
	swchk=dgby(switcher).checked;
	return swchk;
}
// richtung aendern
function switchgrund() {
	if (flick('switcher1') == true) {
		dgby('pg_rein').readOnly=false;
		dgby('vg_rein').readOnly=false;
		dgby('alkrein').readOnly=false;
		dgby('pgz').readOnly=true;
		dgby('vgz').readOnly=true;
		dgby('alkz').readOnly=true;
		dgby('mlz').readOnly=true;
		dgby('go1').disabled=false;
	} else {
		dgby('pg_rein').readOnly=true;
		dgby('vg_rein').readOnly=true;
		dgby('alkrein').readOnly=true;
		dgby('pgz').readOnly=false;
		dgby('vgz').readOnly=false;
		dgby('alkz').readOnly=false;
		dgby('mlz').readOnly=false;
		dgby('go1').disabled=true;
	}
}
// ausrechnen (grundstoffe)
function calc_grund() {
	if (flick('switcher1') == false) {
		let pgpct=dgby('pgz').value, vgpct=dgby('vgz').value, alkpct=dgby('alkz').value, ml=dgby('mlz').value;
		let pgml=(ml/100)*pgpct, vgml=(ml/100)*vgpct, alkml=(ml/100)*alkpct;
		dgby('pg_rein').value=pgml;
		dgby('vg_rein').value=vgml;
		dgby('alkrein').value=alkml;
	} else if (flick('switcher1') == true) {
		let pgml=Number(dgby('pg_rein').value);
		let vgml=Number(dgby('vg_rein').value);
		let alkml=Number(dgby('alkrein').value);
		let ml=Number((pgml+vgml+alkml)),pgpct=(pgml/ml)*100,vgpct=(vgml/ml)*100,alkpct=(alkml/ml)*100;
		dgby('mlz').value=ml;
		dgby('pgz').value=pgpct;
		dgby('vgz').value=vgpct;
		dgby('alkz').value=alkpct;
	}
}
// WERTE VON GRUNDMISCHUNG ZU NIKMISCHUNG UEBERNEHMEN
function slidestate() {
	return dgby('to_nic').value
}
// slider-labels
function slideopt1() {
	state=dgby('to_nic').value;
	if (slidestate() == 0) {
		dgby('slide1').innerHTML='Nullerbasis-Werte aus Feld \"Grundstoffe\" übernehmen';
	} else if (slidestate() == 1) {
		dgby('slide1').innerHTML='keine Werte übernehmen';
	} else if (slidestate() == 2) {
		dgby('slide1').innerHTML='Nullerbasis-Werte aus Feld \"Nikotinmischung\" übernehmen';
	}
}
// werte in andere Tabelle schreiben
function ubernehm() {
	if (slidestate() == 0) {
		console.log(dgby);
		dgby('pgb1').value = dgby('pgz').value;
		dgby('vgb1').value = dgby('vgz').value;
		dgby('alk1').value = dgby('alkz').value;
		console.log('in ifschleife');
		chk100('pgb1','vgb1','alk1');
	}
	else if (slidestate() == 2) {
		dgby('pgz').value = dgby('pgb1').value;
		dgby('vgz').value = dgby('vgb1').value;
		dgby('alkz').value = dgby('alk1').value;
		chk100('pgz','vgz','alkz');
	};
}
// NIKOTINMISCHUNG
// check fuer Nikotinmische
function chkvalid() {
	summ1=chk100('pgb1','vgb1','alk1');
	summ2=chk100('pgb2','vgb2','alk2');
	if (summ1 == 100 &&  summ2 == 100 && chknic('nic2','nicz','mlliq')) {
		dgby('go').disabled=false;
	}
}

function chknic(nicbb,nicliq,mlliq) {
	let nic_bb = Number(dgby(nicbb).value);
	let nic_liq = Number(dgby(nicliq).value);
	let ml = Number(dgby(mlliq).value);
	console.log(nic_bb,nic_liq,ml);

	if ((nic_bb < 1 || nic_bb > 250) || (nic_liq < 0.5 || nic_liq > 32) || (ml < 10)) {
		col100(nicbb,nicliq,mlliq,'#ffd4ca');
		return false;
	} else {
		col100(nicbb,nicliq,mlliq,'honeydew');
		return true;
	}
}
// mischung ausrechnen
function calculate_nic(liq_menge,liq_nic,bb_nic) {
	let liqmenge				=	Number(dgby(liq_menge).value);
	let bb_nic_gehalt		=	Number(dgby(bb_nic).value);
	let liq_nic_gehalt	=	Number(dgby(liq_nic).value);

	let ml_menge_bb = liqmenge/(bb_nic_gehalt/liq_nic_gehalt);
	//console.log(ml_menge_bb);
	let ml_menge_nb = liqmenge-ml_menge_bb;
	//console.log(ml_menge_nb);
	return [ml_menge_nb,ml_menge_bb];
}

function get_pct(nullerbase,bunkerbase,ml_nb,ml_bb) {
	let liqmenge				=	Number(dgby('mlliq').value);
	let pct_nb = Number(dgby(nullerbase).value);
	let pct_bb = Number(dgby(bunkerbase).value);
	let pct_liq = (ml_nb*pct_nb)/liqmenge+(ml_bb*pct_bb)/liqmenge;
	return pct_liq;
}



function calculate_liq () {
	let mls=calculate_nic('mlliq','nicz','nic2'), ml_nb=mls[0], ml_bb=mls[1];
	//console.log(mls, ml_bb, ml_nb);
	let percent_pg_liq = get_pct('pgb1','pgb2',ml_nb,ml_bb);
	let percent_vg_liq = get_pct('vgb1','vgb2',ml_nb,ml_bb);
	let percent_alk_liq = get_pct('alk1','alk2',ml_nb,ml_bb);
	console.log('prozent pg: ',percent_pg_liq,' prozent vg: ',percent_vg_liq,' prozent alk: ',percent_alk_liq);
	dgby('ml1').value=ml_nb;
	dgby('ml2').value=ml_bb;
	dgby('pgbz').value=percent_pg_liq;
	dgby('vgbz').value=percent_vg_liq;
	dgby('alkz1').value=percent_alk_liq;
}

// richtung aendern2
function switch2() {
	if (flick('switcher2') == true) {
		dgby('pgbz').readOnly=false;
		dgby('vgbz').readOnly=false;
		dgby('alkz1').readOnly=false;
		dgby('pgb1').readOnly=true;
		dgby('vgb1').readOnly=true;
		dgby('alk1').readOnly=true;
	} else  if (flick('switcher2') == false) {
		dgby('pgbz').readOnly=true;
		dgby('vgbz').readOnly=true;
		dgby('alkz1').readOnly=true;
		dgby('pgb1').readOnly=false;
		dgby('vgb1').readOnly=false;
		dgby('alk1').readOnly=false;
	}
}





