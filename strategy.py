import pandas as pd 
import matplotlib.pyplot as plt 
import requests
import math
from termcolor import colored as cl 
import numpy as np
import csv

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

file = open("stockData.csv")


def get_historic_data():
    type(file)
    csvreader = csv.reader(file)

    header = []
    header = next(csvreader)

    df = []
    for row in csvreader:
        record = {
            "date" : "",
            "open" : 0,
            "high" : 0,
            "low" : 0,
            "close" : 0
        }
        record["date"] = row[0]
        record["open"] = float(row[1])
        record["high"] = float(row[2])
        record["low"] = float(row[3])
        record["close"] = float(row[4])
        df.append(record)

    file.close ()

    date = []
    open = []
    high = []
    low = []
    close = []
    
    for i in range(len(df)):
        date.append(df[i]['date'])
        open.append(df[i]['open'])
        high.append(df[i]['high'])
        low.append(df[i]['low'])
        close.append(df[i]['close'])
    
    date_df = pd.DataFrame(date).rename(columns = {0:'date'})
    open_df = pd.DataFrame(open).rename(columns = {0:'open'})
    high_df = pd.DataFrame(high).rename(columns = {0:'high'})
    low_df = pd.DataFrame(low).rename(columns = {0:'low'})
    close_df = pd.DataFrame(close).rename(columns = {0:'close'})
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis = 1, join = 'inner')
    return df


nft = get_historic_data()
nft = nft.set_index('date')
nft.index = pd.to_datetime(nft.index)

print(nft.index)

def sma(data, window):
    sma = data.rolling(window = window).mean()
    return sma

nft['sam_1'] = sma(nft['close'], 1)



print (nft)
def bb(data, sma, window):
    std = data.rolling(window = window).std()
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    print("---------------")
    print(std, upper_bb, lower_bb)
    return upper_bb, lower_bb

nft['upper_bb'], nft['lower_bb'] = bb(nft['close'], nft['sam_1'], 1)
nft.tail()
print (nft)



nft['close'].plot(label = 'CLOSE PRICES', color = 'skyblue')
nft['upper_bb'].plot(label = 'UPPER BB 20', linestyle = '--', linewidth = 1, color = 'black')
nft['sam_1'].plot(label = 'MIDDLE BB 20', linestyle = '--', linewidth = 1.2, color = 'grey')
nft['lower_bb'].plot(label = 'LOWER BB 20', linestyle = '--', linewidth = 1, color = 'black')
plt.legend(loc = 'upper left')
plt.title('nft BOLLINGER BANDS')
plt.show()