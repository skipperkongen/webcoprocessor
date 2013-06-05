from hashlib import sha1
from json import loads as json_loads
from json import dumps as json_dumps

class Object(object):
	"""Based on anonymous object"""
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)
	
	def __str__(self):
		return unicode(json_dumps(self.__dict__))
	
	def __repr__(self):
		return self.__str__()
		
	@staticmethod
	def parse_json( message ):
		return Object( **json_loads(message) )

		
			
