import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_stations():
    df = pd.read_csv('s3://adfc-bike-census/adfc_data/transformed/combined.csv')
    df['date'] = pd.to_datetime(df['date'])
    #df = df.resample('H', on='date').sum()
    df.drop('timestamp', 1, inplace=True)
    return df

def to_pivot(df: pd.DataFrame):
    return df.pivot(index='date', columns=['city', 'station_code'], values='count')


def plot_city_time(name: str):
    df = read_stations()
    city = to_pivot(df)[name]
    city = city.resample('H').sum()
    plotsize = (25, 10)
    layout = (-1, 5)
    city.groupby(city.index.date).mean().plot(kind='line',subplots=True, sharey=False,layout=layout, figsize=plotsize, title=f"{name} over time")
    city.groupby(city.index.dayofyear).mean().plot(kind='line',subplots=True, sharey=False,layout=layout, figsize=plotsize, title=f"{name}s average count per day of the year")
    city.groupby(city.index.weekday).mean().plot(kind='bar',subplots=True, sharey=False,layout=layout, figsize=plotsize, title=f"{name}s average count per day of the week")
    city.groupby(city.index.hour).mean().plot(kind='bar',subplots=True, sharey=False,layout=layout, figsize=plotsize, title=f"{name}s average count per hour of the day")

def strip_weekends(df):
    return df[df.index.weekday < 5]

def berufsverkehr(df):
    df = strip_weekends(df)
    return df[(df.index.hour<10)&(df.index.hour>5)]

def freizeit(df,start,stop,weekday):
    return df[(df.index.weekday<weekday)&(df.index.dt.hour<stop)&(df.index.hour>start)]

def covid(df):
    return df[(df.index.year<2020)]

def classify(df):
    nc_df = covid(df)
    mean_beruf = Berufsverkehr(nc_df)['comptage'].mean()
    mean_freizeit = Freizeit(nc_df,10,16,7)['comptage'].mean()
    if mean_beruf < mean_freizeit:
        return 0
    else:
        return 1
    return 


def load_weather(city):
    df_weather = pd.read_csv('weather/weather_{}.csv'.format(city), delimiter=';')
    
    df_weather.rename(columns = {'MESS_DATUM': 'date', ' TMK': 'avg_temp', ' RSK': 'rainfall'}, inplace = True)
    df_weather['date'] = pd.to_datetime(df_weather['date'],format='%Y%m%d')
    df_weather = df_weather[df_weather['date'].dt.year >= 2016]
    
    df_weather.drop(['STATIONS_ID', '  FX', '  FM', 'QN_3', 'QN_4', 'RSKF', ' SDK', 'SHK_TAG', '  NM', ' VPM', '  PM', ' UPM', ' TXK', ' TNK', ' TGK', 'eor'], axis=1, inplace=True)
    df_weather = df_weather.set_index('date')
    
    return df_weather


def bedingte_erwartung(X,Y,y_1,y_2):
    '''

    Parameters
    ----------
    X : numpy array (Bikers counted that day)
    Y : numpy array (Temperature that day, Month that day, Rain that day, sunshine that day)
    y_1 : float,int
    y_2 : float,int

    Returns
    -------
    ex_y : E[X|y_1<Y<=y_2] or E[X| Y == y_1] (when y_1 = y_2)

    '''
    values = np.unique(X)
    p_xy = np.zeros(np.size(values))
    if y_1 == y_2: 
            ind2 = np.equal(Y,y_2)
    else:
            ind21 = np.greater(Y,y_1)
            ind22 = np.less_equal(Y,y_2)
            ind2 = np.multiply(ind22,ind21)
    py = np.sum(ind2)
    counter = 0
    for k in values:
        ind1 = np.equal(X,k)
        ind = np.multiply(ind2,ind1)
        pxy = np.sum(ind)
        p_xy[counter] = pxy/py
        counter+= 1
    ex_y = np.sum(np.multiply(values,p_xy))
    return ex_y
