

class Stock(object):
    
    def __init__(self, stream):
        self.stream = stream
        self.investors = []
        
    def add_investor(self, investor):
        self.investors.append(investor)
    
    def simulate(self):
        print "simulate"
    