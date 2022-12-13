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
import json
import numpy as np
from streamlit.hello.utils import show_code
import re

import transformers
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, AutoConfig, AutoModel
import torch
# from utils.predict import run_prediction
import numpy as np
from annotated_text import annotated_text
print(torch.__version__)
print(torch.version.cuda)
print(torch.backends.cudnn.version())

project_path = 'C:\\Users\\xinhuang\\Git\\appstasc\\'
model_checkpoint = 'C:\\Users\\xinhuang\\cuad-models\\roberta-large'

import os
import sys
sys.path.append(project_path)
from utils.predict import *

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

@st.cache(allow_output_mutation=True)
def load_model(model_checkpoint):
    return AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)
    print('success')

@st.cache(allow_output_mutation=True)
def load_tokenizer(model_checkpoint):
    return AutoTokenizer.from_pretrained(model_checkpoint, use_fast=False)

model = load_model(model_checkpoint)
tokenizer = load_tokenizer(model_checkpoint)

st.image("TASC-orange-horizontal-logo.png",width=500)
st.title("Contract analysis")
with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   The *Contract analysis* app is an easy-to-use interface built in Streamlit for extracting information from contrtact!
-   It uses a Question answering technique that leverages multiple NLP embeddings and relies on [Transformers] (https://huggingface.co/transformers/) fintuning on the dataset CUAD (https://www.atticusprojectai.org/cuad) to extract information from document.
	    """
    )

with open(project_path+'data/cuad/CUADv1.json') as json_file:
    data = json.load(json_file)

question = data['data'][0]['paragraphs'][0]['qas'][2]['question']
paragraph = ' '.join(data['data'][0]['paragraphs'][0]['context'].split()[:300])
contract = data['data'][0]['paragraphs'][0]['context']
print(question,'\n', contract)

st.header("")
doc = st.text_area(
            "Paste your contract text below (max 500 words)",
            value=contract,
            height=510
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

quesType= st.radio("Choose your question",["Document Name","Parties","Agreement Date", "Governing Law ","..."])
st.warning("41 types of legal clauses can be identified")
# submit_button = st.button(label="✨ Contract analysis")


if st.button(label="✨ Contract analysis"): 
    
    encoding = tokenizer.encode_plus(text=question, text_pair=paragraph)
    input_ids = encoding['input_ids']
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    outputs = model(input_ids=torch.tensor([input_ids]))

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

 # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    print(answer_start, answer_end)

# Combine the tokens in the answer and print it out.
# answer = ' '.join(tokenizer.convert_tokens_to_string(tokens[answer_start:answer_end+1]))
    answer = tokenizer.convert_tokens_to_string(tokens[answer_start:answer_end+1])

    print('Answer: "' + answer + '"')


    res = st.text_area(
            label="Results:",
            value=answer,
            height=20,
        )

