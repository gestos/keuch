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

		let delform = document.createElement("form");
		delform.method="POST";
		delform.name="delform";
		delform.action="vars.php";
		delform.target="phpm";

		let delbut = document.createElement("input");
		delbut.type="submit";
		delbut.className="delbutton";
		delbut.name="del_"+marken[i].tag;
		delbut.value="del";

		let hidput = document.createElement("input");
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
	togglebutton.style.width='175px';
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
	togglebutton2.style.width='175px';
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
		if(! (currval['hersteller'] in acc)){     // if hersteller of current object is not in the accumulator object yet
			acc[currval['hersteller']] = [];				// a new array by the name of the hersteller is created
			const idtaste ={};											// a new empty object is created
			idtaste['id'] = currval['id'];	// a new key-value pair for the above object: id of the current iteration gets the value geschmack of c.i.
			idtaste['geschmack'] = currval['geschmack'];
			idtaste['ml'] = currval['ml'];
			acc[currval['hersteller']].push(idtaste);
		}
		else {
			const idtaste ={};
			idtaste['id'] = currval['id'];	// a new key-value pair for the above object: id of the current iteration gets the value geschmack of c.i.
			idtaste['geschmack'] = currval['geschmack'];
			idtaste['ml'] = currval['ml'];
			acc[currval['hersteller']].push(idtaste);
		}
		return acc;
	},{});
	for (let hersteller_aromen in reduced) {
		reduced[hersteller_aromen].sort(sortObjByName);
	}
	return reduced;
}
function generate_flavorlist2(obj){
	let realtable = liste_kpl.children[0];
	for (let brand in obj) {
		let brandlist = obj[brand];
		let brtag = marken.find(item => item.firma == brand).tag;

		tr0 = document.createElement('tr');
		tr0.id = brtag;
		tr0.className="flavor_header";
		tr0.onclick=hide_some;
		td0 = tr0.insertCell();
		td0.colSpan=5;
		td0.innerHTML=brand+" ein/ausblenden";
		realtable.appendChild(tr0);

		for(let i=0;i<brandlist.length;i++){
			let aromaobjekt = brandlist[i];
			let id = aromaobjekt['id'];
			let taste = aromaobjekt['geschmack'];
			let ml = aromaobjekt['ml'];

			tr1 = document.createElement('tr'); 
			tr1.className = brtag+"_row";

			td1 = tr1.insertCell(); // hersteller
			td2 = tr1.insertCell(); // geschmack
			td3 = tr1.insertCell(); // ml
			td4 = tr1.insertCell(); // delete
			td5 = tr1.insertCell(); // edit

			// fill cells with value
			td1.innerHTML = brtag;
			td2.innerHTML = taste;
			// td3:
			let mlfeld = document.createElement('input');
			mlfeld.name="aroma_ml";
			mlfeld.size="4";
			mlfeld.value=ml;
			mlfeld.onblur=function(){ml_hidden.value=mlfeld.value};
			td3.appendChild(mlfeld);
			// td4:
			let delform2 = document.createElement("form");
			delform2.method="POST";
			delform2.name="delform2";
			delform2.action="vars.php";
			delform2.target="phpm";
			let delbut = document.createElement("input");
			delbut.type="submit";
			delbut.name="del_flav";
			delbut.className="delbutton";
			delbut.value="del";
			delform2.appendChild(delbut);
			let idfeld = document.createElement('input');
			idfeld.className="hidden";
			idfeld.name="aroma_id";
			idfeld.value=id;
			delform2.appendChild(idfeld);
			td4.appendChild(delform2);
			// td5:
			let ml_form = document.createElement("form");
			ml_form.method="POST";
			ml_form.name="edit_ml";
			ml_form.action="vars.php";
			ml_form.target="phpm";
			let mlbut = document.createElement("input");
			mlbut.type="submit";
			mlbut.name="ml_anpassen";
			mlbut.className="updatebutton";
			mlbut.value="update";
			let ml_hidden = document.createElement('input');
			ml_hidden.className="hidden";
			ml_hidden.name="hidden_ml";
			ml_hidden.value=mlfeld.value;
			let idfeld2 = document.createElement('input');
			idfeld2.className="hidden";
			idfeld2.name="aroma_id";
			idfeld2.value=id;
			ml_form.appendChild(mlbut);
			ml_form.appendChild(ml_hidden);
			ml_form.appendChild(idfeld2);
			td5.appendChild(ml_form);

			realtable.appendChild(tr1);
		}
	}
}
function hide_some(man) {
	let nodename_tohide=man.target.parentNode.id;
	let class2hide = nodename_tohide+"_row";
	let class_elmts = document.getElementsByClassName(class2hide);
	for (let row of class_elmts) {
		if(	row.hidden === true ) {
			row.hidden = false;
		}
		else {
			row.hidden = true;
		}
	}
}
function liq_generate() {
	let liq_tab=dgby('liquidliste');
	let arN = /^Aro.*\d$/
	let arP = /^Aro.*pct$/

	// table header
	let headrow=liq_tab.insertRow();
	for (var zutat in liquids[0]){
		if (zutat === 'id' || zutat === 'hash'){
			continue;
		}

		let zut_head=document.createElement('th');
		if (arN.test(zutat)){
			zut_head.innerHTML="Aroma";
		} 
		else if (arP.test(zutat)) {
			zut_head.innerHTML="%";
		} 
		else {
			zut_head.innerHTML=zutat;
		}
		headrow.appendChild(zut_head);
	}
	let modhead=headrow.insertCell();
	modhead.innerHTML="";
	let updatehead=headrow.insertCell();
	updatehead.innerHTML="";

	// rows with liquids
	for (i=0;i<liquids.length;i++){
		let liquid=liquids[i];
		updateform = document.createElement('form');
		updateform.method = 'post';
		updateform.action = 'vars.php';
		updateform.target = 'phpm';
		zeile=liq_tab.insertRow();
		zeile.id="liq_no_"+liquid.id;
		for (let bestandteil in liquid){
			if(bestandteil === 'id' || bestandteil === 'hash') {
				continue;
			}
			let zelle=zeile.insertCell();
			if (bestandteil === 'rating' || bestandteil === 'comment') {
				let editable=document.createElement('input');
				editable.value=liquid[bestandteil];
				editable.readOnly=true;
				if(bestandteil === 'rating'){
					editable.size='2';
				}
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

		// create form for php submit
		let updatecolumn = zeile.insertCell();
		updateform = document.createElement('form');
		updateform.name = 'update_'+liquid.id;
		updateform.method = 'post';
		updateform.action = 'vars.php';
		updateform.target = 'phpm';
		updatecolumn.appendChild(updateform);

		// create hidden input fields for php submit
		hashfield = document.createElement('input');
		hashfield.type = "hidden";
		hashfield.value = liquid['hash'];
		hashfield.name = 'hash';
		ratingfield = document.createElement('input');
		ratingfield.type = "hidden";
		ratingfield.value = liquid['rating'];
		ratingfield.name = 'rating';
		ratingfield.id = 'rating_'+liquid.id;
		commentfield = document.createElement('input');
		commentfield.type = "hidden";
		commentfield.value = liquid['comment'];
		commentfield.name = 'comment';
		commentfield.id = 'comment_'+liquid.id;
		updatebutton = document.createElement('input');
		updatebutton.type = 'submit';
		updatebutton.name = 'comment_update';
		updatebutton.className = 'updatebutton';
		updatebutton.value = 'save';
		updateform.appendChild(hashfield);
		updateform.appendChild(ratingfield);
		updateform.appendChild(commentfield);
		updateform.appendChild(updatebutton);

		// create form for php delete
		let delcolumn = zeile.insertCell();
		delform = document.createElement('form');
		delform.name = 'del_'+liquid.id;
		delform.method = 'post';
		delform.action = 'vars.php';
		delform.target = 'phpm';
		delcolumn.appendChild(delform);
		let delbutton = document.createElement('input');
		delbutton.type = 'submit';
		delbutton.className = 'delbutton';
		delbutton.name = 'liq_delete';
		delbutton.value = 'del';
		delfield = document.createElement('input');
		delfield.type = "hidden";
		delfield.value = liquid['hash'];
		delfield.name = 'delete';
		delform.appendChild(delfield);
		delform.appendChild(delbutton);
	}
}
function make_edit() {
	let parentrow = this.parentNode.parentNode;
	let in_left1=parentrow.children[16].children[0];
	let in_left2=parentrow.children[17].children[0];
	let rate_to_submit=parentrow.children[19].children[0][1];
	let comment_to_submit=parentrow.children[19].children[0][2];
	let subbutt=parentrow.children[19].children[0][3];
	if(in_left1.readOnly) {
		in_left1.readOnly = false;
		in_left2.readOnly = false;
		in_left1.className="commentEdit";
		in_left2.className="commentEdit";
		subbutt.disabled=true;
	}
	else {
		in_left1.readOnly = true;
		in_left2.readOnly = true;
		rate_to_submit.value=in_left1.value;
		comment_to_submit.value=in_left2.value;
		in_left1.className="";
		in_left2.className="";
		subbutt.disabled=false;
	}
}
function sortObjByName(compA, compB) {
	let nameA = compA["geschmack"].toLowerCase();
	let nameB = compB["geschmack"].toLowerCase();
	if (nameA.localeCompare(nameB) === -1 ) {
		return -1;
	}
	else {
		return 1;
	}
}
