var dgby=function( id ) { return document.getElementById( id ); };


// ALLGEMEINE FUNKTIONEN
// check several values for 100
function chk100(pg,vg,alk,nic) {
	var1 = Number(dgby(pg).value);
	var2 = Number(dgby(vg).value);
	var3 = Number(dgby(alk).value);
	summe=var1+var2+var3;
	if (summe !== 100) {
		col100(pg,vg,alk,'#c65353')
		return false;
	} else {
		col100(pg,vg,alk,'#254519')
		return true;
	}
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
	if (grundsumme == true && ml >= 10) {
		dgby('mlz').style.background='#254519';
		dgby('go1').disabled=false;
	} else {
		dgby('mlz').style.background='#c65353';
		dgby('go1').disabled=true;
	}
}
// richtung lesen
function flick(switcher) {
	let swchk=dgby(switcher).checked;
	return swchk;
}
// richtung aendern
function switchgrund() {
	if (flick('switcher1') == true) {
		dgby('pg_rein').removeAttribute("style");
		dgby('vg_rein').removeAttribute("style");
		dgby('alkrein').removeAttribute("style");
		dgby('pgz').removeAttribute("style");
		dgby('vgz').removeAttribute("style");
		dgby('alkz').removeAttribute("style");
		dgby('mlz').removeAttribute("style");
		dgby('pgz').value=null;
		dgby('vgz').value=null;
		dgby('alkz').value=null;
		dgby('mlz').value=null;
		dgby('pg_rein').value=null;
		dgby('vg_rein').value=null;
		dgby('alkrein').value=null;

		dgby('pg_rein').readOnly=false;
		dgby('vg_rein').readOnly=false;
		dgby('alkrein').readOnly=false;
		dgby('pgz').readOnly=true;
		dgby('vgz').readOnly=true;
		dgby('alkz').readOnly=true;
		dgby('mlz').readOnly=true;
		dgby('go1').disabled=false;
	} else {
		dgby('pg_rein').removeAttribute("style");
		dgby('vg_rein').removeAttribute("style");
		dgby('alkrein').removeAttribute("style");
		dgby('pgz').removeAttribute("style");
		dgby('vgz').removeAttribute("style");
		dgby('alkz').removeAttribute("style");
		dgby('mlz').removeAttribute("style");
		dgby('pgz').value=null;
		dgby('vgz').value=null;
		dgby('alkz').value=null;
		dgby('mlz').value=null;
		dgby('pg_rein').value=null;
		dgby('vg_rein').value=null;
		dgby('alkrein').value=null;

		dgby('pgz').readOnly=false;
		dgby('vgz').readOnly=false;
		dgby('alkz').readOnly=false;
		dgby('mlz').readOnly=false;
		dgby('pg_rein').readOnly=true;
		dgby('vg_rein').readOnly=true;
		dgby('alkrein').readOnly=true;
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
		dgby('slide1').innerHTML='von<span class="von"> \"Grundstoffe\" </span> nach <span class="nach">\"Nikotinmischung\"</span> übernehmen<br>-------->';
		dgby('pgz').style.borderColor='#00aa4a';
		dgby('vgz').style.borderColor='#00aa4a';
		dgby('alkz').style.borderColor='#00aa4a';
		dgby('pgb1').style.borderColor='#d5ad00';
		dgby('vgb1').style.borderColor='#d5ad00';
		dgby('alk1').style.borderColor='#d5ad00';
		dgby('ubertrag').disabled=false;
	} else if (slidestate() == 1) {
		dgby('slide1').innerHTML='keine Werte übernehmen';
		dgby('pgz').style.borderColor='';
		dgby('vgz').style.borderColor='';
		dgby('alkz').style.borderColor='';
		dgby('pgb1').style.borderColor='';
		dgby('vgb1').style.borderColor='';
		dgby('alk1').style.borderColor='';
		dgby('ubertrag').disabled=true;
	} else if (slidestate() == 2) {
		dgby('slide1').innerHTML='von<span class="von"> \"Nikotinmischung\"</span> nach <span class="nach">\"Grundstoffe\"</span> übernehmen<br><--------';
		dgby('pgb1').style.borderColor='#00aa4a';
		dgby('vgb1').style.borderColor='#00aa4a';
		dgby('alk1').style.borderColor='#00aa4a';
		dgby('pgz').style.borderColor='#d5ad00';
		dgby('vgz').style.borderColor='#d5ad00';
		dgby('alkz').style.borderColor='#d5ad00';
		dgby('ubertrag').disabled=false;
	}
}
// werte in andere Tabelle schreiben
function ubernehm() {
	if (slidestate() == 0) {
		switch2();
		dgby('pgb1').value = dgby('pgz').value;
		dgby('vgb1').value = dgby('vgz').value;
		dgby('alk1').value = dgby('alkz').value;
		chk100('pgb1','vgb1','alk1');
	}
	else if (slidestate() == 2) {
		switchgrund();
		dgby('pgz').value = dgby('pgb1').value;
		dgby('vgz').value = dgby('vgb1').value;
		dgby('alkz').value = dgby('alk1').value;
		chk100('pgz','vgz','alkz');
	};
}
// NIKOTINMISCHUNG
// check fuer Nikotinmische
function chkvalid() {
	if (flick('switcher2') == false) {
		summ1=chk100('pgb1','vgb1','alk1');
		summ2=chk100('pgb2','vgb2','alk2');
	} else if (flick('switcher2') == true) {
		summ1=chk100('pgb2','vgb2','alk2');
		summ2=chk100('pgbz','vgbz','alkz1');
	}
	if (summ1 &&  summ2 && chknic('nic2','nicz','mlliq') == true) {
		dgby('go').disabled=false;
	} else {
		dgby('go').disabled=true;
	}
}

