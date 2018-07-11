from StockInfo import StockInfo
import logging

logging_enabled = True


class Stock:
    """An object representing a single stock"""

    instances_started = 0

    def __init__(self, name, purchase_date, shares=0, price=0):
        self.name = name
        self.purchase_date = purchase_date
        self.shares = shares
        self.price = price

        # Initiate, but don't set
        self.stockinfo = None
        self.total_cost = 0
        self.ticker = ''
        self.current_price = 0
        self.isin = ''
        self.update_price = False

        if logging_enabled:
            self.logger = logging.getLogger(__name__)
            self.logger.debug(f"Stock object {name} created {purchase_date}, {shares}, {price}")

        Stock.instances_started += 1


    def add_transaction(self, date, time, shares, price, tx_cost=0):
        self.shares += shares
        self.total_cost += (shares * price) - tx_cost  # tx_cost is given as a negative value, so subtract it, to add

    def get_total_cost(self):
        return self.total_cost

    def get_shares(self):
        return self.shares

    def get_total_cost_per_share(self):
        return self.total_cost / self.shares

    def set_ticker(self, ticker):
        self.ticker = ticker.upper()
        self.stockinfo = StockInfo(self.ticker)

    def get_price(self):
        if self.ticker:
            if self.current_price and not self.update_price:
                return self.current_price
            else:
                self.current_price = self.stockinfo.getPrice()
                return self.current_price
        else:
            return 0.0

    def set_price(self, current_price):
        self.current_price = current_price

    def set_isin(self, isin):
        self.isin = isin

    def set_update_price(self, update_price):
        if logging_enabled:
            self.logger.debug(f"set_update_price {update_price} for {self.ticker}")
        self.update_price = update_price

    def json(self):
        dict_stock = {
            "name": {self.name},
            "ticker": {self.ticker},
            "purchase date": {self.purchase_date},
            "shares": {self.shares},
            "average purchase price": {self.price},
            "total cost": {self.total_cost},
            "current price": {self.current_price},
            "ISIN": {self.isin}
        }
        return dict_stock

    def __repr__(self):
        return f'Stock({self.name}, {self.purchase_date}, {self.shares}, {self.price})'

    def __str__(self):
        return f'Stock({self.name} ({self.ticker}), {self.shares}, {self.price})'
