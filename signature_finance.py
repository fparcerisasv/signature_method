



import pandas as pd
import numpy as np
import yfinance as yf
import datetime

def options_chain(symbol):
    '''
    Code modified from https://medium.com/@txlian13/webscrapping-options-data-with-python-and-yfinance-e4deb0124613

    ''' 

    tk = yf.Ticker(symbol)
    
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options_list = []
    for e in exps:
        opt = tk.option_chain(e)
        calls_df = pd.DataFrame(opt.calls)
        puts_df = pd.DataFrame(opt.puts)
        opt_df = pd.concat([calls_df, puts_df], ignore_index=True)
        opt_df['expirationDate'] = e
        options_list.append(opt_df)

    options = pd.concat(options_list, ignore_index=True)

    # Bizarre error in yfinance that gives the wrong expiration date
    # Add 1 day to get the correct expiration date
    options['expirationDate'] = pd.to_datetime(options['expirationDate']) + datetime.timedelta(days=1)
    options['dte'] = (options['expirationDate'] - datetime.datetime.today()).dt.days / 365

    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(lambda x: "C" in x)

    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2  # Calculate the midpoint of the bid-ask

    # Drop unnecessary and meaningless columns
    #options = options.drop(columns=['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])

    return options