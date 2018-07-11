import DeGiro
import shelve
from Stock import Stock
from MorningStar_wrapper import Wrapper

def setTickers(ISIN, object):
    # Uses a wrapper to set the tickers
    w = Wrapper(ISIN)
    object.set_ticker(w.getTicker())

def showStocks(list_of_stocks):
    title = 'PORTFOLIO'

    headerItems = ['Name', 'Ticker', '# shares', 'Avg. / share ($)', 'Current ($)', '+/- total ($)', '+/- (%)']
    headerItemsLens = [25, 7, 9, 12, 14, 15, 12]
    totalLength = sum(headerItemsLens)

    # Print header
    print(title.center(totalLength, '-'))

    index = 0
    for headerItem in headerItems:
        print(headerItem.ljust(headerItemsLens[index]), end='')
        index += 1
    print('')
    print(totalLength * "-")

    # Print data (lines)
    show_current_holdings_only = True

    for key, stock in list_of_stocks.items():

        # If we only show current holdings, every holding of which I have 0 shares, is skipped
        if show_current_holdings_only and stock.get_shares() == 0:
            continue

        print(
            key.ljust(headerItemsLens[0]) +  # Name
            stock.ticker.ljust(headerItemsLens[1]) +
            str(stock.get_shares()).rjust(headerItemsLens[2]) +  # Shares
            # '{0:.2f}'.format(stock.get_total_cost()).rjust(headerItemsLens[2]) +  # Cost base
            '{0:.2f}'.format(stock.get_total_cost_per_share()).rjust(headerItemsLens[3]) +  # Cost base, per stock
            '{0:.2f}'.format(stock.get_price()).rjust(headerItemsLens[4])  # Current price
        )

def readTransactions(list_of_txs):
    # print('readTransaction() code executed now')
    for tx in list_of_txs:
        # Instantiate Stock object
        if tx['product'] not in list_of_stocks:
            list_of_stocks[tx['product']] = Stock(tx['product'], tx['date'])

        # When transactions are free, they are returned as empty, instead of 0, we have to fix this
        if tx['transaction_cost'] == '':
            tx['transaction_cost'] = 0

        # Uses a custom MorningStar wrapper to determine ticker, with ISIN input
        if updateTicker:
            setTickers(tx['ISIN'], list_of_stocks[tx['product']])

        list_of_stocks[tx['product']].set_isin(tx['ISIN'])

        # Adding transaction to object
        list_of_stocks[tx['product']].add_transaction(
            tx['date'],
            tx['time'],
            int(tx['shares']),
            float(tx['foreign_price']),
            float(tx['transaction_cost'])
        )

    return list_of_stocks

def saveListOfStocks(list_of_stocks):
    d = shelve.open('../Data/Portfolio')
    d['myStocks'] = list_of_stocks
    d.close()

def readListOfStocks():
    list_of_stocks = []
    #if 'Port'
    d = shelve.open('../Data/Portfolio')
    list_of_stocks = d['myStocks']
    d.close()
    return list_of_stocks

list_of_txs = DeGiro.processTransactionsFile()
list_of_stocks = {}

updateTicker = True
updatePrice = True

# Reading from disk
# list_of_stocks = readListOfStocks()

# If we have to update from disk, execute code below
list_of_stocks = readTransactions(list_of_txs)

for key, value in list_of_stocks.items():
       setTickers(value.isin, value)

showStocks(list_of_stocks)

# Writing to disk
# saveListOfStocks(list_of_stocks)


# NOTES
# Current jobs of create_stocks
#
# 1. setTickers to set ticker of Stock object
# 2. showStocks to view portfolio on screen
# 3. Reads through Stock objects to display the portfolio
# 4. Calls certain Stock class functions to return info
# 5. Reads transactions
# 6. Creates stock objects based on transactions
# 7. Uses Morningstar wrapper to update tickers
# 8. Adds transactions to the Stock object, based on list of tx
# 9. Opens shelve
# 10. Saves shelve
# 11. Handles DeGiro class which returns a list of transactions in a dictionary
# 12. Handles list of stock objects
#
# New situation:
#
# Class Stock
# > Reform getters / setters
#
#
# Class StockFactory
# > Handles list of objects (13)
# > Calculate stuff which applies to all Stocks (averages)
#
# Program HandleShelve
# > Saves list of objects to a shelve (10)
# > Opens list of objects from a shelve (9)
#
