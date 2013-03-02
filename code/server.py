import pdb
from json import loads as json_loads
from json import dumps as json_dumps
from Queue import Queue
from datetime import datetime
from threading import Lock

import tornado.ioloop
import tornado.web
import tornado.websocket

from engine import WebCoProcessor, QueryEngine
from util import Object


lock_register = Lock()

class DemoHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("demo.html")

class WebCoProcessorHandler(tornado.websocket.WebSocketHandler):
	"""
	- http://www.tornadoweb.org/documentation/websocket.html (this is the one to use)
	
	The Web Sockets API enables web browsers to maintain a bi-directional 
	communication channel to a server, which in turn makes implementing 
	real-time web sites about 1000% easier than it is today.
	"""
	def allow_draft76(self):
		return True
	
	def initialize(self, webcoprocessor):
		self.webcoprocessor = webcoprocessor
		self.connect_time = datetime.now()
	
	def write_message_json(self, obj):
		self.write_message( json_dumps(obj.__dict__) )
	
	def open(self):
		# pdb.set_trace() # let's see what info we have
		self.webcoprocessor.add_core( self )
		print "webcore joining. num_cores:", self.webcoprocessor.num_cores()
				
	def on_message(self, message):
		"""Received a message from a web core"""
		msg_from_core = WCPMessage.parse_message(message)
		
		print msg_from_core.message_type, msg_from_core.data

		#if msg_from_core.message_type == 'init':
			# web core saying hi!
		#	pass

		if msg_from_core.message_type == 'result':
			# web core has computed a JSON result
			self.webcoprocessor.output_buffer.put( msg_from_core.data )

		# no need to answer web cores back, but this is how you'd do it:
		# - self.write_message( json_dumps(obj.__dict__)  )

	def on_close(self):
		self.webcoprocessor.remove_core( self )
		print "webcore leaving. num_cores:", self.webcoprocessor.num_cores(), "; avg_core_life (sec):", self.webcoprocessor.avg_core_life 

class QueryEngineHandler(tornado.websocket.WebSocketHandler):
	
	def initialize(self, queryengine):
		self.queryengine = queryengine
		
	def open(self):
		pass
		
	def on_message(self, message):
		pass	

	def on_close(self):
		pass

class WCPMessage(Object):
	"""Based on anonymous object"""
	
	@staticmethod
	def parse_message( message ):
		return WCPMessage( **json_loads(message) )


if __name__ == "__main__":
	
	settings = {
				"static_path": "static",
				"template_path": "html"
	}
	
	# TODO, add persistence via leveldb or tightdb
	webcoprocessor = WebCoProcessor( input_buffer=Queue(), output_buffer=Queue() ) # The web co-processor (WCP)
	queryengine = QueryEngine( webcoprocessor ) # query engine executes queries on WCP
	
	application = tornado.web.Application([
		(r"/demo", DemoHandler),
		(r'/webcoprocessor/attach', WebCoProcessorHandler, dict(webcoprocessor=webcoprocessor)),
		(r'/queryengine/attach', QueryEngineHandler, dict(queryengine=queryengine))
	],**settings)

	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()