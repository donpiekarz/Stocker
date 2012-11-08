

class Event:
	pass

class EventStream(Event):
	"""Event in Stream"""
	
	def __init__(self, action, order):
		self.action = action
		self.order = order
		
class EventStock(Event):
	"""Event in Stock"""
	
	pass
		
