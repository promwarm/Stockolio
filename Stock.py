
class Stock():
    """An object representing a single stock"""

    number_of_stocks = 0

    def __init__(self, name, purchase_date, shares=0, price=0):
        self.name = name
        self.purchase_date = purchase_date
        self.shares = shares
        self.price = price
        self.total_cost = 0

        Stock.number_of_stocks += 1

    def add_transaction(self, date, time, shares, price, tx_cost=0):
        self.shares += shares
        self.total_cost += (shares * price) - tx_cost # tx_cost is given as a negative value, so substract it, to add

    def get_total_cost(self):
        return self.total_cost

    def get_shares(self):
        return self.shares

    def get_total_cost_per_share(self):
        return self.total_cost / self.shares