const dgby=function( id ) { return document.getElementById( id ); };
const manuf_tab = dgby('herstellertabelle');
const liste_kpl = dgby('aromenliste');
const hersteller_objekt=get_herstellernamen();
const flavors_grouped = sort_flavors_bymanuf();
const manufacturers_table = create_manufacturer_list(manuf_tab);
const flavors_table = generate_flavorlist2(flavors_grouped);
const liquids_table = liq_generate();
function get_herstellernamen(){
	let hersteller={};
	for(marke in marken){
		let t=marken[marke].tag;
		let f=marken[marke].firma;
		hersteller[t]=f;
	}
	return hersteller;
}
function aromen_bycount(aroma_array) {
	console.log('aromen_bycount');
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
	if(this.id === "toggle_addform"){
		mnt=dgby('addform');
	}
	else if(this.id === "toggle_addflav"){
		mnt=dgby('addflav');
	}
	else {
		mnt=dgby(el);
	}
	if (mnt.style.visibility === "collapse") {

		mnt.style.visibility="visible";
	} else {
		mnt.style.visibility="collapse";
	}
}
function make_manuf_selection(targetElement,virt_real,all_or_available) {
	// create a selection of manufacturers that are available
	// console.log(targetElement, virt_real);
	if(virt_real === 'cell'){
		var aro_sel = document.createElement('select');
	}
	else {
		var aro_sel = dgby(targetElement);
	}

	if(all_or_available === 'alle'){
		var manlist_by_freq=Object.keys(get_herstellernamen());
	}
	else if(all_or_available === 'vorhandene'){
		var manlist_by_freq=aromen_bycount(aromen);
	}
	else {
		alert('bitte parameter beachten');
	}


	sel = document.createElement("option");
	aro_sel.appendChild(sel);
	for (i=0; i < manlist_by_freq.length; i++) {
		sel = document.createElement("option");
		sel.value = manlist_by_freq[i];
		sel.innerHTML = manlist_by_freq[i];
		aro_sel.appendChild(sel);
	}
	return aro_sel;
}
function create_manufacturer_list(table) {
	for (i = 0; i < marken.length; i++) {

		tr1 = table.insertRow(); 
		td1 = tr1.insertCell();
		td2 = tr1.insertCell();
		td3 = tr1.insertCell();
		td1.innerHTML = marken[i].tag;
		td2.innerHTML = marken[i].firma;

		var delform = document.createElement("form");
		delform.method="POST";
		delform.name="delform";
		delform.action="vars.php";
		delform.target="phpm";

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

	// Zeile mit Eingabemöglichkeit für weitere Hersteller
	var add_manu=table.insertRow();
	add_manu.className="add_toggle";
	var add_manu_td = add_manu.insertCell();
	add_manu_td.colSpan="3";
	var togglebutton=add_manu_td.appendChild(document.createElement('input'));
	togglebutton.type='button';
	togglebutton.style.width='200px';
	togglebutton.value="add another manufacturer";
	togglebutton.id="toggle_addform";
	togglebutton.onclick=toggle;

	var formrow=table.insertRow();
	formrow.id='addform';
	formrow.style.visibility='collapse';

	in_tag_cell=formrow.insertCell();
	in_tag=in_tag_cell.appendChild(document.createElement('input'));
	in_tag.size="2";
	in_tag.name="tag";
	in_tag.placeholder="Kürzel";
	in_tag_cell.appendChild(in_tag);

	in_firma_cell=formrow.insertCell();
	in_firma=in_firma_cell.appendChild(document.createElement('input'));
	in_firma.name="firma";
	in_firma.placeholder="Firmenname";
	in_firma_cell.appendChild(in_firma);

	manu_submitcell=formrow.insertCell();
	new_manu_submit=document.createElement('input');
	new_manu_submit.type='submit';
	new_manu_submit.name='new_manu';
	new_manu_submit.value='add';
	manu_submitcell.appendChild(new_manu_submit);

	// Zeile mit Eingabemöglichkeit für weitere Hersteller
	var add_flav=table.insertRow();
	var add_flav_td = add_flav.insertCell();
	add_flav_td.colSpan="3";
	var togglebutton2=add_flav_td.appendChild(document.createElement('input'));
	togglebutton2.type='button';
	togglebutton2.style.width='200px';
	togglebutton2.value="add another flavor";
	togglebutton2.id="toggle_addflav";
	togglebutton2.onclick=toggle;

	var flavrow=table.insertRow();
	flavrow.id='addflav';
	flavrow.style.visibility='collapse';

	selecta_cell=flavrow.insertCell();
	var hersteller_selektion=make_manuf_selection(selecta_cell, 'cell', 'alle');	
	hersteller_selektion.name="brand";
	hidden_map=document.createElement('input');
	hidden_map.className="hidden";
	hidden_map.name="hidden_map";
	hidden_map.id="hidden_map";
	hidden_map.value=JSON.stringify(get_herstellernamen());
	selecta_cell.appendChild(hidden_map);
	selecta_cell.appendChild(hersteller_selektion);

	gschmck_cell=flavrow.insertCell();
	gschmck=gschmck_cell.appendChild(document.createElement('input'));
	gschmck.name="Geschmack";
	gschmck.placeholder="Geschmack";
	gschmck_cell.appendChild(gschmck);

	flv_sub_cell=flavrow.insertCell();
	flv_sub=document.createElement('input');
	flv_sub.type='submit';
	flv_sub.name='new_flav';
	flv_sub.value='add';
	flv_sub_cell.appendChild(flv_sub);
}
function sort_flavors_bymanuf() {
	const reduced = aromen.reduce((acc, currval) => {
		if(currval['hersteller'] in acc){
			const idtaste ={};
			idtaste[currval['id']] = currval['geschmack'];
			acc[currval['hersteller']].push(idtaste);
		}
		else {
			acc[currval['hersteller']] = [];
			const idtaste ={};
			idtaste[currval['id']] = currval['geschmack'];
			acc[currval['hersteller']].push(idtaste);
		}
		return acc;
	},{});
	return reduced;
}
function generate_flavorlist2(obj){
	for (let brand in obj) {
		let brandlist = obj[brand];
		for(let i=0;i<brandlist.length;i++){
			let flava_id = brandlist[i];
			for(let id of Object.keys(flava_id)){
				let taste = flava_id[id];

				tr1 = liste_kpl.insertRow(); 
				td1 = tr1.insertCell();
				td2 = tr1.insertCell();
				td3 = tr1.insertCell();
				td4 = tr1.insertCell();
				td1.innerHTML = brand;
				td2.innerHTML = taste;
				//console.log(aromen[i].hersteller+' '+aromen[i].geschmack);

				var idfeld = document.createElement('input');
				idfeld.name="aroma_id";
				idfeld.id="aroma_id";
				idfeld.className="hidden";
				idfeld.value=id;
				//td3.appendChild(idfeld);

				var delform2 = document.createElement("form");
				delform2.method="POST";
				delform2.name="delform2";
				delform2.action="vars.php";
				delform2.target="phpm";
				var delbut = document.createElement("input");
				delbut.type="submit";
				delbut.name="del_flav";
				delbut.value="del";
				delform2.appendChild(delbut);
				delform2.appendChild(idfeld);
				td4.appendChild(delform2);
			}
		}
	}
}
function liq_generate() {
	var liq_tab=dgby('liquidliste');
	var arN = /^Aro.*\d$/
	var arP = /^Aro.*pct$/

	// table header
	var headrow=liq_tab.insertRow();
	for (var zutat in liquids[0]){
		if (zutat === 'id' || zutat === 'hash'){
			continue;
		}
		var zut_head=headrow.insertCell();
		if (arN.test(zutat)){
			zut_head.innerHTML="Aroma";
		} 
		else if (arP.test(zutat)) {
			zut_head.innerHTML="%";
		} 
		else {
			zut_head.innerHTML=zutat;
		}
	}
	var modhead=headrow.insertCell();
	modhead.innerHTML="";
	var updatehead=headrow.insertCell();
	updatehead.innerHTML="";

	// rows with liquids
	for (i=0;i<liquids.length;i++){
		let liquid=liquids[i];
		updateform = document.createElement('form');
		updateform.method = 'post';
		updateform.action = 'vars.php';
		updateform.target = 'phpm';
		zeile=liq_tab.insertRow();
		for (var bestandteil in liquid){
			//console.log(bestandteil);
			if(bestandteil === 'id' || bestandteil === 'hash') {
				continue;
			}
			var zelle=zeile.insertCell();
			if (bestandteil === 'rating' || bestandteil === 'comment') {
				//console.log("create input field");
				var editable=document.createElement('input');
				editable.size='2';
				editable.value=liquid[bestandteil];
				editable.readOnly=true;
				zelle.appendChild(editable);
			}
			else {
				zelle.innerHTML=liquid[bestandteil];
			}
		}
		editcolumn=zeile.insertCell();
		editbutton=document.createElement('input');
		editbutton.type='button';
		editbutton.value='edit';
		editbutton.onclick=make_edit;
		editcolumn.appendChild(editbutton);

		updatecolumn = zeile.insertCell();
		updateform = document.createElement('form');
		updateform.name = 'update_comment';
		updateform.method = 'post';
		updateform.action = 'vars.php';
		updateform.target = 'phpm';
		updatecolumn.appendChild(updateform);

		hashfield = document.createElement('input');
		hashfield.type = "hidden";
		hashfield.value = liquid['hash'];
		hashfield.name = 'hash';
		ratingfield = document.createElement('input');
		ratingfield.type = "hidden";
		ratingfield.value = liquid['rating'];
		ratingfield.name = 'rate';
		ratingfield.id = 'rating';
		commentfield = document.createElement('input');
		commentfield.type = "hidden";
		commentfield.value = liquid['comment'];
		commentfield.name = 'comm';
		commentfield.id = 'comment';
		updatebutton = document.createElement('input');
		updatebutton.type = 'submit';
		updatebutton.name = 'comment_update';
		updatebutton.value = 'save';
		updateform.appendChild(hashfield);
		updateform.appendChild(ratingfield);
		updateform.appendChild(commentfield);
		updateform.appendChild(updatebutton);
	}
}
function make_edit() {
	in_left1=this.parentNode.previousSibling.childNodes[0];
	in_left2=this.parentNode.previousSibling.previousSibling.childNodes[0];
	subbutt=this.parentNode.nextSibling.childNodes[0].childNodes[3];
	if(in_left1.readOnly) {
		in_left1.readOnly = false;
		in_left2.readOnly = false;
		subbutt.disabled=true;
	}
	else {
		in_left1.readOnly = true;
		in_left2.readOnly = true;
		dgby('rating').value=in_left2.value;
		dgby('comment').value=in_left1.value;
		subbutt.disabled=false;
	}
}
