#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2022/11/15 16:14:24
@Author  :   Xin HUANG 
@Version :   1.0
@Contact :   xin.huang@altran.com
'''

# here put the import lib


import streamlit as st
from annotated_text import annotated_text, annotation
from streamlit.logger import get_logger

import inspect
import textwrap
import time
import json
import numpy as np
from streamlit.hello.utils import show_code
import re

import transformers
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, AutoConfig, AutoModel
from transformers import pipeline
import torch

import numpy as np

print(torch.__version__)
print(torch.version.cuda)
print(torch.backends.cudnn.version())

from streamlit.hello.utils import show_code

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode


project_path = 'C:\\Users\\xinhuang\\Git\\appstasc\\'
model_checkpoint = 'C:\\Users\\xinhuang\\cuad-models\\roberta-large'
LOGGER = get_logger(__name__)

ModelType=""
quesType=""
contractType=""
st.set_page_config(page_title="Contract analysis", page_icon="TASC-orange-horizontal-logo.png",layout="wide")

    


def header_app():
    
    st.image("TASC-orange-horizontal-logo.png",width=500)
    st.title("Contract analysis")
    with st.expander("ℹ️ - About this app", expanded=True):

        st.write(
        """     
-   The *Contract analysis* app is an easy-to-use interface built in Streamlit for extracting information from contrtact!
-   It use the model of text classification for identifying the type of contract and clause.
-   It uses a Question answering technique that leverages multiple NLP embeddings and relies on [Transformers] (https://huggingface.co/transformers/) fintuning on the dataset CUAD (https://www.atticusprojectai.org/cuad) to extract information from document.
	    """
    )


def load_file():
    """Load text from file"""
    uploaded_file = st.file_uploader("Upload Files",type=['txt'])
    file_name =" "
    raw_text=" "
    if uploaded_file is not None:
        print(uploaded_file.name)
        file_name = uploaded_file.name
        if uploaded_file.type == "text/plain":
            raw_text = str(uploaded_file.read(),"utf-8")
    return raw_text, file_name



@st.cache(allow_output_mutation=True)
def load_model(model_checkpoint):
    return AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)

@st.cache(allow_output_mutation=True)
def load_tokenizer(model_checkpoint):
    return AutoTokenizer.from_pretrained(model_checkpoint, use_fast=False)

model = AutoModelForQuestionAnswering.from_pretrained(model_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=False)

if __name__ == "__main__":

    header_app()
    st.sidebar.header("Contract analysis")
    ModelType = st.sidebar.radio("Choose your model",["DistilBERT","deBerta","RoBerta."])
    quesType= st.sidebar.radio("Choose your question",["Document Name","Parties","Agreement Date","Effective Date", "Expiration Date" ,
    "Renewal Term","Terminate Renewal","Governing Law","Etc..."])
    st.sidebar.warning("41 types of legal clauses can be identified")
    # contractType = st.sidebar.selectbox("Choose your contract type",["Affiliate_Agreements", "Co_Branding", "Development","Distributor" , "License_Agreements","Maintenance", "Manufacturing", "Service", "Supply","Transportation"])
    
    print("***************"+quesType)
    # App title and description

    with open(project_path+'data/cuad/CUADv1.json') as json_file:
        data = json.load(json_file)

    if quesType == "Document Name":
        question = data['data'][0]['paragraphs'][0]['qas'][0]['question']
    elif quesType == "Parties":
        question = data['data'][0]['paragraphs'][0]['qas'][1]['question']
    elif quesType == "Agreement Date":
        question = data['data'][0]['paragraphs'][0]['qas'][2]['question']
    elif quesType == "Effective Date":
        question = data['data'][0]['paragraphs'][0]['qas'][3]['question']
    elif quesType == "Expiration Date":
        question = data['data'][0]['paragraphs'][0]['qas'][4]['question']
    elif quesType == "Renewal Term":
        question = data['data'][0]['paragraphs'][0]['qas'][5]['question']
    elif quesType == "Terminate Renewal":
        question = data['data'][0]['paragraphs'][0]['qas'][6]['question']
    elif quesType == "Governing Law":
        question = data['data'][0]['paragraphs'][0]['qas'][7]['question']
    

    # question = data['data'][0]['paragraphs'][0]['qas'][3]['question']
    print(quesType)

    # Load file
    raw_text,uploaded = load_file()
    
    paragraph = ' '
    if raw_text != None and raw_text != '':
        if question != '' and raw_text != '':
            paragraph = ' '.join(raw_text.split()[:250])
        # Display text
        with st.expander("See contract text"):
            st.write(raw_text)

        # Perform question answering
        # question_answerer = pipeline(task='question-answering', model=model, tokenizer=tokenizer)

        # answer = ''
        # question = st.text_input('Ask a question')

        # if question != '' and raw_text != '':
        #     answer = question_answerer({
        #         'question': question,
        #         'context': raw_text
        #     })

        # st.write(answer)
  
    # print(question,'\n', contract)

    col1, col2 = st.columns(2)

    with col1:

        if st.button(label="✨ Contract classification and Clause segmentation"): 
            st.warning("Identify contract type and the information contained in each paragraph or clause")
            st.info("Contract type")
            if uploaded == "PROFOUNDMEDICALCORP_08_29_2019-EX-4.5-SUPPLY AGREEMENT.txt":
                st.text("Supply")
            elif uploaded== "MTITECHNOLOGYCORP_11_16_2004-EX-10.102-Reseller Agreement Premier Addendum.txt":
                st.text("Reseller")
            else:
                st.text("Service")
            st.info("Clause segmentation")
            annotated_text((' '.join(raw_text.split()[:300]), "\n GENERAL INFORMATION"))
            annotated_text((' '.join(raw_text.split()[300:600]), "TERMS") )
     

    with col2:
        if st.button(label="✨ Contract extraction"): 
            # question_answerer = pipeline(task='question-answering', model=model, tokenizer=tokenizer)

            # answer = ''
            # question = st.text_input('Ask a question')

            # if question != '' and raw_text != '':
            #     answer = question_answerer({
            #     'question': question,
            #     'context': raw_text
            # })
            #     st.write(answer)
        
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
            height=20,)

    print(question)