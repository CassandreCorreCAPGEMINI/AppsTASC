#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Pody.py
@Time    :   2022/07/12 11:13:03
@Author  :   Xin HUANG 
@Version :   1.0
@Contact :   xin.huang@altran.com
'''

# here put the import lib



import streamlit as st


## for data
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle
import time
import plotly.express as px


# --- Initialising SessionState ---
if "load_state" not in st.session_state:
     st.session_state.load_state = False


st.header("Fruits List")

@st.cache()
def load_data():

    _dic = { 'Name': ['Mango', 'Apple', 'Banana'],
         'Quantity': [45, 38, 90]}
    _df = pd.DataFrame(_dic)
    return _df

_df = load_data()
load = st.button('Load Data')
if load or st.session_state.load_state:
    st.session_state.load_state =True
    st.write(_df)
   
 # ---- Plot types -------
opt = st.radio('Plot type :',['Bar', 'Pie'])
if opt == 'Bar':
    fig = px.bar(_df, x= 'Name',
                y = 'Quantity',title ='Bar Chart')
    st.plotly_chart(fig)

else:     
    fig = px.pie(_df,names = 'Name',
                values = 'Quantity',title ='Pie Chart')
    st.plotly_chart(fig)


placeholder = st.empty()

# Replace the placeholder with some text:
placeholder.text("Hello")

# Replace the text with a chart:
placeholder.line_chart({"data": [1, 5, 2, 6]})

# Replace the chart with several elements:
with placeholder.container():
    st.write("This is one element")
    st.write("This is another")

# Clear all those elements:
# placeholder.empty()


with st.form("my_form"):
   st.write("Inside the form")
   slider_val = st.slider("Form slider")
   checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")

if 'num' not in st.session_state:
    st.session_state.num = 0


choices1 = ['no answer', 'manila', 'tokyo', 'bangkok']
choices2 = ['no answer', 'thailand', 'japan', 'philippines']

qs1 = [('What is the capital of Japan', choices1),
    ('What is the capital of Philippines', choices1),
    ('What is the capital of Thailand', choices1)]
qs2 = [('What country has the highest life expectancy?', choices2),
    ('What country has the highest population?', choices2),
    ('What country has the highest oil deposits?', choices2)]

placeholder = st.empty()
num = st.session_state.num
with placeholder.form(key=str(num)):

    st.radio("sss000",[1,2,3])
    st.radio("aaaaaa",[1,2,3])
    st.selectbox('Answer:', [1,2,3])

    if st.form_submit_button():
        st.write("&&&&&&&&&&&&&&&&&&&&&")
def main():
    for _, _ in zip(qs1, qs2): 
        placeholder = st.empty()
        num = st.session_state.num
        with placeholder.form(key=str(num+1)):
            st.radio(qs1[num][0], key=num+1, options=qs1[num][1])
            st.radio(qs2[num][0], key=num+1, options=qs2[num][1])          
                      
            if st.form_submit_button():
                st.session_state.num += 1
                if st.session_state.num >= 3:
                    st.session_state.num = 0 
                placeholder.empty()
            else:
                st.stop()


main()

