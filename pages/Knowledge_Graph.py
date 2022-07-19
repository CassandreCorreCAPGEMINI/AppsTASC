#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   KG.py
@Time    :   2022/07/12 15:00:31
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

def kg_demo():
    pass

st.set_page_config(page_title="Knowledge Graph", page_icon="📊")

def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


_max_width_()

st.sidebar.header("Knowledge Graph")