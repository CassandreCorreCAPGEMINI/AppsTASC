#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Disputes classification.py
@Time    :   2022/11/29 17:57:37
@Author  :   Xin HUANG 
@Version :   1.0
@Contact :   xin.huang@capgemini.com
'''


# here put the import lib
import streamlit as st
## for data
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import pickle

## for processing
import re
import nltk
import spacy
## for machine learning
from sklearn import feature_extraction, feature_selection , model_selection, naive_bayes, pipeline, manifold, preprocessing, metrics
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.feature_selection import chi2

## for word embedding
import gensim
import gensim.downloader as gensim_api
from gensim.models import KeyedVectors
## for deep learning
from keras import backend as K
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.layers import Dense, Input, GlobalMaxPooling1D, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
# from keras.initializers import Constant
from keras.callbacks import ModelCheckpoint
from tensorflow import keras
from keras import regularizers

from streamlit.hello.utils import show_code

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode

## for word embedding
import gensim
import gensim.downloader as gensim_api
from gensim.models import KeyedVectors

st.title("Disputes classifcation")

nlpModelFile = "C:\\Users\\xinhuang\\Datasets\\frWiki_no_lem_no_postag_no_phrase_1000_skip_cut200.bin"

project_path = 'C:\\Users\\xinhuang\\Git\\appstasc\\'
train_path = project_path+'data\\pody\\aug_train_v3.csv'
test_path = project_path+'data\\pody\\test.csv'


MAX_SEQUENCE_LENGTH = 50
MAX_NUM_WORDS = 10579
EMBEDDING_DIM = 1000
VALIDATION_SPLIT = 0.2
NUM_CATEGORIES = 14

@st.cache
def get_data(file):
    dtf = pd.read_csv(file, sep=';',encoding = 'utf-8',header=0,dtype=str)
    print('all data shape', dtf.shape)
    return dtf

@st.cache
def load_nlpModel(file):
    nlp_model = KeyedVectors.load_word2vec_format(file, binary=True, unicode_errors="ignore")
    return nlp_model

@st.cache(allow_output_mutation =True)
def load_spacyModel(name):
    nlp = spacy.load(name)
    return nlp

@st.cache
def load_LabelEncoder(file):
    with open(file, 'rb') as pkl_file:
        le = pickle.load(pkl_file) 
        pkl_file.close()
        return le

@st.cache
def load_tokenizer(file):
    with open(file, 'rb') as handle:
        tokenizer = pickle.load(handle)
        return tokenizer

@st.cache
def load_embeddings(file):
    embeddings = np.load(file)
    return embeddings

nlp_model = load_nlpModel(nlpModelFile)
nlp = load_spacyModel("fr_core_news_lg")
# nlp = spacy.load("fr_core_news_lg")
le = load_LabelEncoder(project_path+"data\\pody\\le_category.pkl")
le1 = load_LabelEncoder(project_path+"data\\pody\\le_sub_category.pkl")
tokenizer = load_tokenizer(project_path+"data\\pody\\tokenizer.pkl")
embeddings = load_embeddings(project_path+"data\\pody\\embeddings.npy")


st.write(
    """This demo show how to classify the tickets with AI"""
    )

train_df = get_data(train_path)
# st.dataframe(df)

test_df = get_data(test_path)

gb = GridOptionsBuilder.from_dataframe(test_df[:20])
# enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=False)
# gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
gridOptions = gb.build()

response = AgGrid(
        test_df[:20],
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
    )

st.text("Test data shape:"+str(test_df.shape))
dtf = pd.DataFrame(response["selected_rows"])
st.subheader("Filtered data will appear below 👇 ")
st.text("")
st.dataframe(dtf)


df = pd.concat([train_df, test_df], axis=0)

ModelType = st.radio("Choose your model",["TextCNN", "TextRNN","DistilBERT","etc."])

model1 = keras.models.load_model(project_path+'models\\pody_categories')
model2 = keras.models.load_model(project_path+'models\\pody_sub_categories')

if st.button("Predict the tickets"): 
        list_disputes = dtf['text_clean']
        print(len(list_disputes))
        print(list_disputes)
        lst_corpus = []
        for string in list_disputes:
            lst_words = string.split()
            lst_grams = [" ".join(lst_words[i:i+1]) for i in range(0, len(lst_words), 1)]
            lst_corpus.append(lst_grams)
        lst_text2seq= tokenizer.texts_to_sequences(lst_corpus)
        print(lst_text2seq)
        X = pad_sequences(lst_text2seq, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post")

        predicted_valid_prob = model1.predict(X)
        print(X[0])
        predicted_label=[list(x).index(max(x)) for x in predicted_valid_prob]
        print(predicted_label)
        predicted_valid = le.inverse_transform(predicted_label)
        print(predicted_valid)

        predicted_valid_prob2 = model2.predict(X)
        print(X[0])
        predicted_label2=[list(x).index(max(x)) for x in predicted_valid_prob2]
        print(predicted_label2)
        predicted_valid2 = le1.inverse_transform(predicted_label2)
        print(predicted_valid2)

        result = pd.DataFrame(data=[],columns=['category', 'sub-category'])
        result['category'] = predicted_valid
        result['sub-category'] = predicted_valid2
        st.header("Prediction results")
        st.dataframe(result)

