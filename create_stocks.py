import DeGiro
from Stock import Stock

list_of_txs = DeGiro.processTransactionsFile()
list_of_stocks = []

for tx in list_of_txs:
    if tx['product'] not in Stock.all_stocks:
        s = Stock(tx['product'], tx['date'])
        list_of_stocks.append(s)

print(s.number_of_stocks)
