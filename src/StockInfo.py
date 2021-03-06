import requests as req
import logging

logging_enabled = True


class StockInfo:

    """ Returns realtime stock info, provided by IEX trading, for free """

    PREFIX = 'https://api.iextrading.com/1.0'

    def __init__(self, ticker):
        self.ticker = ticker.upper()
        if logging_enabled:
            self.logger = logging.getLogger(f'Stockolio.{__name__}')
            self.logger.debug(f"StockInfo object created for ticker {self.ticker}")

    def getPrice(self):
        # if logging_enabled:
        #     self.logger.debug(f"getPrice() ran for {self.ticker} - quitting right away for now")
        endpoint = f'/stock/{self.ticker}/price'
        url = self.PREFIX + endpoint
#        return 0

        price = 0.0

        r = req.get(url)
        if r.status_code == 200:
            price = float(r.content.decode())
            if logging_enabled:
                self.logger.debug(f"Ticker {self.ticker} - URL {url} - Price {price}")

        return price
