function funx() {
	var var1=200,var2=200,var3=50;
	var breaks1=(200/450),breaks2=(50/450);
	console.log(breaks1,breaks2);
	var b1=Number(breaks1).toPrecision(2);
	var b2=Number(breaks2).toPrecision(2);
	var sum=Number(b1)+Number(b2);
	console.log(b1,b2,sum);
}
