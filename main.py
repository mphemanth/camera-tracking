import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web

import os.path
import uuid
from tornado import escape
from tornado.options import define, options
import datetime
import json
import socket
import struct
import math
import network



ownIP=''

#Application class initialization
class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
	    (r"/comm_socket",network.commHandler),

        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
	self.render("index.html")



def main():
	network.fp=open("data",'w')	
	tornado.options.parse_command_line()
	app = Application()
	app.listen(options.port)
	x=tornado.ioloop.IOLoop.instance()
#	genericSocket=network.udpSocket(ownIP,30201,x,processor.genericPacketHandler,256)
	x.start()

	



if __name__ == "__main__":
    main()
