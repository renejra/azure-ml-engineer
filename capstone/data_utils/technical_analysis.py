import pandas as pd

def transform_ma(data, ma1=4, ma2=50, ma3=80):
    '''
    Moving Averages
    Gets a DataFrame and adds columns of three simple moving averages
    :param data: DataFrame

    (optional)
    :param ma1: int
    :param ma2: int
    :param ma3: int
    :return: DataFrame
    '''
    data['MA'+str(ma1)] = round(data['close'].rolling(ma1).mean(),0)
    data['MA'+str(ma2)] = round(data['close'].rolling(ma2).mean(),0)
    data['MA'+str(ma3)] = round(data['close'].rolling(ma3).mean(),0)
    return data



def transform_rsi(data, alpha=14, smoothK=3, smoothD=3):
    '''
    Relative Strenght Index and StochRSI
    Gets a DataFrame and returns columns with (stochastic) RSI features
    :param data: DataFrame

    optional
    :param alpha:
    :param smoothK:
    :param smoothD:

    :return: DataFrame
    '''
    data['change'] = data['close'].pct_change(1)
    data['cum_change'] = (data['change']+1).cumprod()
    data['k'] = 0
    data['d'] = 0
    cond_k = data.change > 0
    cond_d = data.change < 0
    data['k'] = data.k.mask(cond_k, data['change'])
    data['d'] = data.d.mask(cond_d, - data['change'])

    # data['num'] = data['k'].rolling(alpha).mean()
    data['num'] = pd.Series.ewm(data['k'], span=alpha).mean()
    data['div'] = pd.Series.ewm(data['d'], span=alpha).mean()

    # data['div'] = data['d'].rolling(alpha).mean()
    data['rs'] = data['num']/data['div']
    data['RSI'] = (100 - (100/(1+data['rs'])))
    data['RSImin'] = data['RSI'].rolling(alpha).min()
    data['RSImax'] = data['RSI'].rolling(alpha).max()
    data['stochRSI'] = 100*(data['RSI'] - data['RSImin']) / (data['RSImax'] - data['RSImin'])
    data['smoothK'] = round(data['stochRSI'].rolling(smoothK).mean(),2)
    data['smoothD'] = round(data['smoothK'].rolling(smoothD).mean(),2)
    data['K1'] = data['smoothK'].shift(1)
    data['D1'] = data['smoothD'].shift(1)

    # cond_num_zero = data.num == 0
    # data['RSI'] = data.RSI.mask(cond_num_zero, 0)

    # cond_div_zero = data.div == 0
    # data['RSI'] = data.RSI.mask(cond_div_zero, 100)

    return data



def transform_std(df, confidence=80):
    '''
    Adds

    :param df:
    :param confidence:
    :return:
    '''
    df['btc_std_dev'] = df['returns'].expanding(2).std()
    df['btc_mean'] = df['returns'].expanding(2).mean()
    # df['conf_int_p'] = np.percentile(df['change'], (100-confidence)/2)
    # df['conf_int_m'] = np.percentile(df['change'], confidence + (100-confidence)/2)
    df['std_dif'] = (df['close'] - df['btc_std_dev']).abs()

    return df
