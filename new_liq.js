var dgby=function( id ) { return document.getElementById( id ); };

function chk100(val1,val2,val3) {
	var1 = Number(dgby(val1).value);
	var2 = Number(dgby(val2).value);
	var3 = Number(dgby(val3).value);
	summe=var1+var2+var3;
	if (summe !== 100) {
		dgby(val1).style.background = "salmon";
		dgby(val2).style.background = "salmon";
		dgby(val3).style.background = "salmon";
	} else {
		dgby(val1).style.background = "lightgreen";
		dgby(val2).style.background = "lightgreen";
		dgby(val3).style.background = "lightgreen";
	}
	return summe;
}
function gochk(summ1,summ2) {
	if (summ1 == 100 &&  summ2 == 100) {
		dgby('go').disabled=false;
	}
}
function chkvalid() {
	summ1=chk100('pgb1','vgb1','alk1');
	summ2=chk100('pgb2','vgb2','alk2');
	gochk(summ1,summ2);
}
