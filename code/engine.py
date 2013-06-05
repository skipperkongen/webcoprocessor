from datetime import datetime
from threading import Thread, Lock
import pdb
from random import choice
from hashlib import sha1
#pdb.set_trace()


from util import Object

lock = Lock()
no_result = object()

class WebCoProcessor(object):
	"""NEEDS WORK!!"""
	def __init__(self, io_buffer):
		super(WebCoProcessor, self).__init__()
		self.cores = set()
		self.io_buffer = io_buffer
		# for statistics
		self.stats = Object(avg_core_life=None, num_cores=0)
		self.alpha = 0.1
		self.queryengine = None
	
	def add_core(self, core):
		self.cores.add( core )
		self.stats.num_cores += 1

	def remove_core(self, core):
		
		# updated weighted average of core life span
		if self.stats.avg_core_life:
			self.stats.avg_core_life = (1.0 - self.alpha) * self.stats.avg_core_life + self.alpha * (datetime.now() - core.connect_time).total_seconds()
		else:
			self.stats.avg_core_life = (datetime.now() - core.connect_time).total_seconds()
		self.stats.num_cores -= 1
		self.cores.remove( core )
	
	def schedule_subtask(self, subtask):
		# select random core... hmmm, how to get both fast random choice and fast add/remove?
		core = choice( list(self.cores) ) # looks a bit expensive?
		core.write_message( unicode(subtask) )
	
	def num_cores(self):
		return len( self.cores )
				
class QueryEngine(object):
	"""NEEDS WORK!!"""
	def __init__(self, webcoprocessor):
		super(QueryEngine, self).__init__()
		self.webcoprocessor = webcoprocessor
		self.queries = {}
		self._next_query_id = 0
			
	def register_query(self, query):
		with lock:
			self._next_query_id += 1
			self.queries[ self._next_query_id ] = query
			return self._next_query_id
		
	def process_query( self, dsl, query_text, client_websocket ):

		# Dummy implementation
		try:
			query = self.create_query( query_text, client_websocket )
			query_id = self.register_query( query )
			for subtask in query.subtasks.values():
				self.webcoprocessor.schedule_subtask( 
					Object( query_id=query_id, subtask_id=subtask.id, javascript=subtask.javascript )
				)
		except:
			raise
	
	def process_subresult( self, res ):
		query = self.queries[ res.query_id ]
		query.update( res.subtask_id, res.result )
		if query.is_complete():
			query.client_websocket.write_message( unicode(query.result()) )
			del self.queries[ res.query_id ]

	def create_query( self, query_text, client_websocket ):
		def chunks(l, n):
		    """ Yield successive n-sized chunks from l. """
		    for i in xrange(0, len(l), n):
		        yield l[i:i+n]

		operator = [s for s in query_text.split() if s.isalpha()][0] # get first word
		numbers = [s for s in query_text.split() if s.isdigit()] # get numbers
		if operator == 'max':
			num_tasks = int(len(numbers) / float( self.webcoprocessor.stats.num_cores ))
			chunk_size = int(len(numbers) / float(num_tasks))
			task_texts = ['Math.max(%s);' % ",".join(chunk) for chunk in chunks(numbers, chunk_size)]
			subtasks = [Subtask(task_text) for task_text in task_texts]
			return Query(subtasks, client_websocket, eval(operator))
		else:
			raise ValueError("Unknown query") 
	


class Query(object):
	"""docstring for Query"""
	def __init__(self, subtasks, client_websocket, result_combiner):
		super(Query, self).__init__()
		self.subtasks = dict([(subtask.id, subtask) for subtask in subtasks])
		self.client_websocket = client_websocket
		self._result_combiner = result_combiner
	
	def update(self, subtask_id, subresult):
		#pdb.set_trace()
		self.subtasks[subtask_id].subresult = subresult
		
	def is_complete(self):
		return no_result not in [subtask.subresult for subtask in self.subtasks.values()]
	
	def result(self):
		if self.is_complete():
			return self._result_combiner([subtask.subresult for subtask in self.subtasks.values()])
		else:
			raise ValueError('Badness!')
		
class Subtask(object):
	"""docstring for Subtask"""
	def __init__(self, javascript):
		super(Subtask, self).__init__()
		self.javascript = javascript
		h = sha1()
		h.update( javascript )
		self.id = h.hexdigest()
		self.subresult = no_result		
		
		
		
		