// this file handles bi-directional communication between http server and  clients 
var COMM = {
    socket: null,
    url:null,
    init:function(path) {
    this.url="ws://"+path+'/comm_socket';
    },
	
    start: function() {
	
        if ("WebSocket" in window) {
	    this.socket = new WebSocket(this.url);
		GLOBAL.ws_status=1;
	document.getElementById('connectionStatus').innerHTML="connected";
        } else {

            this.socket = new MozWebSocket(this.url);
		GLOBAL.ws_status=1;
	document.getElementById('connectionStatus').innerHTML="connected";
        }
	
	this.socket.onopen=function(event)
	{
	//COMM.sendConfigRefreshSignal();
	}
	this.socket.onmessage = function(event) {
	    


		msg=JSON.parse(event.data);
		console.log(msg.x,msg.y,msg.z);
		mesh.rotation.x =msg.x*(Math.PI/180.0);
		mesh.rotation.y =-1*msg.y*(Math.PI/180.0);
		mesh.rotation.z =-1*msg.z*(Math.PI/180.0);
		$('#reportframe').innerHTML=event.data;
		renderer.render( scene, camera );

		
		
		
		}// end of om message


	this.socket.onclose=function(event){
		GLOBAL.ws_status=0;
		console.log('socket closed',event);
		document.getElementById('connectionStatus').innerHTML=" <button onclick='COMM.start();' class='ui-btn ui-corner-all'>disconnected.Click here to re-connect!</button>";

		}// end of on close
		
		
		

    },
	send:function(message){
	  this.socket.send(JSON.stringify(message));
	  },
	sendConfigRefreshSignal:function(){
	message={};
	message['refresh']=true;
	this.socket.send(JSON.stringify(message));
		
}
	





}
