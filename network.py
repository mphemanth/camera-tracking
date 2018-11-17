# this module handles all network related activities ( websocket,TCP/IP & UDP)
from tornado.options import define, options
import socket
import tornado.websocket
import logging
import json

from datetime import datetime as dt
define("port", default=88, help="run on the given port", type=int)



#open a udp socket with a handler at a given port number. 
#handler does the remaining work.
class udpSocket:
	def __init__(self,ip,cInfo,IOLoop,processor):
		self.N=70000
		self.cInfo=cInfo
		self.ip=ip
		self.processor=processor
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind( (ip, int(self.cInfo['port'])) )
		self.sock.setblocking(0)			
		IOLoop.add_handler(self.sock.fileno(), self.callback, IOLoop.READ)
	def callback(self,fd,events):
		(self.data, self.source_ip_port) = self.sock.recvfrom(self.N)
		self.processor(self.data,self.source_ip_port)


		
class commHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        commHandler.waiters.add(self)

    def on_close(self):
        commHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, data):
	for waiter in cls.waiters:
		try:
			waiter.write_message(data)
		except:
			logging.error("Error sending data", exc_info=True)

    def on_message(self, data):
		global fp
		#logging.info("Received data %r", data)
		#parsed = tornado.escape.json_decode(data)
		d1=  tornado.escape.json_decode(data)
		out=[]
		#print 'data:',d1,d1[u'x']
		if 'x' in d1:
			t1= dt.now()
			co=d1
			outstring= str(t1.year)+"-"+str(t1.month)+"-"+str(t1.day)+","+str(t1.hour)+":"+str(t1.minute)+":"+str(t1.second)+":"+str(t1.microsecond/1000)+","
			d3=[co[u'x'],co[u'y'],co[u'z']]
			d4=[float(i) for i in d3]
			d5=[round(i,4) for i in d4]
			outstring=outstring+","+str(d5[0])+","+str(d5[1])+","+str(d5[2])+"\n"
			fp.write(outstring)
			print outstring
		commHandler.send_updates(data)
