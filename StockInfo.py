import requests as req

class StockInfo():

    """ Returns realtime stock info, provided by IEX trading, for free """

    PREFIX = 'https://api.iextrading.com/1.0'

    def __init__(self, ticker):
        self.ticker = ticker.upper()

    def getPrice(self):
        endpoint = f'/stock/{self.ticker}/price'
        url = self.PREFIX + endpoint

        price = 0.0

        r = req.get(url)
        if r.status_code == 200:
            price = float(r.content.decode())

        return price