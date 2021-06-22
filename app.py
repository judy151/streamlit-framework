# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 05:17:05 2021

@author: Judy
"""

import requests
#import os
#from os.path import join, dirname
#from dotenv import load_dotenv
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.palettes import Spectral6
import streamlit as st

#from boto.s3.connection import S3Connection
#api_key = S3Connection(os.environ['API_KEY'])


output_file("ticker.html")


#dotenv_path = join(dirname(__file__), '.env')
#load_dotenv(dotenv_path)
#api_key=os.environ.get("API_KEY")

#Checkbox for Tickers
ticker_select = st.selectbox("Select Ticker", ["IBM", "GOOGL", "AAPL", "AMZN"])
st.title("Ticker Information for " + ticker_select)


st.write('Select items for graphing:')
opt_open = st.checkbox('Closing Price')
opt_close = st.checkbox('Opening Price')
opt_high = st.checkbox('Daily high')
opt_low = st.checkbox('Daily low')
opt_adjclose = st.checkbox('Adjusted close')



api_key="XOGU5IREVDTWDYVP"
r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=compact&symbol='+ticker_select+'&apikey='+api_key)
data = r.json()

if len(data)==1:
    st.write("Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.")
    st.write("Wait before refreshing")

else:
    key_name=list(data.keys())[1]    
    metadata=data["Meta Data"]
    
    st.write(metadata)
    df= pd.DataFrame.from_dict(data[key_name], orient='index')
    df.columns=df.columns.str[3:]  # remove leading numbers
    df.index = pd.to_datetime(df.index)
    
    p=figure(x_axis_type="datetime")
    
    
    if opt_open:
        p.line(df.index.values, df["open"], legend_label="open", line_color=Spectral6[0])
    if opt_close:
        p.line(df.index.values, df["close"], legend_label="close", line_color=Spectral6[1])
    if opt_high:
        p.line(df.index.values, df["high"], legend_label="high", line_color=Spectral6[2])
    if opt_low:
        p.line(df.index.values, df["low"], legend_label="low", line_color=Spectral6[3])
    if opt_adjclose:
        p.line(df.index.values, df["adjusted close"], legend_label="adjusted close", line_color=Spectral6[4])
    
    
    p.xaxis.formatter=DatetimeTickFormatter(days=["%b %d, %Y"])
    st.bokeh_chart(p)
