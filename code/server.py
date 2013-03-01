import tornado.ioloop
import tornado.web

class DemoHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("demo.html")

class WebCoProcessor(tornado.web.RequestHandler):
	"""http://backchannel.org/blog/web-sockets-tornado"""
	def get():
		self.write("communication endpoint: not implemented")

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