#pip install beautifulsoup4
#pip install XlsxWriter
#pip install selenium
#pip install phantomjs
#pip install matplotlib
#pip install mpl_finance
#pip install pandas
#pip install pandas-datareader
#pip install yfinance
#pip install fix_yahoo_finance

import bs4 as bs
import datetime as dt
import os
import pandas as pd
from pandas_datareader import data as pdr
import pickle
import requests
import fix_yahoo_finance as yf


def save_sp500_tickers():
    """
    This function will scrape the S&P 500 companies from the wikipedia API
    and will save this list into an array name tickers
    :return: An array of strings with the ticker symbols of all the S&P 500 tickers
    """

    # Access the S&P 500 list from the wiki webpage
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    # Find the S&P 500 table using beautiful soup
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    # Variable that will store the S&P 500 list
    tickers = []

    # Go through the S&P 500 table and append each ticker to the tickers array
    for row in table.findAll('tr')[1:]:
        # If the ticker has a '.' or '-' then remove them
        ticker = row.findAll('td')[0].text.replace('.', '-')
        ticker = ticker[:-1]
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    # Return the S&P 500 list
    print(tickers)
    return tickers


def get_data_from_yahoo(reload_sp500=False):
    """
    This function will use the pandas_datareader to access the Yahoo Finance API to get the
    open, high, low, close data for each S&P 500 stock and save the data into a csv file and
    store it into the stock_dfs directory
    :param reload_sp500:
    :return: The data of each S&P 500 saved into a csv file and stored in the stock_dfs directory
    """

    # load the S&P 500 company tickers into a variable
    if reload_sp500:
        tickers = save_sp500_tickers()

    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    # make the stock_dfs directory if it does not currently exist
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    # I will be searching for data from 2019 until present
    start = dt.datetime(2019, 6, 8)
    end = dt.datetime.now()

    # Iterate through the stock tickers
    for ticker in tickers:
        print(ticker)
        # Create a file with the tickers name in the stock_dfs directory if it doesn't exist
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            # Get the data from yahoo finance from the current ticker from 2019 till now
            df = pdr.get_data_yahoo(ticker, start, end)
            # Set the Date as the index
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            # Save the dataframe into a csv file
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            # if the file already exists message the user that the file is created already
            print('Already have {}'.format(ticker))

# Run both functions
save_sp500_tickers()
get_data_from_yahoo()