const dgby=function( id ) { return document.getElementById( id ); };
function styleswitch(button) {
	let style_array=[
		{no:0,name:"bright",url:"heller_style.css"},
		{no:1,name:"dark",url:"dunkler_style2.css"},
		{no:2,name:"blue",url:"dunkler_style.css"},
		{no:3,name:"scheme3",url:"scheme3.css"}	
	];
	let stylelink=dgby('style');
	
	let currentStyleName=button.value;
	let currentStyleObject = style_array.filter(function(objekt) {return objekt["name"] === currentStyleName})[0];
	let currentIndex=style_array.indexOf(currentStyleObject);

	console.log(currentIndex);

	function ix_reset() {
	if (currentIndex+1 >= style_array.length) {
		return 0;
	}
	else {
		return currentIndex+1;
	}
	}
	let nextIndex=ix_reset();
	console.log(nextIndex);

	let nextStyleObject = style_array[nextIndex];
	let nextStyleName = nextStyleObject['name'];
	let nextStyle = nextStyleObject['url'];

	stylelink.setAttribute('href',nextStyle);
	button.value = nextStyleName;

}
