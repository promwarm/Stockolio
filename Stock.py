from StockInfo import StockInfo

class Stock():
    """An object representing a single stock"""

    number_of_stocks = 0

    def __init__(self, name, purchase_date, shares=0, price=0):
        self.name = name
        self.purchase_date = purchase_date
        self.shares = shares
        self.price = price

        # Initiate, but don't set
        self.total_cost = 0
        self.ticker = ''
        self.stockinfo = None
        self.current_price = 0

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

    def set_ticker(self, ticker):
        self.ticker = ticker.upper()

    def get_price(self):
        if self.ticker:
            if self.current_price:
                return self.current_price
            else:
                self.stockinfo = StockInfo(self.ticker)
                self.current_price = self.stockinfo.getPrice()
                return self.current_price
        else:
            return 0.0

    def setCurrentPrice(self, current_price):
        self.current_price = current_price

    def setISIN(self, ISIN):
        self.ISIN = ISIN