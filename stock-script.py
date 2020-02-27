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



#this function will scrape the s&p 500 companies
#from wikipedia and will save it into an array 
#called tickers
def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    
    tickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('.', '-')
        ticker = ticker[:-1]
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

#This function will take all the data from the s&p500 using
#the yahoo finance api and will store the data into an excel 
#file in the folder stock_dfs
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()

    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2019, 6, 8)
    end = dt.datetime.now()

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = pdr.get_data_yahoo(ticker, start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

save_sp500_tickers()
get_data_from_yahoo()