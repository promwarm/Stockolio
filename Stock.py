
class Stock():

    """An object representing a stock"""

    number_of_stocks = 0
    all_stocks = []

    def __init__(self, name, purchase_date, shares=0, price=0):
        self.name = name
        self.purchase_date = purchase_date
        self.shares = shares
        self.price = price

        Stock.number_of_stocks += 1
        Stock.all_stocks.append(name)

    def find_stock_by_name(self, name):
        #How do I return the instance with the given name?
        return self
