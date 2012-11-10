

class Event(object):
	pass

class EventStream(Event):
	"""Event in Stream"""
	
	def __init__(self, order):
		self.order = order
		
class EventStreamNew(EventStream):
	
	def __init__(self, order):
		super(EventStreamNew, self).__init__(order)
		
class EventStreamDel(EventStream):
	
	def __init__(self, order):
		super(EventStreamDel, self).__init__(order)
		
class EventStock(Event):
	"""Event in Stock"""
	
	pass
		