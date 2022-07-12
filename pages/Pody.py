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
import inspect
import textwrap
import time
import numpy as np
from streamlit.hello.utils import show_code

def pody_demo():
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)

    st.write(
    """This demo show how to classify the tickets with AI"""
    )
    st.header("Enter the your dispute")

    # Add space for ticket
    dispute_text = st.text_area("Write your ticket", ' ')

    # Add button to check for spam 
    if st.button("Predict"): 
        # Create input 
	    model_input = dispute_text
        # st.write("This ticket is **Spam**")
        

pody_demo()

show_code(pody_demo)