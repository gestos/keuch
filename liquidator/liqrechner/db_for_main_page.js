const manlist_by_freq=aromen_bycount(aromen);
var herstellerfelder=Object.keys(mapping_objekt);
// create an array of available manufacturers, sorted by frequency
function aromen_bycount(aroma_array) {
	if(!aromen){console.log("no db [aromen]"); return false;}
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
function build_selection_manufacturers(selection) {
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
// create a selection of manufacturers that are available
for (feld of herstellerfelder){
	var aro_sel = dgby(feld);
	build_selection_manufacturers(aro_sel);
}
const table_clone = dgby('klondiv').innerHTML;
function db_free_switch(button) {
	let einzelm = dgby('einzelmenge');
	let aromage = dgby('aromagesamt');
	if(button.value === 'set freehand mode'){
		let row3=document.getElementsByClassName('row3');
		for(let [feld1,feld2] of Object.entries(mapping_objekt)){
			let f1 = dgby(feld1); let f2 = dgby(feld2);
			var f1_clone = f1.cloneNode(true);
			let contain1 = f1.parentNode;
			let contain2 = f2.parentNode;
			f1.remove(); f2.remove();
			let in1 = document.createElement('input');
			in1.id = feld1;
			in1.inlineSize = "100px";
			in1.onblur = chk100_2; 
			contain1.className += " freehand_input";
			contain1.appendChild(in1);
		}
		while(row3[0]){
			row3[0].remove();
		}
		let db_buttons = document.getElementsByClassName('markirbox');
		for(let dbel of db_buttons){
			dbel.hidden = true;
		}
		button.value = 'set database mode';
	}
	else{ 
		dgby('klondiv').innerHTML = table_clone;
		let db_buttons = document.getElementsByClassName('markirbox');
		for(let dbel of db_buttons){
			dbel.hidden = false;
		}
		button.value = 'set freehand mode';
	}
}
db_free_switch(dgby('db_freehand_switch'));	// initale ausfuehrung, um auf db-freien modus zu schalten
