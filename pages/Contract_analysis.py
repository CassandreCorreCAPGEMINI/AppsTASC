#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Contract_analysis.py
@Time    :   2022/07/18 16:12:47
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
import re

import transformers
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, AutoConfig, AutoModel
import torch
# from utils.predict import run_prediction
import numpy as np

print(torch.__version__)
print(torch.version.cuda)
print(torch.backends.cudnn.version())

st.set_page_config(page_title="Contract analysis", page_icon="random")

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

def contract_demo():
    pass


st.sidebar.header("Contract analysis")


st.image("TASC-orange-horizontal-logo.png",width=500)
st.title("Contract analysis")
with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   The *Contract analysis* app is an easy-to-use interface built in Streamlit for extracting information from contrtact!
-   It uses a Question answering technique that leverages multiple NLP embeddings and relies on [Transformers] (https://huggingface.co/transformers/) fintuning on the dataset CUAD (https://www.atticusprojectai.org/cuad) to extract information from document.
	    """
    )

st.header("")
doc = st.text_area(
            "Paste your contract text below (max 500 words)",
            height=510,
        )
ModelType = st.radio("Choose your model",["DistilBERT","deBerta","RoBerta."])


MAX_WORDS = 500
res = len(re.findall(r"\w+", doc))
if res > MAX_WORDS:
    st.warning(
                "⚠️ Your text contains "
                + str(res)
                + " words."
                + " Only the first 500 words will be reviewed. Stay tuned as increased allowance is coming! 😊"
            )

    doc = doc[:MAX_WORDS]

submit_button = st.button(label="✨ Contract analysis")
    
model_checkpoint = 'C:\\Users\\xinhuang\\cuad-models\\roberta-large'


@st.cache(allow_output_mutation=True)
def load_model(model_checkpoint):
    return AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)

@st.cache(allow_output_mutation=True)
def load_tokenizer(model_checkpoint):
    return AutoTokenizer.from_pretrained(model_checkpoint, use_fast=False)

# model = load_model(model_checkpoint)
# tokenizer = load_tokenizer(model_checkpoint)

# model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)
# tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=False)