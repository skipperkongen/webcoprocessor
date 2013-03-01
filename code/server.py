import tornado.ioloop
import tornado.web
import tornado.websocket
from json import loads as json_loads
from json import dumps as json_dumps

class DemoHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("demo.html")

class WebCoProcessor(tornado.websocket.WebSocketHandler):
	"""
	- http://backchannel.org/blog/web-sockets-tornado (github repo down):
	- http://www.tornadoweb.org/documentation/websocket.html (this is the one to use)
	
	The Web Sockets API enables web browsers to maintain a bi-directional 
	communication channel to a server, which in turn makes implementing 
	real-time web sites about 1000% easier than it is today.
	"""
	def open(self):
		print "WebSocket opened"

	def on_message(self, message):
		"""Valid message is JSON with following structure:
			{
				"node_id":"who sent this message?",
				"type":"is it a query or a result?",
				"data":"stuff... whatever..",
				"for": "who is the result for (if it is a result)" 
			}
		"""
		print "MESSAGE:", message		
		
		resp = WCPMessage() # initialize empty response
		try:
			req = WCPMessage.from_text(message)

			if req.message_type == 'register':
				print "node has registered (but which)"
				resp.sender = 'master'
				resp.message_type = 'result'
				resp.data = '[registration accepted]'
				
			elif req.message_type == 'query':		
				resp.sender = 'master'
				resp.message_type = 'result'
				resp.data = '[echo] %s' % req.data

			elif req.message_type == 'result':
				raise NotImplementedError()

			else:
				raise NotImplementedError()

		except Exception, NotImplementedError:
			raise
			resp.type = 'error'
			resp.data = 'badness 9000'

		self.write_message( json_dumps(resp.__dict__)  )

	def on_close(self):
		print "WebSocket opened"
		print "node has left (but which?)"

class WCPMessage(object):
	"""docstring for Message"""
	def __init__(self, message_type=None, data=None, sender=None, pool=None):
		super(WCPMessage, self).__init__()
		self.message_type = message_type
		self.data = data
		self.sender = sender
		self.pool = pool
	
	@staticmethod
	def from_text( message ):
		jsondata = json_loads(message)
		return WCPMessage(
			message_type = jsondata['message_type'],
			data = jsondata['data'],
			sender = jsondata['sender'],
			pool = jsondata['pool'] if 'pool' in jsondata else None
		)
		

if __name__ == "__main__":
	
	settings = {
				"static_path": "static",
				"template_path": "html"
	}
	
	application = tornado.web.Application([
		(r"/demo", DemoHandler),
		(r'/web_coproc', WebCoProcessor)
	],**settings)

	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()