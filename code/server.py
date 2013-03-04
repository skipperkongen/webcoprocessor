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

Subresult = Object

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
		
	def open(self):
		self.webcoprocessor.add_core( self )
		print "webcore joining. num_cores:", self.webcoprocessor.stats.num_cores
				
	def on_message(self, text):
		"""Received a message from a web core"""
		try:
			print  "Recieved from webcore:", text
			subresult = Subresult.parse_json( text )
			self.webcoprocessor.output_buffer.put( subresult )
		except AttributeError:
			print "query object is missing 'subtask_id' or 'result' attribute"		
			raise	

	def on_close(self):
		self.webcoprocessor.remove_core( self )
		print "webcore leaving. num_cores:", self.webcoprocessor.stats.num_cores, "; avg_core_life (sec):", self.webcoprocessor.stats.avg_core_life 

class QueryEngineHandler(tornado.websocket.WebSocketHandler):
	"""
	TODO: Write what this is
	"""
	
	def allow_draft76(self):
		return True
	
	def initialize(self, queryengine):
		self.queryengine = queryengine

	def on_message(self, query):		
		print query
		try:
			client_websocket = self
			self.queryengine.process_query( 'default', query, client_websocket )
		except AttributeError:
			print "query object is missing 'query' attribute"
			raise

if __name__ == "__main__":
	
	settings = {
				"static_path": "static",
				"template_path": "html"
	}
	
	# TODO, add persistence via leveldb or tightdb
	query2proc = Queue()
	proc2query = Queue()
	
	webcoprocessor = WebCoProcessor( input_buffer=query2proc, output_buffer=proc2query ) # The web co-processor (WCP)
	queryengine = QueryEngine( input_buffer=proc2query, output_buffer=query2proc, wcp_stats=webcoprocessor.stats ) # query engine executes queries on WCP
	
	application = tornado.web.Application([
		(r"/demo", DemoHandler),
		(r'/webcoprocessor/attach', WebCoProcessorHandler, dict(webcoprocessor=webcoprocessor)),
		(r'/queryclients/attach', QueryEngineHandler, dict(queryengine=queryengine))
	],**settings)

	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()