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
function generate_manuf_selections(selection) {
	// set an initial empty value
	sel = document.createElement("option");
	selection.appendChild(sel);
	// get the rest of the values from the manufacturer list
	for (j=0; j<manlist_by_freq.length; j++) {
		sel = document.createElement("option");
		sel.value = manlist_by_freq[j];
		sel.innerHTML = manlist_by_freq[j];
		selection.appendChild(sel);
	} 
}
function load_aro(selection_element) {
	var taste_sel=dgby(mapping_objekt[selection_element.id]);
	taste_sel.innerHTML = '';

	var chosenbrand=selection_element.value;	
	var label = marken.filter(obj => {
		return obj.firma === chosenbrand
	})

	if(label === undefined || label.length == 0){
		taste_sel.value='';
	}
	else {
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
	chk100_2();
} 
var manlist_by_freq=aromen_bycount(aromen);
var mapping_objekt={'aromaselect1':'geschmack1', 'aromaselect2':'geschmack2', 'aromaselect3':'geschmack3', 'aromaselect4':'geschmack4', 'aromaselect5':'geschmack5'};
// create a selection of manufacturers that are available
var herstellerfelder=Object.keys(mapping_objekt);
for (feld of herstellerfelder){
	var aro_sel = dgby(feld);
	generate_manuf_selections(aro_sel);
}
