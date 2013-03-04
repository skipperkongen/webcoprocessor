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
	TODO: Write what this is
	"""
	def allow_draft76(self):
		return True
	
	def initialize(self, webcoprocessor):
		self.webcoprocessor = webcoprocessor
		self.connect_time = datetime.now()
	
	def write_message_json(self, obj):
		self.write_message( json_dumps(obj.__dict__) )
	
	def open(self):
		self.webcoprocessor.add_core( self )
		print "webcore joining. num_cores:", self.webcoprocessor.num_cores()
				
	def on_message(self, text):
		"""Received a message from a web core"""
		message = Message.parse_json( text )
		
		print  message

		try:
			obj = Message(subtask_id=message.data['subtask_id'], result=message.data['result'])
			self.webcoprocessor.output_buffer.put( obj )
		except AttributeError:
			print "query object is missing 'subtask_id' or 'result' attribute"			

	def on_close(self):
		self.webcoprocessor.remove_core( self )
		print "webcore leaving. num_cores:", self.webcoprocessor.num_cores(), "; avg_core_life (sec):", self.webcoprocessor.avg_core_life 

class QueryEngineHandler(tornado.websocket.WebSocketHandler):
	"""
	TODO: Write what this is
	"""
	
	def allow_draft76(self):
		return True
	
	def initialize(self, query_engine):
		self.query_engine = query_engine
		
	def open(self):
		self.query_engine.add_client( self )
		
	def on_message(self, text):
		
		message = Message.parse_json( text )
		
		print message
		
		try:
		    self.query_engine.process_query( message.query )
		except AttributeError:
		    print "query object is missing 'query' attribute"

	def on_close(self):
		self.query_engine.remove_client( self )

class Message(Object):
	"""Based on anonymous object"""
	
	@staticmethod
	def parse_json( message ):
		return Message( **json_loads(message) )


if __name__ == "__main__":
	
	settings = {
				"static_path": "static",
				"template_path": "html"
	}
	
	# TODO, add persistence via leveldb or tightdb
	query2proc = Queue()
	proc2query = Queue()
	
	webcoprocessor = WebCoProcessor( input_buffer=query2proc, output_buffer=proc2query ) # The web co-processor (WCP)
	queryengine = QueryEngine( input_buffer=proc2query, output_buffer=query2proc ) # query engine executes queries on WCP
	
	application = tornado.web.Application([
		(r"/demo", DemoHandler),
		(r'/webcoprocessor/attach', WebCoProcessorHandler, dict(webcoprocessor=webcoprocessor)),
		(r'/queryengine/attach', QueryEngineHandler, dict(queryengine=queryengine))
	],**settings)

	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()