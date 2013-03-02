import tornado.ioloop
import tornado.web
import tornado.websocket
import pdb
from json import loads as json_loads
from json import dumps as json_dumps
from util import Object
from Queue import Queue

from threading import Lock

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
	def initialize(self, webcoprocessor):
		self.webcoprocessor
		self.engine = None

	next_webcore_id = 1
	
	def write_message_json(self, obj):
		self.write_message json_dumps(obj.__dict__)
	
	def open(self):
		# pdb.set_trace() # let's see what info we have
		print "webcore joining"
		self.webcoprocessor.add_core(self)
		
	def on_message(self, message):
		"""Received a message from a web core"""
		msg_from_core = WCPMessage.parse_message(message)
		
		print msg_from_core.message_type, msg_from_core.data

		if msg_from_core.message_type == 'init':
			# web core wanna to tell us something about its flops
			self.engine = msg_from_core.data['engine']

		if msg_from_core.message_type == 'result':
			# web core has computed a JSON result
			self.webcoprocessor.output_buffer.put( msg_from_core.data )

		# no need to answer web cores back, but this is how you'd do it:
		# - self.write_message( json_dumps(obj.__dict__)  )

	def on_close(self):
		print "webcore leaving"
		self.webcoprocessor.remove_core(self)

class WCPMessage(Object):
	"""Based on anonymous object"""
	
	@staticmethod
	def parse_message( message ):
		return WCPMessage( **json_loads(message) )

class WebCoProcessor(object):
	"""docstring for WebCoProcessor"""
	def __init__(self, input_buffer, output_buffer):
		super(WebCoProcessor, self).__init__()
		self.cores = dict()
		self.input_buffer = input_buffer
		self.output_buffer = output_buffer
	
	def add_core(self, core):
		self.cores.add( core )	

	def remove_core(self, websocket):
		self.cores.remove( Core(websocket) )
	
	def start(self):
		"""in thread: while 1: get job from input_buffer, partition and send to cores"""
		pass
		
if __name__ == "__main__":
	
	settings = {
				"static_path": "static",
				"template_path": "html"
	}
	
	# TODO, add persistence via leveldb or tightdb
	webcoprocessor = WebCoProcessor( input_buffer=Queue(), outout_buffer=Queue() ) # The web co-processor (WCP)
	queryengine = WCPQueryEngine( webcoprocessor ) # query engine executes queries on WCP
	
	application = tornado.web.Application([
		(r"/demo", DemoHandler),
		(r'/webcoprocessor/attach', WebCoProcessorHandler, dict(webcoprocessor=webcoprocessor))
		(r'/queryengine', QueryEngineHandler, queryengine=queryengine)
	],**settings)

	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()