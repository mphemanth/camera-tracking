
$( function() {

	COMM.init(NETWORK.webSocketAdd);
	COMM.start();
	TIMER.init();
	Mainloop();
	CANVAS.init(document.getElementById('myCanvas'));
	
} );


function Mainloop(){
document.getElementById('timestamp').innerHTML=moment().format('MMMM Do YYYY, h:mm:ss a');
requestAnimationFrame(Mainloop);
}
