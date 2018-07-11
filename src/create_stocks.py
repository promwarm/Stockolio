import DeGiro
from Stock import Stock
from MorningStar_wrapper import Wrapper
import logging
from colorama import Fore


def setTickers(ISIN, object):
    #logger.debug(f"setTickers() - ISIN: {ISIN} - object {object}")
    # Uses a wrapper to set the tickers
    if object.ticker == '':
        logger.debug(f"setTickers() - Creating Wrapper object for ISIN: {ISIN} - ticker: {object.ticker}")
        w = Wrapper(ISIN)
        ticker = w.getTicker()
        #logger.debug(f"setTickers() - ISIN: {ISIN} - ticker: {ticker}")
        object.set_ticker(ticker)


def showStocks(list_of_stocks):
    logger.debug(f"showStocks() for {len(list_of_stocks)} stocks")
    title = 'PORTFOLIO'

    headerItems = ['Name', 'Ticker', '# shares', 'Avg. / share ($)', 'Current ($)', '+/- total ($)', '+/- (%)']
    headerItemsLens = [25, 7, 9, 12, 14, 15, 12]
    totalLength = sum(headerItemsLens)
    colour_reset = Fore.WHITE

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
        logger.debug(f"showStocks() - key: {key}")

        # If we only show current holdings, every holding of which I have 0 shares, is skipped
        if show_current_holdings_only and stock.get_shares() == 0:
            continue

        if stock.get_total_cost_per_share() < stock.get_price():
            colour = Fore.GREEN
        else:
            colour = Fore.RED

        print(
            key.ljust(headerItemsLens[0]) +  # Name
            stock.ticker.ljust(headerItemsLens[1]) +
            str(stock.get_shares()).rjust(headerItemsLens[2]) +  # Shares
            # '{0:.2f}'.format(stock.get_total_cost()).rjust(headerItemsLens[2]) +  # Cost base
            '{0:.2f}'.format(stock.get_total_cost_per_share()).rjust(headerItemsLens[3]) +  # Cost base, per stock
            colour + '{0:.2f}'.format(stock.get_price()).rjust(headerItemsLens[4]) + colour_reset # Current price
        )


def readTransactions(list_of_txs, updateTicker, updatePrice):
    logger.debug(f"readTransactions() - total transactions: {len(list_of_txs)}")
    list_of_stocks = {}
    for tx in list_of_txs:
        # Instantiate Stock object
        if tx['product'] not in list_of_stocks:
            list_of_stocks[tx['product']] = Stock(tx['product'], tx['date'])

        # When transactions are free, they are returned as empty, instead of 0, we have to fix this
        if tx['transaction_cost'] == '':
            tx['transaction_cost'] = 0

        # Uses a custom MorningStar wrapper to determine ticker, with ISIN input
        if updateTicker and list_of_stocks[tx['product']].ticker == '':
            setTickers(tx['ISIN'], list_of_stocks[tx['product']])

        if updatePrice:
            list_of_stocks[tx['product']].set_update_price(updatePrice)

        if list_of_stocks[tx['product']].isin == '':
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


def config_logger():
    from os import path, remove
    import logging

    # If applicable, delete the existing log file to generate a fresh log file during each execution
    if path.isfile("../logs/python_logging.log"):
        remove("../logs/python_logging.log")

    # Create the Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create the Handler for logging data to a file
    logger_handler = logging.FileHandler('../logs/python_logging.log')
    logger_handler.setLevel(logging.DEBUG)

    # Create a Formatter for formatting the log messages
    logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # Add the Formatter to the Handler
    logger_handler.setFormatter(logger_formatter)

    # Add the Handler to the Logger
    logger.addHandler(logger_handler)
    logger.info('Completed configuring logger()!!')
    return logger


def main():
    logger.debug("Creating a list_of_txs")
    list_of_txs = DeGiro.processTransactionsFile()

    updateTicker = True
    updatePrice = False

    # If we have to update from disk, execute code below
    logger.debug("Creating a list_of_stocks")
    list_of_stocks = readTransactions(list_of_txs, updateTicker, updatePrice)
    print(Stock.instances_started)
    #pprint(list_of_stocks)

    for key, value in list_of_stocks.items():
         setTickers(value.isin, value)

    showStocks(list_of_stocks)

    log_to_debug = logging.getLogger(__name__)
    while log_to_debug is not None:
        print(f"level: {log_to_debug.level}, name: {log_to_debug.name}, handlers: {log_to_debug.handlers}")
        log_to_debug = log_to_debug.parent


if __name__ == '__main__':
    logger = config_logger()
    main()
