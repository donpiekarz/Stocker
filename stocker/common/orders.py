class Order(object):
    def __init__(self, company_id, amount, limit_price, expiration_date):
        self.company_id = company_id
        self.amount = amount
        self.limit_price = limit_price
        self.expiration_date = expiration_date
        self.investor = None
        self.stockbroker = None

    def __eq__(self, other):
        return self.company_id == other.company_id and self.amount == other.amount and self.limit_price == other.limit_price and self.expiration_date == other.expiration_date

    def __repr__(self):
        return "%s: Company: %s, amount: %d,  limit price: %.2f, expiration date: %s" %\
               (
                   self.__class__,
                   self.company_id,
                   self.amount,
                   self.limit_price,
                   self.expiration_date
                   )

    def __getstate__(self):
        odict = self.__dict__.copy()
        # prevent serializing investor and stockbroker
        del odict['investor']
        del odict['stockbroker']
        return odict


class OrderBuy(Order):
    def __init__(self, company_id, amount, limit_price, expiration_date):
        super(OrderBuy, self).__init__(company_id, amount, limit_price, expiration_date)


class OrderSell(Order):
    def __init__(self, company_id, amount, limit_price, expiration_date):
        super(OrderSell, self).__init__(company_id, amount, limit_price, expiration_date)
        

