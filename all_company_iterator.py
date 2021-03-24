'''
DS2000 Final Project
Varun Jauhar and Wyeth Thompson
Functions to iterate through all company data and perform portfolio management functions
'''

import pandas as pd
import csv

def open_symbols():
    '''
    open_symbols takes the txt file of company stock tickers and converts it into
a list
    Parameters: none
    Returns: clean_list(list) 
'''
    with open("all_symbols.txt", "r") as infile:
        lines = infile.readlines()
        clean_list = []
        for line in lines:
            clean_line = line.strip()
            clean_line = clean_line.replace("\\","")
            clean_list.append(clean_line)
    return clean_list

def csv_reader(data):
    '''
    csv_reader processes a dataframe of stock information to only include information
we need as well as adding a daily gain column in order to be iterated over
    Parameters: data(dataframe of stock information)
    Returns: data(dataframe of stock information)
'''

    data = data.drop(['high', 'low', 'volume', 'adjclose'], axis=1)
    data['gain'] = ((data['close']- data['open']) / data['open']) * 100
    data = data.iloc[::-1]
    return(data)

def all_company_data(data, ticker, buy, sell):
    '''
    all_company_data iterates through a dataframe of edited stock information
of a particular company and makes buy or sell decisions based on the parameters given.
    Parameters: data(dataframe), ticker(string), buy(int), sell(int)
    Returns: df(dataframe of investment information including investment amounts,
gain on sale, sell date, and percent return)
'''
            
    buydate = []
    selldate = []
    purchase = []
    gains = []
    dolgains = []
    investmentamount = []
    investmentdolgains = []
    investmentpercentreturn = []
    
    for i in range((len(data)-2)):
        
        if data.iloc[i]['gain'] <= buy and data.iloc[i + 1]['gain'] <= buy:
            purchase.append(data.iloc[i+2]['open'])
            buydate.append(data.index[i+2])
            
        elif data.iloc[i]['gain'] >= sell and len(purchase) > 0:
            sale = data.iloc[i+1]['open']
            for a in purchase:
                gains.append((sale-a)/a)
            
            for gain in gains:
                dolgains.append(gain * 10)
        
            investmentamount.append(len(purchase)*10)
            investmentdolgains.append(sum(dolgains))
            investmentpercentreturn.append((sum(dolgains)/(10 * len(dolgains))*100))
            selldate.append(data.index[i+1])
            
            gains = []
            dolgains = []
            purchase = []
            buydate = []
    dictionary = {'Ticker': ticker, 'Sell Date': selldate, 'Investment Percent Return': investmentpercentreturn,
                  'Investment Dollar Gain': investmentdolgains, "Investment Amount": investmentamount}
    df = pd.DataFrame(dictionary)
    df = df.set_index('Sell Date')
    return(df)


def main():
    clean_list = open_symbols()
    
#create empty master dataframes to include all by/sell information for each strategy
    momentum = pd.DataFrame(columns=['Ticker', 'Sell Date', 'Investment Percent Return',
                                  'Investment Dollar Gain', 'Investment Amount'])
    buy_low = pd.DataFrame(columns=['Ticker', 'Sell Date', 'Investment Percent Return',
                                  'Investment Dollar Gain', 'Investment Amount'])
    momentum = momentum.set_index('Sell Date')
    buy_low = buy_low.set_index('Sell Date')
    
#iterates through list of tickers and accesses each company's csv file for all_company_data
    path = "/Users/wyeththompson/Desktop/projectfolder/full_history"
    for i in clean_list:
        filename = path + "/" + i + ".csv"
        data = pd.read_csv(filename, index_col = "date")
        if data.shape[0] >= 3:
            print(i)
            #momentum = momentum.append(all_company_data(csv_reader(data), i, 2, -2))
            buy_low = buy_low.append(all_company_data(csv_reader(data), i, -2, 2))
            
#saves dataframes containing all purchase decisions to csv files
    #momentum.to_csv('CompanyReturns.csv')
    buy_low.to_csv('BuyLowReturns.csv')
main()
