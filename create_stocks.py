import DeGiro
from Stock import Stock

list_of_txs = DeGiro.processTransactionsFile()
list_of_stocks = {}

for tx in list_of_txs:
    # Instantiate Stock object
    if tx['product'] not in list_of_stocks:
        list_of_stocks[tx['product']] = Stock(tx['product'], tx['date'])

    # When transactions are free, they are returned as empty, instead of 0, we have to fix this
    if tx['transaction_cost'] == '':
        tx['transaction_cost'] = 0

    # Adding transaction
    list_of_stocks[tx['product']].add_transaction(
        tx['date'],
        tx['time'],
        int(tx['shares']),
        float(tx['foreign_price']),
        float(tx['transaction_cost'])
    )

# TODO, this part should be in another function or file
# Show data
print(
    'Stock'.ljust(25),
    'Shares'.rjust(6),
    'Cost base'.rjust(7),
    'Cost / share'.rjust(5)
)

show_current_holdings_only = True

for key, stock in list_of_stocks.items():
    if show_current_holdings_only and stock.get_shares() == 0:
        continue

    print(
        key.ljust(25) +                                                              # Name
        str(stock.get_shares()).rjust(6) +                                           # Shares
        '{0:.2f}'.format(stock.get_total_cost()).rjust(10) +                         # Cost base
        '{0:.2f}'.format(stock.get_total_cost_per_share()).rjust(10)                 # Cost base, per stock
         )