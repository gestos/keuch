var dgby=function( id ) { return document.getElementById( id ); };
var manuf_tab = dgby('herstellertabelle');

// create an array of available manufacturers, sorted by frequency
function aromen_bycount(aroma_array) {
	var counter = {};
	for (i=0;i<aromen.length;i++) {
		counter[aromen[i].hersteller] = 0;
	}
	for (i=0;i<aromen.length;i++) {
		counter[aromen[i].hersteller] += 1;
	}
	// console.log(counter);
	var sortable = [];
	for (var hersteller in counter) {
		sortable.push([hersteller, counter[hersteller]]);
	}
	sortable.sort(function(a, b) {
		return a[1] - b[1];
	});
	var manlist = [];
	for (i=0; i<sortable.length; i++){
		manlist.push(sortable[i][0]);
	}
	return manlist.reverse();
}

function toggle(el) {
	mnt=dgby(el);
	if (mnt.style.visibility === "collapse") {
		mnt.style.visibility="visible";
	} else {
		mnt.style.visibility="collapse";
	}
}

// create a table of all known manufacturers
for (i = 0; i < marken.length; i++) {

	tr1 = manuf_tab.insertRow(); 
	td1 = tr1.insertCell();
	td2 = tr1.insertCell();
	td3 = tr1.insertCell();
	td1.innerHTML = marken[i].tag;
	td2.innerHTML = marken[i].firma;

	var delform = document.createElement("form");
	delform.method="POST";
	delform.name="delform";
	delform.action="";

	var delbut = document.createElement("input");
	delbut.type="submit";
	delbut.name="del_"+marken[i].tag;
	delbut.value="del";

	var hidput = document.createElement("input");
	hidput.type="text";
	hidput.name="del_man";
	hidput.value=marken[i].tag;
	hidput.style.display="none";

	td3.appendChild(delform);
	delform.appendChild(delbut);
	delform.appendChild(hidput);
} 

// create a selection of manufacturers that are available
var aro_sel = dgby('aromaselect');
var manlist_by_freq=aromen_bycount(aromen);

sel = document.createElement("option");
aro_sel.appendChild(sel);
for (i=0; i < manlist_by_freq.length; i++) {
	sel = document.createElement("option");
	sel.value = manlist_by_freq[i];
	sel.innerHTML = manlist_by_freq[i];
	aro_sel.appendChild(sel);
}

// create selection of flavours for chosen brand
var taste_sel = dgby('geschmack');
function load_aro(manufacturer) {
	var chosenbrand=manufacturer.value;
	taste_sel.innerHTML = '';
	
	var label = marken.filter(obj => {
		return obj.firma === chosenbrand
	})

	var label_name = label[0].firma;
	var result = aromen.filter(obj => {
		return obj.hersteller === label_name
	})

	for (i=0;i<result.length;i++) {
		sel = document.createElement("option");
		sel.value = result[i].geschmack;
		sel.innerHTML = result[i].geschmack;
		taste_sel.appendChild(sel);
	}
}

// create a table containing all flvaours
var liste_kpl = dgby('aromenliste');
for (i=0;i<aromen.length;i++) {
	tr1 = liste_kpl.insertRow(); 
	td1 = tr1.insertCell();
	td2 = tr1.insertCell();
	td1.innerHTML = aromen[i].hersteller;
	td2.innerHTML = aromen[i].geschmack;
}





