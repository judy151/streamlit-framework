# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 05:17:05 2021

Day-10 milestone task 

@author: Judy
"""
import requests
import os
import pandas as pd
from bokeh.plotting import figure, output_file
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.palettes import Spectral6
import streamlit as st

output_file("ticker.html")

form = st.sidebar.form(key='my_form')
ticker=form.text_input('Enter a ticker symbol (e.g. GOOGL, IBM, AAPL, AMZN)')

opt_open = form.checkbox('Opening Price')
opt_close = form.checkbox('Closing Price')
opt_high = form.checkbox('Daily high')
opt_low = form.checkbox('Daily low')
opt_adjclose = form.checkbox('Adjusted close')

submit= form.form_submit_button(label='Submit')


api_key=os.environ.get("API_KEY")

if submit:
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=compact&symbol='+ticker+'&apikey='+api_key)
    data = r.json()    

    st.title("Ticker Information for " + ticker.upper())
    
    
    if len(data)==1:
        key=data.keys()
        st.write(key)
        st.write(data.get(key))
        #if data[key].find("Invalid"):
         #   st.write(ticker + " is not a valid entry.")
        #else:
        st.write("Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.")
        st.write("Wait before refreshing")
    
    elif len(data)==2:
        key_name=list(data.keys())[1]    
        metadata=data["Meta Data"]
        
        df= pd.DataFrame.from_dict(data[key_name], orient='index')
        df.columns=df.columns.str[3:]  # remove leading numbers
        df.index = pd.to_datetime(df.index)
        
        p = figure(
            x_axis_label="Date",
            y_axis_label="Stock Price",
            x_axis_type="datetime",
            tools="pan,reset,save,wheel_zoom")
        
        cnt=0
        if opt_open:
            p.line(df.index.values, df["open"], legend_label="open", line_color=Spectral6[0])
            cnt+=1
        if opt_close:
            p.line(df.index.values, df["close"], legend_label="close", line_color=Spectral6[1])
            cnt+=1
        if opt_high:
            p.line(df.index.values, df["high"], legend_label="high", line_color=Spectral6[2])
            cnt+=1
        if opt_low:
            p.line(df.index.values, df["low"], legend_label="low", line_color=Spectral6[3])
            cnt+=1
        if opt_adjclose:
            p.line(df.index.values, df["adjusted close"], legend_label="adjusted close", line_color=Spectral6[4])
            cnt+=1
        
        if cnt==0:
            st.write("Select at least one checkbox to graph")
        else:
            st.bokeh_chart(p)
            p.xaxis.formatter=DatetimeTickFormatter(days=["%b %d, %Y"])
    
