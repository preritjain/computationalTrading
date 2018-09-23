'''
Created on 23-Sep-2018

@author: prerit
'''
def HA(df):
    df['HA_Close']=(df['Open']+ df['High']+ df['Low']+df['Close'])/4

    idx = df.index.name
    df.reset_index(inplace=True)

    for i in range(0, len(df)):
        if i == 0:
            df.set_value(i, 'HA_Open', ((df.get_value(i, 'Open') + df.get_value(i, 'Close')) / 2))
        else:
            df.set_value(i, 'HA_Open', ((df.get_value(i - 1, 'HA_Open') + df.get_value(i - 1, 'HA_Close')) / 2))

    if idx:
        df.set_index(idx, inplace=True)

    df['HA_High']=df[['HA_Open','HA_Close','High']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','Low']].min(axis=1)
    return df



