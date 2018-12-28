var dgby=function( id ) { return document.getElementById( id ); };



function shoot() {
	var a1 = dgby('ar1').value || '-';
	var a2 = dgby('ar2').value || '-';
	var a3 = dgby('ar3').value || '-';
	var a4 = dgby('ar4').value || '-';
	var a5 = dgby('ar5').value || '-';
	var a1p = dgby('aroma1pct').value || '0'+"%";
	var a2p = dgby('aroma2pct').value || '0'+"%";
	var a3p = dgby('aroma3pct').value || '0'+"%";
	var a4p = dgby('aroma4pct').value || '0'+"%";
	var a5p = dgby('aroma5pct').value || '0'+"%";
	var flv_liq = String(dgby('arpct_5').value) + "%";
	var nic_liq = String(dgby('nic_5').value) + " mg";
	var pvg_liq = Number.parseFloat(dgby('pg_5').value).toFixed(1) + "/" + Number.parseFloat(dgby('vg_5').value).toFixed(1) + "%";
	var todai = new Date();
	var todate = todai.getDate()+'.'+todai.getMonth()+'.'+todai.getFullYear()
	console.log(todate);
	console.log(a1,a1p);



	labeldiv = dgby('etikettenliste');
	newtab = document.createElement('table');
	newtab.className = 'labeltable';

	tr1 = newtab.insertRow(); 

	acll1 = tr1.insertCell();
	acll1.innerHTML=a1;
	apcll1 = tr1.insertCell();
	apcll1.innerHTML=a1p;
	trenn = tr1.insertCell();
	trenn.className="trenner";
	trenn.rowSpan = 5;
	argesamt = tr1.insertCell();
	argesamt.innerHTML="Aroma/Liq";
	argesamtpct = tr1.insertCell();
	argesamtpct.innerHTML = flv_liq;

	tr2 = newtab.insertRow();

	acll2 = tr2.insertCell();
	acll2.innerHTML=a2;
	apcll2 = tr2.insertCell();
	apcll2.innerHTML=a2p;
	pvgcll = tr2.insertCell();
	pvgcll.innerHTML="PG/VG";
	pvpct = tr2.insertCell();
	pvpct.innerHTML=pvg_liq;

	tr3 = newtab.insertRow();

	acll3 = tr3.insertCell();
	acll3.innerHTML=a3;
	apcll3 = tr3.insertCell();
	apcll3.innerHTML=a3p;
	nicll = tr3.insertCell();
	nicll.innerHTML="Nic";
	nicpcll = tr3.insertCell();
	nicpcll.innerHTML=nic_liq;

	tr4 = newtab.insertRow();

	acll4 = tr4.insertCell();
	acll4.innerHTML=a4;
	apcll4 = tr4.insertCell();
	apcll4.innerHTML=a4p;
	datcll = tr4.insertCell();
	datcll.innerHTML="Datum";
	datvcll = tr4.insertCell();
	datvcll.innerHTML=todate;

	tr5 = newtab.insertRow();

	acll5 = tr5.insertCell();
	acll5.innerHTML=a5;
	apcll5 = tr5.insertCell();
	apcll5.innerHTML=a5p;
	removal = tr5.insertCell();
	rembutton = document.createElement("input");
	rembutton.className="pushbuttonr";
	rembutton.type="button";
	rembutton.id="remover";
	rembutton.value="Etikett loeschen";
	rembutton.onclick=function(){
		console.log(this);
		console.log(this.parentElement);
		console.log(this.parentElement.parentElement);
		console.log(this.parentElement.parentElement.parentElement);
		console.log(this.parentElement.parentElement.parentElement.parentElement);
		this.parentElement.parentElement.parentElement.parentElement.remove();
		return false;
	}
	removal.appendChild(rembutton);

	labeldiv.appendChild(newtab);
}
