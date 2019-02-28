const dgby=function( id ) { return document.getElementById( id ); };
const mapping_objekt={'aromaselect1':'geschmack1', 'aromaselect2':'geschmack2', 'aromaselect3':'geschmack3', 'aromaselect4':'geschmack4', 'aromaselect5':'geschmack5'};
function collapse(block) {
	klapp=dgby(block);
	//console.log(klapp);
	dgby(block).style.display = dgby(block).style.display == "block" ? "none" : "block";
}
// ALLGEMEINE FUNKTIONEN
// check several values for 100
function chk100(pg,vg,alk,nic) {
	var1 = Number(dgby(pg).value);
	var2 = Number(dgby(vg).value);
	var3 = Number(dgby(alk).value);
	summe=var1+var2+var3;
	// console.log(var1,var2,var3,summe);
	if (summe >= 99.99 && summe <= 100) {
		dgby(pg).className="okfeld";
		dgby(vg).className="okfeld";
		dgby(alk).className="okfeld";
		return true;
	} else {
		dgby(pg).className="failfeld";
		dgby(vg).className="failfeld";
		dgby(alk).className="failfeld";
		return false;
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
		dgby('mlz').className="okfeld";
		dgby('go1').disabled=false;
	} else {
		dgby('mlz').className="failfeld";
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
	var list=['pg_rein','vg_rein','alkrein','pgz','vgz','alkz','mlz'];
	for (var i=0; i<list.length; i++) {
		// console.log(i);
		dgby(list[i]).removeAttribute('style');
		dgby(list[i]).className="";
		dgby(list[i]).value=null;
	}
	if (flick('switcher1') == true) {
		dgby('pg_rein').readOnly=false;
		dgby('vg_rein').readOnly=false;
		dgby('alkrein').readOnly=false;
		dgby('mlz').readOnly=true;
		dgby('pgz').readOnly=true;
		dgby('vgz').readOnly=true;
		dgby('alkz').readOnly=true;
		dgby('go1').disabled=false;
	} else {
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
		var pgpct=Number(dgby('pgz').value).toFixed(2),
			vgpct=Number(dgby('vgz').value).toFixed(2),
			alkpct=Number(dgby('alkz').value).toFixed(2),
			ml=Number(dgby('mlz').value).toFixed(2),
			pgml=((ml/100)*pgpct).toFixed(2),
			vgml=((ml/100)*vgpct).toFixed(2),
			alkml=((ml/100)*alkpct).toFixed(2);
		dgby('pg_rein').value=pgml;
		dgby('vg_rein').value=vgml;
		dgby('alkrein').value=alkml;
	} else if (flick('switcher1') == true) {
		var pgml=Number((dgby('pg_rein').value) || 0).toFixed(2),
			vgml=Number((dgby('vg_rein').value) || 0).toFixed(2),
			alkml=Number((dgby('alkrein').value) || 0).toFixed(2),
			ml=  (parseFloat(pgml) + parseFloat(vgml) + parseFloat(alkml)).toFixed(2),
			pgpct=(((pgml/ml)*100) || 0).toFixed(2),
			vgpct=(((vgml/ml)*100) || 0).toFixed(2),
			alkpct=(((alkml/ml)*100) || 0).toFixed(2);
		//console.log(pgml,vgml,alkml,ml,pgpct,vgpct,alkpct);
		dgby('mlz').value=ml;
		dgby('pgz').value=pgpct;
		dgby('vgz').value=vgpct;
		dgby('alkz').value=alkpct;
	}
}
function hilite(felder) {
	//	console.log(felder);
	for (var i in felder.basis) {
		dgby(felder.basis[i]).className='ausgangswert';
	}
	for (var i in felder.ziel) {
		dgby(felder.ziel[i]).className='zielwert';
	}
	for (var i in felder.neutral) {
		dgby(felder.neutral[i]).className='';
	}
}
var labeltexte={
	slider1:{
		label:'slider1_label',
		vonoben:'<span class="von">&#8595</span>',
		keine:'-',
		vonunten:'<span class="nach">&#8593</span>',
		felder:{oben:['pgz','vgz','alkz'],unten:['pgb1','vgb1','alk1'],exe:'ubertrag1'}
	},
	slider2:{
		label:'slider2_label',
		vonoben:'<span class="von">&#8595</span>',
		keine:'-',
		vonunten:'<span class="nach">&#8593</span>',
		felder:{oben:['pgbz','vgbz','alkz1','nicz'],unten:['pg_3','vg_3','alk3','nic3'],exe:'ubertrag2'}
	},
	slider3:{
		label:'slider3_label',
		vonoben:'<span class="von">&#8595</span>',
		keine:'-',
		vonunten:'<span class="nach">&#8593</span>',
		felder:{oben:['arpct_5','ml_5'],unten:['aromagesamt','einzelmenge'],exe:'ubertrag3'}
	}
}
function slideopt(slider) {
	state=dgby(slider.id).value;
	sliderID=slider.id;
	felder=labeltexte[sliderID].felder;

	if (state == 0) {
		felder.basis=felder.oben, felder.ziel=felder.unten, felder.neutral = [];
		hilite(labeltexte[sliderID].felder);
		dgby(labeltexte[sliderID].label).innerHTML=labeltexte[sliderID].vonoben;
		dgby(felder.exe).disabled=false;
	} else if (state == 1) {
		felder.neutral = felder.oben.concat(felder.unten);
		hilite(labeltexte[sliderID].felder);
		dgby(labeltexte[sliderID].label).innerHTML=labeltexte[sliderID].keine;
		dgby(felder.exe).disabled=true;
	} else if (state == 2) {
		felder.basis=felder.unten, felder.ziel=felder.oben, felder.neutral = [];
		hilite(labeltexte[sliderID].felder);
		dgby(labeltexte[sliderID].label).innerHTML=labeltexte[sliderID].vonunten;
		dgby(felder.exe).disabled=false;
	}

}
function ubernehm(button) {
	var abschnitte={ubertrag1:'slider1',ubertrag2:'slider2',ubertrag3:'slider3'};
	buttonID=button.id;
	slider=abschnitte[buttonID];
	state=dgby(slider).value;
	felder=labeltexte[slider].felder;
	if (state == 0) {
		felder.basis=felder.oben, felder.ziel=felder.unten, felder.neutral = [];
		//console.log(felder.basis,felder.ziel);
		for (var i in felder.ziel) {
			//console.log(dgby(felder.ziel[i]).value);
			//console.log(dgby(felder.basis[i]).value);
			dgby(felder.ziel[i]).value=dgby(felder.basis[i]).value;
		}
	}
	else if (state == 2) {
		felder.basis=felder.unten, felder.ziel=felder.oben, felder.neutral = [];
		//console.log(felder.basis,felder.ziel);
		for (var i in felder.ziel) {
			//console.log(dgby(felder.ziel[i]).value);
			//console.log(dgby(felder.basis[i]).value);
			dgby(felder.ziel[i]).value=dgby(felder.basis[i]).value;
		};
	};
	/* console.log(buttonID); */
	if (buttonID == 'ubertrag3') {
		chk100_2();
	}
	dgby(slider).value=1;
	slideopt(dgby(slider));
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
	let nic_bb = Number(dgby(nicbb).value).toFixed(2);
	let nic_liq = Number(dgby(nicliq).value).toFixed(2);
	let ml = Number(dgby(mlliq).value).toFixed(2);

	if ((nic_bb < 1 || nic_bb > 250)) {
		dgby('nic2').className="failfeld";
	} else {
		dgby('nic2').className="okfeld";
	};
	if ((nic_liq < 0.5 || nic_liq > 32)) {
		dgby('nicz').className="failfeld";
	} else {
		dgby('nicz').className="okfeld";
	};
	if (ml < 10) {
		dgby('mlliq').className="failfeld";
	} else {
		dgby('mlliq').className="okfeld";
	};
	if ((nic_bb < 1 || nic_bb > 250) || (nic_liq < 0.5 || nic_liq > 32) || (ml < 10)) {
		return false;
	} else {
		return true;
	}
}
// mischung ausrechnen
function calculate_nic(liq_menge,liq_nic,bb_nic) {
	let liqmenge				=	Number(dgby(liq_menge).value).toFixed(2);
	let bb_nic_gehalt		=	Number(dgby(bb_nic).value).toFixed(2);
	let liq_nic_gehalt	=	Number(dgby(liq_nic).value).toFixed(2);

	let ml_menge_bb = (liqmenge/(bb_nic_gehalt/liq_nic_gehalt)).toFixed(2);
	let ml_menge_nb = (liqmenge-ml_menge_bb).toFixed(2);
	return [ml_menge_nb,ml_menge_bb];
}

function get_pct(nullerbase,bunkerbase,ml_nb,ml_bb) {
	let liqmenge				=	Number(dgby('mlliq').value).toFixed(2);
	let pct_nb = Number(dgby(nullerbase).value).toFixed(2);
	let pct_bb = Number(dgby(bunkerbase).value).toFixed(2);
	let pct_liq = ((ml_nb*pct_nb)/liqmenge+(ml_bb*pct_bb)/liqmenge).toFixed(2);
	return pct_liq;
}
function calculate_liq () {
	if (flick('switcher2') == false) {
		let mls=calculate_nic('mlliq','nicz','nic2'), ml_nb=mls[0], ml_bb=mls[1];
		//console.log(mls, ml_bb, ml_nb);
		let percent_pg_liq = Number(get_pct('pgb1','pgb2',ml_nb,ml_bb)).toFixed(2);
		let percent_vg_liq = Number(get_pct('vgb1','vgb2',ml_nb,ml_bb)).toFixed(2);
		let percent_alk_liq = Number(get_pct('alk1','alk2',ml_nb,ml_bb)).toFixed(2);
		//console.log('prozent pg: ',percent_pg_liq,' prozent vg: ',percent_vg_liq,' prozent alk: ',percent_alk_liq);
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
	//console.log('calc2pct');
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

	//console.log('BB ml_PG:',ml_pg_bb,' ml_VG:',ml_vg_bb,' ml_Alk:',ml_alk_bb);

	// diese Werte in ml soll das Ziel-Liquid haben:
	let ml_pg_liq=(menge_lq*(pct_pg_lq/100)).toFixed(2);
	let ml_vg_liq=(menge_lq*(pct_vg_lq/100)).toFixed(2);
	let ml_alk_liq=(menge_lq*(pct_alk_lq/100)).toFixed(2);

	//console.log('Liq ml_PG:',ml_pg_liq,' ml_VG:',ml_vg_liq,' ml_Alk:',ml_alk_liq);

	// diese Werte in ml werden von der NB benoetigt, um auf die Zielwerte zu kommen
	let ml_pg_nb=(ml_pg_liq-ml_pg_bb).toFixed(2);
	let ml_vg_nb=(ml_vg_liq-ml_vg_bb).toFixed(2);
	let ml_alk_nb=(ml_alk_liq-ml_alk_bb).toFixed(2);

	//console.log('NB ml_PG:',ml_pg_nb,' ml_VG:',ml_vg_nb,' ml_Alk:',ml_alk_nb);

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
	var Fo=['pgb1','vgb1','alk1','ml1'],Fu=['pgbz','vgbz','alkz1'],nc='nicz',Fa=Fo.concat(Fu);
	for (var i=0;i<Fa.length;i++) {
		dgby(Fa[i]).value=null;
		dgby(Fa[i]).removeAttribute('style');
		dgby(Fa[i]).className="";
	}
	if (flick('switcher2') == true) {
		for (var i=0;i<Fu.length;i++) {
			dgby(Fu[i]).readOnly=false;
			dgby(Fo[i]).readOnly=true;
		}
		dgby('misch_nuller').className="hiliterow";
		dgby('misch_ziel').className="";
	} else  if (flick('switcher2') == false) {
		for (var i=0;i<Fu.length;i++) {
			dgby(Fu[i]).readOnly=true;
			dgby(Fo[i]).readOnly=false;
		}
		dgby('misch_ziel').className="hiliterow";
		dgby('misch_nuller').className="";
	}
}

function switch3() {
	var Fo=['pg_3','vg_3','alk3','nic3'],Fu=['pg_5','vg_5','alk_5','nic_5'],Fm=['ml3','ml4'],Fa=Fo.concat(Fu).concat(Fm);
	for (var i=0;i<Fa.length;i++) {
		dgby(Fa[i]).value=null;
		dgby(Fa[i]).removeAttribute('style');
		dgby(Fa[i]).className="";
	}

	var swi='switcher3';
	if (flick(swi) == true) {
		for (var i=0;i<Fu.length;i++) {
			dgby(Fu[i]).readOnly=false;
			dgby(Fo[i]).readOnly=true;
		}
		dgby('Liq3').className="hiliterow"
		dgby('Ergebnis3').className=""
	} else  if (flick(swi) == false) {
		for (var i=0;i<Fu.length;i++) {
			dgby(Fo[i]).readOnly=false;
			dgby(Fu[i]).readOnly=true;
		}

		dgby('Liq3').className=""
		dgby('Ergebnis3').className="hiliterow"
	}
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
		//console.log(richtung);
		let row1=chk100('pg_3','vg_3','alk3');
		let row2=chk100('pg_4','vg_4','alk4');
		if (0 < nicsrc && nicsrc < 49) {
			dgby('nic3').className="okfeld";
			var nicok=true;
		} else {
			dgby('nic3').className="failfeld";
			var nicok=false;
		}
		if (0 < arpct && arpct < 51) {
			dgby('arpct_5').className="okfeld";
			var arok=true;
		} else {
			dgby('arpct_5').className="failfeld";
			var arok=false;
		}
		if (dgby('ml_5').value > 9) {
			dgby('ml_5').className="okfeld";
			var mengok=true;
		} else {
			dgby('ml_5').className="failfeld";
			var mengok=false;
		}
		if (row1 && row2 && nicok && arok && mengok) {
			dgby('go2').disabled=false;
		} else {
			dgby('go2').disabled=true;
		}
	} else {
		//console.log(richtung);
		let row2=chk100('pg_4','vg_4','alk4');
		let row1=chk100('pg_5','vg_5','alk_5');
		if (0 < nicdst && nicdst < 49) {
			dgby('nic_5').className="okfeld";
			var nicok=true;
		} else {
			dgby('nic_5').className="failfeld";
			var nicok=false;
		}
		if (0 < arpct && arpct < 51) {
			dgby('arpct_5').className="okfeld";
			var arok=true;
		} else {
			dgby('arpct_5').className="failfeld";
			var arok=false;
		}
		if (dgby('ml_5').value > 9) {
			dgby('ml_5').className="okfeld";
			var mengok=true;
		} else {
			dgby('ml_5').className="failfeld";
			var mengok=false;
		}
		if (row1 && row2 && nicok && arok && mengok) {
			dgby('go2').disabled=false;
		} else {
			dgby('go2').disabled=true;
		}
	}
	chk100_2();
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
	var overall=Number(dgby('einzelmenge').value).toFixed(2);
	var ar_ml=Number(dgby('aromagesamt').value).toFixed(2);
	var overall_ml=Number(overall*(ar_ml/100)).toFixed(2);

	dgby('aromagesamtml').value=overall_ml;

	var ins=document.getElementsByClassName('arpct');
	var outs=document.getElementsByClassName('arml');
	var suma=0;

	var einzelwerte_pztfelder = [];
	for (var i=0; i < ins.length; i++) {
		var curpct=ins[i];
		var curml=outs[i];
		suma += Number(curpct.value) || 0;
		curml.value=(curpct.value*(overall_ml/100)).toFixed(2);
		einzelwerte_pztfelder.push(curpct.value);
	}
	su=dgby('sum').value=suma;
	function pct_chk() {
		if (su !== 100) {
			dgby('sum').style.background="#c65353";
			return false;
		}
		else {
			dgby('sum').style.background="#c4fa9d";
			return true;
		}
	}

	// test if at least one flavour is set
	var catstr='';
	for (feld of Object.keys(mapping_objekt)) {
		feldstring=dgby(feld).value;
		catstr += feldstring;
	}
	function strng_check(catstr) {
		if(!catstr){
			return false;
		}
		else {
			return true;
		}
	}

	// test for negative perceantages
	function test_neg(pztarray) {
		for (let num of pztarray) {
			if (num < 0) {
				return false;
			} 
		}
		return true;
	}

	function volumencheck() {
		menge=dgby('einzelmenge').value;
		aromaanteil=dgby('aromagesamt').value;
		if( (menge > 0) && (aromaanteil>0) ){
			return true; 
		}
		else {
			return false;
		}
	}

	function nic_pg_check() {
		if(!dgby('nic_5').value || !dgby('pg_5').value || !dgby('vg_5').value){
			return false;
		}
		else{
			return true;
		}
	}

	let pc = pct_chk();
	let vol = volumencheck();
	let nic_pg = nic_pg_check();
	let str = strng_check(catstr);
	let neg = test_neg(einzelwerte_pztfelder);
	if( pc && vol && str && neg && nic_pg ) {
		dgby('shooter').disabled=false;
	} else {
		dgby('shooter').disabled=true;
	}
}
chk100_2();

function ausblenden(tabelle,ausblender) {
	if (dgby(tabelle).style.display !== 'none') {
		dgby(tabelle).style.display='none';
		dgby(ausblender).style.display='none';
	} else {
		dgby(tabelle).style.display='';
		dgby(ausblender).style.display='';

	}
}
