# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 18:20:21 2020

@author: harry
"""
import requests
import pandas
#from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
#import simplejson as json

apicode='7T7Z8AXC4TTZ6N15'

def getdata(ticker):
    """
        takes ticker, outputs dataframe 
        
        Returns
        -------
        fig : pandas data frame """
    error= None
    df= None
    try:
        curdict = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker+'&interval=15min&outputsize=full&apikey='+apicode)
    except requests.exceptions.RequestException:
        error=1
    # getting dataframe with datetimeindex
    curdict=curdict.json()
    # wrong ticker
    if len(list(curdict.keys()))<2:
        error=2
    else:
        df = pandas.DataFrame(curdict[list(curdict.keys())[1]]).transpose()
        df.rename(columns=lambda x: x.split(" ")[1], inplace=True)
        df.index = pandas.to_datetime(df.index)
        # only taking the last month
        df=df.iloc[df.index>=df.index[0]-pandas.DateOffset(months=1),:]
    
    return [df, error]

def plot_series(width, height, ticker, df, series):
    """
        takes data, plot height and weight, series names and plots

        Returns
        -------
        fig : Bokeh Figure """  
    colors={'low':'red', 'high':'blue', 'close':'green', 'open':'purple'}
    fig= figure(plot_width=width, plot_height=height, x_axis_type="datetime", title='Stock price of '+ticker)
    for col in series:
        fig.line(x=df.index, y=df[col], color=colors[col], legend_label=col)
    fig.legend.location='top_left'
    return fig

# to add <script src="https://cdn.bokeh.org/bokeh/release/bokeh-x.y.z.min.js"
#        crossorigin="anonymous"></script>



