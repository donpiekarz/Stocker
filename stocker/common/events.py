

class Event(object):
	pass

class EventStream(Event):
	"""Event in Stream"""
	
	def __init__(self, timestamp, order):
		self.timestamp = timestamp
		self.order = order
		
	def __lt__(self, other):
		return self.order < other.order
		
class EventStreamNew(EventStream):
	pass
		
class EventStreamDel(EventStream):
	pass
		
class EventStock(Event):
	"""Event in Stock"""
	
	def __init__(self, timestamp, order):
		self.timestamp = timestamp
		self.order = order

class EventStockOrderNew(EventStock):
	pass

class EventStockOrderDel(EventStock):
	pass
		
class EventStockTransaction(EventStock):
	pass



