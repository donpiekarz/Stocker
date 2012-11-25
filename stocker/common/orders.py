

class Order(object):
    
    def __init__(self, company_id, amount, limit_price, expiration_date):
        self.company_id = company_id
        self.amount = amount
        self.limit_price = limit_price
        self.expiration_date = expiration_date
        self.owner = None
        
    def __eq__(self, other):
        return self.company_id == other.company_id and self.amount == other.amount and self.limit_price == other.limit_price and self.expiration_date == other.expiration_date
        

class OrderBuy(Order):
    
    def __init__(self, company_id, amount, limit_price, expiration_date):
        super(OrderBuy, self).__init__(company_id, amount, limit_price, expiration_date)
        
class OrderSell(Order):
    
    def __init__(self, company_id, amount, limit_price, expiration_date):
        super(OrderSell, self).__init__(company_id, amount, limit_price, expiration_date)
        