function chknic(nicbb,nicliq,mlliq) {
	let nic_bb = Number(dgby(nicbb).value);
	let nic_liq = Number(dgby(nicliq).value);
	let ml = Number(dgby(mlliq).value);

	if ((nic_bb < 1 || nic_bb > 250)) {
		dgby('nic2').style.backgroundColor='#c65353';
	} else {
		dgby('nic2').style.backgroundColor='#254519';
	};
	if ((nic_liq < 0.5 || nic_liq > 32)) {
		dgby('nicz').style.backgroundColor='#c65353';
	} else {
		dgby('nicz').style.backgroundColor='#254519';
	};
	if (ml < 10) {
		dgby('mlliq').style.backgroundColor='#c65353';
	} else {
		dgby('mlliq').style.backgroundColor='#254519';
	};
	if ((nic_bb < 1 || nic_bb > 250) || (nic_liq < 0.5 || nic_liq > 32) || (ml < 10)) {
		return false;
	} else {
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
	if (flick('switcher2') == false) {
		let mls=calculate_nic('mlliq','nicz','nic2'), ml_nb=mls[0], ml_bb=mls[1];
		//console.log(mls, ml_bb, ml_nb);
		let percent_pg_liq = get_pct('pgb1','pgb2',ml_nb,ml_bb).toFixed(2);
		let percent_vg_liq = get_pct('vgb1','vgb2',ml_nb,ml_bb).toFixed(2);
		let percent_alk_liq = get_pct('alk1','alk2',ml_nb,ml_bb).toFixed(2);
		console.log('prozent pg: ',percent_pg_liq,' prozent vg: ',percent_vg_liq,' prozent alk: ',percent_alk_liq);
		dgby('ml1').value=ml_nb;
		dgby('ml2').value=ml_bb;
		dgby('pgbz').value=percent_pg_liq;
		dgby('vgbz').value=percent_vg_liq;
		dgby('alkz1').value=percent_alk_liq;
	} else if (flick('switcher2') == true) {
		calc2pct('pgb2','vgb2','alk2','nic2','nicz','mlliq','pgbz','vgbz','alkz1');
	}
}
function calc2pct(pct_pg_bb,pct_vg_bb,pct_alk_bb,mg_bb,mg_lq,menge_lq,pct_pg_lq,pct_vg_lq,pct_alk_lq) {
	console.log('calc2pct');
	for (i=0; i<arguments.length;i++) {
		// console.log(arguments[i]);
		arguments[i]=dgby(arguments[i]).value;
		// console.log(arguments[i]);
	}
	// diese Werte sind fix, weil durch die Zusammensetzung der BB vorgegeben
	let ml_bb=((mg_lq*menge_lq)/mg_bb).toFixed(2);
	let ml_nb=(menge_lq-ml_bb).toFixed(2);;
	let ml_pg_bb=(ml_bb*(pct_pg_bb/100)).toFixed(2);
	let ml_vg_bb=(ml_bb*(pct_vg_bb/100)).toFixed(2);
	let ml_alk_bb=(ml_bb*(pct_alk_bb/100)).toFixed(2);

	console.log('BB ml_PG:',ml_pg_bb,' ml_VG:',ml_vg_bb,' ml_Alk:',ml_alk_bb);

	// diese Werte in ml soll das Ziel-Liquid haben:
	let ml_pg_liq=(menge_lq*(pct_pg_lq/100)).toFixed(2);
	let ml_vg_liq=(menge_lq*(pct_vg_lq/100)).toFixed(2);
	let ml_alk_liq=(menge_lq*(pct_alk_lq/100)).toFixed(2);

	console.log('Liq ml_PG:',ml_pg_liq,' ml_VG:',ml_vg_liq,' ml_Alk:',ml_alk_liq);

	// diese Werte in ml werden von der NB benoetigt, um auf die Zielwerte zu kommen
	let ml_pg_nb=(ml_pg_liq-ml_pg_bb).toFixed(2);
	let ml_vg_nb=(ml_vg_liq-ml_vg_bb).toFixed(2);
	let ml_alk_nb=(ml_alk_liq-ml_alk_bb).toFixed(2);

	console.log('NB ml_PG:',ml_pg_nb,' ml_VG:',ml_vg_nb,' ml_Alk:',ml_alk_nb);

	// diese in Prozent von der berechneten NB-Menge
	let pct_pg_nb=((ml_pg_nb/ml_nb)*100).toFixed(2);
	let pct_vg_nb=((ml_vg_nb/ml_nb)*100).toFixed(2);
	let pct_alk_nb=((ml_alk_nb/ml_nb)*100).toFixed(2);


	// check, ob die Werte ueberhaupt legal sind
	if ((ml_pg_liq-ml_pg_bb < 0) || (ml_vg_liq-ml_vg_bb <0) || (ml_alk_liq-ml_alk_bb <0)) {
		window.alert('nicht moeglich');
	}



	dgby('ml2').value=ml_bb;
	dgby('ml1').value=ml_nb;
	dgby('pgb1').value=pct_pg_nb;
	dgby('vgb1').value=pct_vg_nb;
	dgby('alk1').value=pct_alk_nb;
}

// richtung aendern2
function switch2() {
	if (flick('switcher2') == true) {
		dgby('pgb1').value=null;
		dgby('vgb1').value=null;
		dgby('alk1').value=null;
		dgby('pgbz').value=null;
		dgby('vgbz').value=null;
		dgby('alkz1').value=null;
		dgby('pgb1').removeAttribute("style");
		dgby('vgb1').removeAttribute("style");
		dgby('alk1').removeAttribute("style");
		dgby('pgbz').removeAttribute("style");
		dgby('vgbz').removeAttribute("style");
		dgby('alkz1').removeAttribute("style");

		dgby('pgbz').readOnly=false;
		dgby('vgbz').readOnly=false;
		dgby('alkz1').readOnly=false;
		dgby('pgb1').readOnly=true;
		dgby('vgb1').readOnly=true;
		dgby('alk1').readOnly=true;

		dgby('misch_nuller').className="hiliterow";
		dgby('misch_ziel').className="";
	} else  if (flick('switcher2') == false) {
		dgby('pgb1').value=null;
		dgby('vgb1').value=null;
		dgby('alk1').value=null;
		dgby('pgbz').value=null;
		dgby('vgbz').value=null;
		dgby('alkz1').value=null;
		dgby('pgb1').removeAttribute("style");
		dgby('vgb1').removeAttribute("style");
		dgby('alk1').removeAttribute("style");
		dgby('pgbz').removeAttribute("style");
		dgby('vgbz').removeAttribute("style");
		dgby('alkz1').removeAttribute("style");

		dgby('pgbz').readOnly=true;
		dgby('vgbz').readOnly=true;
		dgby('alkz1').readOnly=true;
		dgby('pgb1').readOnly=false;
		dgby('vgb1').readOnly=false;
		dgby('alk1').readOnly=false;

		dgby('misch_ziel').className="hiliterow";
		dgby('misch_nuller').className="";
	}
	//let chk=chkvalid();
}

function switch3() {
	var swi='switcher3';
	if (flick(swi) == true) {
		dgby('pg_3').removeAttribute("style");
		dgby('vg_3').removeAttribute("style");
		dgby('alk3').removeAttribute("style");
		dgby('nic3').removeAttribute("style");
		dgby('pg_5').removeAttribute("style");
		dgby('vg_5').removeAttribute("style");
		dgby('alk_5').removeAttribute("style");
		dgby('nic_5').removeAttribute("style");
		dgby('pg_3').value=null;
		dgby('vg_3').value=null;
		dgby('alk3').value=null;
		dgby('nic3').value=null;
		dgby('pg_5').value=null;
		dgby('vg_5').value=null;
		dgby('alk_5').value=null;
		dgby('nic_5').value=null;
		dgby('ml3').value=null;
		dgby('ml4').value=null;

		dgby('pg_5').readOnly=false;
		dgby('vg_5').readOnly=false;
		dgby('alk_5').readOnly=false;
		dgby('nic_5').readOnly=false;
		dgby('pg_3').readOnly=true;
		dgby('vg_3').readOnly=true;
		dgby('alk3').readOnly=true;
		dgby('nic3').readOnly=true;


		dgby('Liq3').className="hiliterow"
		dgby('Ergebnis3').className=""
	} else  if (flick(swi) == false) {
		dgby('pg_3').removeAttribute("style");
		dgby('vg_3').removeAttribute("style");
		dgby('alk3').removeAttribute("style");
		dgby('nic3').removeAttribute("style");
		dgby('pg_5').removeAttribute("style");
		dgby('vg_5').removeAttribute("style");
		dgby('alk_5').removeAttribute("style");
		dgby('nic_5').removeAttribute("style");
		dgby('pg_3').value=null;
		dgby('vg_3').value=null;
		dgby('alk3').value=null;
		dgby('nic3').value=null;
		dgby('pg_5').value=null;
		dgby('vg_5').value=null;
		dgby('alk_5').value=null;
		dgby('nic_5').value=null;
		dgby('ml3').value=null;
		dgby('ml4').value=null;

		dgby('pg_5').readOnly=true;
		dgby('vg_5').readOnly=true;
		dgby('alk_5').readOnly=true;
		dgby('nic_5').readOnly=true;
		dgby('pg_3').readOnly=false;
		dgby('vg_3').readOnly=false;
		dgby('alk3').readOnly=false;
		dgby('nic3').readOnly=false;
		dgby('Liq3').className=""
		dgby('Ergebnis3').className="hiliterow"
	}
	//let chk=chkvalid2();
}

function chkvalid2() {
	// erstmal bestimmen, in welche richtung gerechnet wird
	if (flick('switcher3') == false) {
		var richtung='norm';
	} else {
		var richtung='rev';
	}

	// paar Variablen
	var nicsrc=dgby('nic3').value;
	var nicdst=dgby('nic_5').value;
	var arpct=dgby('arpct_5').value;


	if (richtung == 'norm') {
		console.log(richtung);
		let row1=chk100('pg_3','vg_3','alk3');
		let row2=chk100('pg_4','vg_4','alk4');
		if (0 < nicsrc && nicsrc < 49) {
			dgby('nic3').style.background='#254519';
			var nicok=true;
		} else {
			dgby('nic3').style.background='#c65353';
			var nicok=false;
		}
		if (0 < arpct && arpct < 51) {
			dgby('arpct_5').style.background='#254519';
			var arok=true;
		} else {
			dgby('arpct_5').style.background='#c65353';
			var arok=false;
		}
		if (dgby('ml_5').value > 9) {
			dgby('ml_5').style.background='#254519';
			var mengok=true;
		} else {
			dgby('ml_5').style.background='#c65353';
			var mengok=false;
		}
		if (row1 && row2 && nicok && arok && mengok) {
			dgby('go2').disabled=false;
		} else {
			dgby('go2').disabled=true;
		}
	} else {
		console.log(richtung);
		let row2=chk100('pg_4','vg_4','alk4');
		let row1=chk100('pg_5','vg_5','alk_5');
		if (0 < nicdst && nicdst < 49) {
			dgby('nic_5').style.background='#254519';
			var nicok=true;
		} else {
			dgby('nic_5').style.background='#c65353';
			var nicok=false;
		}
		if (0 < arpct && arpct < 51) {
			dgby('arpct_5').style.background='#254519';
			var arok=true;
		} else {
			dgby('arpct_5').style.background='#c65353';
			var arok=false;
		}
		if (dgby('ml_5').value > 9) {
			dgby('ml_5').style.background='#254519';
			var mengok=true;
		} else {
			dgby('ml_5').style.background='#c65353';
			var mengok=false;
		}
		if (row1 && row2 && nicok && arok && mengok) {
			dgby('go2').disabled=false;
		} else {
			dgby('go2').disabled=true;
		}
	}
}

function calculate_liq2() {
	if (flick('switcher3') == false) {

		// Zielmenge, Ziel-Aromenprozent, Ausgangsnikotin
		let dlq_ml=Number(dgby('ml_5').value).toFixed(2);
		let dpct_aro=Number(dgby('arpct_5').value).toFixed(2);
		let nic_src=Number(dgby('nic3').value).toFixed(2);

		// Prozente des Basisliquids
		let olq_pg_pct=Number(dgby('pg_3').value).toFixed(2);
		let olq_vg_pct=Number(dgby('vg_3').value).toFixed(2);
		let olq_alk_pct=Number(dgby('alk3').value).toFixed(2);

		// Prozente des Aromas
		let oar_pg_pct=Number(dgby('pg_4').value).toFixed(2);
		let oar_vg_pct=Number(dgby('vg_4').value).toFixed(2);
		let oar_alk_pct=Number(dgby('alk4').value).toFixed(2);

		// ml Aroma, ml Basisliquid
		let dml_aro=((dlq_ml/100)*dpct_aro).toFixed(2);
		let dml_olq=(dlq_ml-dml_aro).toFixed(2);
		dgby('ml3').value=dml_olq;
		dgby('ml4').value=dml_aro;

		// PG/VG/ALK gesamt-ml
		let aro_pg_ml=dml_aro*(oar_pg_pct/100);
		let aro_vg_ml=dml_aro*(oar_vg_pct/100);
		let aro_alk_ml=dml_aro*(oar_alk_pct/100);
		let olq_pg_ml=dml_olq*(olq_pg_pct/100);
		let olq_vg_ml=dml_olq*(olq_vg_pct/100);
		let olq_alk_ml=dml_olq*(olq_alk_pct/100);
		let dlq_pg_ml=(aro_pg_ml+olq_pg_ml).toFixed(2);
		let dlq_vg_ml=(aro_vg_ml+olq_vg_ml).toFixed(2);
		let dlq_alk_ml=(aro_alk_ml+olq_alk_ml).toFixed(2);

		// PG/VG/ALK gesamt-% im Zielliquid
		let dlq_pct_pg=(((aro_pg_ml+olq_pg_ml)/dlq_ml)*100).toFixed(2);
		let dlq_pct_vg=(((aro_vg_ml+olq_vg_ml)/dlq_ml)*100).toFixed(2);
		let dlq_pct_alk=(((aro_alk_ml+olq_alk_ml)/dlq_ml)*100).toFixed(2);

		dgby('pg_5').value=dlq_pct_pg;
		dgby('vg_5').value=dlq_pct_vg;
		dgby('alk_5').value=dlq_pct_alk;

		// mg/ml im Zielliquid
		let nic_dst=((dml_olq*nic_src)/dlq_ml).toFixed(2);
		dgby('nic_5').value=nic_dst;
	} else if (flick('switcher3') == true) {

		// HIER IN DIE ANDERE RICHTUNG RECHNEN!

		// gewünschte Menge und Prozentanteile
		end_menge_ml=Number(dgby('ml_5').value).toFixed(2);
		end_pg_przt=Number(dgby('pg_5').value).toFixed(2);
		end_vg_przt=Number(dgby('vg_5').value).toFixed(2);
		end_alk_przt=Number(dgby('alk_5').value).toFixed(2);
		end_aroma_przt=Number(dgby('arpct_5').value).toFixed(2);

		// End-Prozente in ml:
		end_pg_ml=((end_menge_ml/100)*end_pg_przt).toFixed(2);
		end_vg_ml=((end_menge_ml/100)*end_vg_przt).toFixed(2);
		end_alk_ml=((end_menge_ml/100)*end_alk_przt).toFixed(2);

		// Prozentverteilung des Aromas
		aroma_przt_pg=Number(dgby('pg_4').value).toFixed(2);
		aroma_przt_vg=Number(dgby('vg_4').value).toFixed(2);
		aroma_przt_alk=Number(dgby('alk4').value).toFixed(2);

		// davon sind die Mengen aus dem Aroma fix, die vom Grundliquid sollen dann angepasst sein
		aroma_ml=((end_menge_ml/100)*end_aroma_przt).toFixed(2);
		aroma_ml_pg=((aroma_ml/100)*aroma_przt_pg).toFixed(2);
		aroma_ml_vg=((aroma_ml/100)*aroma_przt_vg).toFixed(2);
		aroma_ml_alk=((aroma_ml/100)*aroma_przt_alk).toFixed(2);

		// also sind die fehlenden ml der einzelnen Zutaten:
		basis_ml=(end_menge_ml-aroma_ml).toFixed(2);
		basis_ml_pg=(end_pg_ml-aroma_ml_pg).toFixed(2);
		basis_ml_vg=(end_vg_ml-aroma_ml_vg).toFixed(2);
		basis_ml_alk=(end_alk_ml-aroma_ml_alk).toFixed(2);
		basis_przt_pg=(((end_pg_ml-aroma_ml_pg)/basis_ml)*100).toFixed(2);
		basis_przt_vg=(((end_vg_ml-aroma_ml_vg)/basis_ml)*100).toFixed(2);
		basis_przt_alk=(((end_alk_ml-aroma_ml_alk)/basis_ml)*100).toFixed(2);

		// Nikotinumrechnung
		let nico_gewuenscht_mg=Number(dgby('nic_5').value).toFixed(2);
		let nico_benoetigt=((end_menge_ml*nico_gewuenscht_mg)/basis_ml).toFixed(2);

		// noch checken, ob die Werte überhaupt legal sind
		function chkminimum(ml1,ml2,stoff){
			if ((ml1-ml2) < 0) {
				minpct=(ml2/end_menge_ml)*100;
				window.alert('Minimum '+minpct+'% '+stoff+' sind durch das Aroma vorhanden');
				return false
			} else {
				return true;
			}
		}
		if (chkminimum(end_pg_ml,aroma_ml_pg,'PG') &&	chkminimum(end_vg_ml,aroma_ml_vg,'VG') && chkminimum(end_alk_ml,aroma_ml_alk,'PG')) {
			// Werte ins Dokument schreiben
			dgby('ml4').value=aroma_ml;
			dgby('ml3').value=basis_ml;
			dgby('nic3').value=nico_benoetigt;
			dgby('pg_3').value=basis_przt_pg;
			dgby('vg_3').value=basis_przt_vg;
			dgby('alk3').value=basis_przt_alk;
		} else {
			dgby('pg_5').value=null;
			dgby('vg_5').value=null;
			dgby('alk_5').value=null;
		}
	}
}

function chk100_2() {
	var overall=Number(dgby('einzelmenge').value);
	var ar_ml=Number(dgby('aromagesamt').value);
	var overall_ml=Number(overall*(ar_ml/100));

	dgby('aromagesamtml').value=overall_ml;



	var ins=document.getElementsByClassName('arpct');
	var outs=document.getElementsByClassName('arml');
	var suma=0;

	for (var i=0; i < ins.length; i++) {
		//console.log(i);
		var curpct=ins[i];
		var curml=outs[i];
		suma += Number(curpct.value) || 0;
		curml.value=(curpct.value*(overall_ml/100));
	}
	su=dgby('sum').value=suma;
	if (su !== 100) {
		dgby('sum').style.background="#c65353"
	} else {
		dgby('sum').style.background="#254519"
	}

}

function ausblenden(tabelle,ausblender) {
	if (dgby(tabelle).style.display !== 'none') {
	dgby(tabelle).style.display='none';
	dgby(ausblender).style.display='none';
	} else {
	dgby(tabelle).style.display='';
	dgby(ausblender).style.display='';

	}
}

//window.onload=switch2();
