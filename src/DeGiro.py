def processTransactionsFile():
    """
    Processes the transactions.csv file you could download from your DeGiro account.
    Returns a list of dictionaries with the individual transactions
    """

    number_of_tx_lines = 0
    list_of_txs = []

    with open('../Data/Transactions.csv') as tx:
        tx_lines = tx.readlines()

    for tx_line in tx_lines:
        number_of_tx_lines += 1
        if number_of_tx_lines != 1: # Skip header
            list_of_txs.append(processTransaction(tx_line.rstrip()))

    return list_of_txs

def processTransaction(tx_line):
    """
    Processes 1 line of Transaction.csv.
    It should contain these column:
    Date, time, Product, ISIN
    Exchange, number of shares, foreign currency, foreign price

    TODO: Update correct info
    Foreign currency, total value in foreign curency, exchange rate, transaction costs, total
    """

    # Put data in colums, each element in the list has a number to refer to
    tx_colums = []
    tx_colums = tx_line.split(',')

    # Because numbers are not so clear, we make a dictionary
    tx_data = {}

    tx_data['date'] = tx_colums[0]
    tx_data['time'] = tx_colums[1]
    tx_data['product'] = tx_colums[2]
    tx_data['ISIN'] = tx_colums[3]
    tx_data['exchange'] = tx_colums[4]
    tx_data['shares'] = tx_colums[5]
    tx_data['foreign_currency_1'] = tx_colums[6]
    tx_data['foreign_price'] = tx_colums[7]
    tx_data['foreign_currency_2'] = tx_colums[8]
    tx_data['total_amount_foreign_currency'] = tx_colums[9]
    tx_data['local_currency_1'] = tx_colums[10]
    tx_data['local_value'] = tx_colums[11]
    tx_data['exchange_rate'] = tx_colums[12]
    tx_data['local_currency_2'] = tx_colums[13]
    tx_data['transaction_cost'] = tx_colums[14]
    tx_data['total_amount_local_currency'] = tx_colums[15]

    return tx_data