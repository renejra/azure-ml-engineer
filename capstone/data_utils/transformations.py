import numpy as np

def lower_clean_name(word, signs):
    word = word.lower()
    for char in signs:
        word = word.replace(char, '')
    return word

def change_name(ticker):
    if ticker == 'tnx':
        x = 'rates'
    elif ticker == 'gspc':
        x = 'spy'
    elif ticker == 'sif':
        x = 'silver'
    elif ticker == 'gcf':
        x = 'gold'
    elif ticker == 'ixic':
        x = 'nasdaq'
    elif ticker == 'clf':
        x = 'crude oil'
    elif ticker == 'btcusd':
        x = 'btc'
    elif ticker == 'n225':
        x = 'nikkei'
    elif ticker == 'eurusdx':
        x = 'euro'
    elif ticker == '000001ss':
        x = 'shangai'
    else:
        x = ticker
    return x

def min_max_scaler(df, log=False):
    if log:
        df = np.log(df)
    normalized_df=(df-df.min())/(df.max()-df.min())
    return normalized_df, df.min(), df.max()

def back_min_max(ndf,mindf,maxdf, log=False):
    df = ndf*(maxdf-mindf) + mindf
    if log:
        df = np.exp(df)
    return df

def standardizer(df, log=False):
    '''
    Returns log normalized and standartized df, mean and standard deviation of raw dataframe
    '''
    if log:
        df = np.log(df)
    ndf = (df-df.mean())/df.std()
    return ndf, df.mean(), df.std()

def back_standardizer(ndf, mean, std, log=False):
    df = ndf*std + mean
    if log:
        df = np.exp(df)
    return df

def get_log_cumulative(df):
    ndf = (1 + df.pct_change(1)).cumprod()
    ndf = np.log(ndf)
    return ndf