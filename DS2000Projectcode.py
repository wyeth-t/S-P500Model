'''
DS2000 Final Project
Varun Jauhar and Wyeth Thompson
All functions regarding data processing and manipulation to form comparisons in graphs
'''

import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import stats


def sp_yearly_returns(data):
    '''
    sp_yearly_returns uses daily s&p500 open and close information to calculate year
gain information for the s&p500 index
    Parameters: data(dataframe of daily s&p information since 1970)
    Returns: df(dataframe of yearly s&p percentage gains)
'''
    year = '1970'
    years = []
    yearly_return = []
    date = 0
    
    while date < 49:
        
        df = data.filter(like= year, axis=0)
        annual= (((df.iloc[-1]['Close']) - (df.iloc[0]['Open'])) /(df.iloc[0]['Open']))
        years.append(year)
        yearly_return.append(annual)
        year = int(year) + 1
        year = str(year)
        date = date +1
        
    dictionary = {'Year': years, 'Yearly Return': yearly_return}
    df = pd.DataFrame(dictionary)
    df = df.set_index('Year') 
    return(df)


def portfolio_yearly_returns(data):
    '''
    porfolio_yearly_returns takes a dataframe of buy/sell decisions and results for thousands
of companies and agregates returns into years to see the effectiveness of a given portfolio strategy
    Parameters: data(dataframe of buy/sell stock decisions)
    Returns: df(dataframe of yearly portfolio returns)
'''
    year = "1970"
    years = []
    yearly_returns = []
    date = 0
    
    while date < 49:
        
        df = data.filter(like= year, axis=0)
        yearly_return = (df['Investment Dollar Gain'].sum()) / (df['Investment Amount'].sum())
        years.append(year)
        yearly_returns.append(yearly_return)
        year = int(year) + 1
        year = str(year)
        date = date +1
        
    dictionary = {'Year': years, 'Yearly Return': yearly_returns}
    df = pd.DataFrame(dictionary)
    df = df.set_index('Year') 
    return(df)


def remove_outliers(df):
    '''
    Remove_Outliers takes a dataframe and removes the rows that contain outliers
in the percent return column. The purpose of this function is to correct for dataset errors
    Parameters:  dataframe (df) containing a percent return column
    Return: dataframe (df) corrected for outliers
'''
    z_scores = stats.zscore(df['Investment Percent Return'])
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3)
    new_df = df[filtered_entries]
    return new_df
    
    

def line_plot(sp, portfolio):
    '''
line_plot takes yearly gain information from a portfolio and the s&p and plots them
    on a line chart.
    Parameters: sp(dataframe of yearly s&p returns), portfolio(dataframe of yearly portfolio returns)
    Returns: nothing

'''
    
    sp['Yearly Return'] = sp['Yearly Return']*100
    portfolio['Yearly Return'] = portfolio['Yearly Return']*100
    sp_returns = sp['Yearly Return'].to_list()
    p_returns = portfolio['Yearly Return'].to_list()
    plt.plot(sp, label= "S&P500 Returns")
    plt.plot(portfolio, label= "Buy Low Sell High Returns")
    plt.legend(loc="upper right")
    plt.xlabel('Years')
    plt.ylabel('Yearly Returns')
    plt.title('S&P500 vs Buy Low Sell High Strategy')
    plt.show()
    
def main():
 
#Process daily S&P 500 returns to yearly returns to be used for graphing
    benchmark = pd.read_csv("^GSPC.csv", index_col = "Date")
    sp_yearly_returns(benchmark).to_csv("SP_Yearly_returns.csv")
    

#buy low strategy, process of removing outliers and aggregating to yearly returns
    #buylow_returns = pd.read_csv("BuyLowReturns.csv", index_col = "Sell Date")
    #remove_outliers(buylow_returns).to_csv("BuyLowReturns_NoOutliers.csv")
    #buyLowReturns_NoOutliers = pd.read_csv("BuyLowReturns_NoOutliers.csv", index_col = "Sell Date")
    #buylow_yearly_returns = portfolio_yearly_returns(buyLowReturns_NoOutliers)
    #buylow_yearly_returns.to_csv("BuyLow_Yearly_Returns1.csv")
    

#momentum strategy,process of removing outliers and aggregating to yearly returns
    momentum_returns = pd.read_csv("CompanyReturns.csv", index_col = "Sell Date")
    print(remove_outliers(momentum_returns))
    #MomentumReturns_NoOutliers = pd.read_csv("MomentumReturns_NoOutliers.csv", index_col = "Sell Date")
    #Momentum_Yearly_Returns = portfolio_yearly_returns(MomentumReturns_NoOutliers)
#Momentum_Yearly_Returns.to_csv("Momentum_Yearly_Returns1.csv")

#Yearly Returns read from csv files and used for graphing
    #SP_Yearly_Returns = pd.read_csv('SP_Yearly_Returns.csv', index_col = "Year")
    #Momentum_Yearly_Returns = pd.read_csv('Momentum_Yearly_Returns1.csv', index_col = "Year")
    #BuyLow_Yearly_Returns = pd.read_csv('BuyLow_Yearly_Returns1.csv', index_col = "Year")

#Plot of the Momentum strategy compared to the S&P500 returns
    #line_plot(SP_Yearly_Returns, Momentum_Yearly_Returns)
    
#Plot of the Buy Low Sell High strategy compared to the S&P500 returns
    #line_plot(SP_Yearly_Returns, BuyLow_Yearly_Returns)
    
#Plot of our two strategies compared to one another
    #line_plot(BuyLow_Yearly_Returns, Momentum_Yearly_Returns)
    
    
    
    
    
    
main()
