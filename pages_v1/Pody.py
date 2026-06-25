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

project_path = 'C:\\Users\\xinhuang\\Git\\appstasc\\'
train_path = project_path+'data\\pody\\aug_train_v3.csv'
test_path = project_path+'data\\pody\\test.csv'


MAX_SEQUENCE_LENGTH = 50
MAX_NUM_WORDS = 10579
EMBEDDING_DIM = 1000
VALIDATION_SPLIT = 0.2
NUM_CATEGORIES = 14

# st.set_page_config(page_title="Classification of text", page_icon="random")
# st.image("TASC-orange-horizontal-logo.png",width=600)

# st.header("Deep learning for text classification")
# st.markdown(
#         """
#         1. Deep learning methods are proving very good at text classification, achieving state-of-the-art results on a suite of standard academic benchmark problems.
#         - TextCNN, TextRNN, FastText, Transformers
#         2. But these algorithms don't work well enough on the Pody dataset.
#     """
#     )

# st.header("Data Description")
# st.markdown(
#         """
#         1. 13 categories et 81 sub-categories: distribution très déséquilibré
#         2. Ambiguous classification: le bruit dans les données peut affecter négativement le modèle
#         Ex: 165 disputes contain « Merci de réessayer » are classified into different categories
#     """
#     )
# st.image("ambiguity.png",width=800)
# st.image("ambiguity1.png",width=500)
# st.markdown(
#         """
#         3. Text augmentation, Ambiguity clean

#     """
#     )

# st.header("Objectifs")
# st.markdown(
#         """
#         1. Distinguer le texte qui peut être traité manuellement et automatiquement?​
#         2. Un niveau de performance le plus élevé possible (proche à 100%)
#     """
#     )

# st.header("Application of Deep learning model")
# st.markdown(
#         """
#         1. Application intégrée
#         - Script exécuté locale ou sous le logiciel RPA
#         - API Rest(API web): Python, flask
#         2. Application indépendante(Web Application)
#         - frontend: Html,CSS, backend:Python, Flask
#         - frontend et backend: js(vue,React, node.js)
#         - frontend et backend: Python(streamlit) (⚠️this Demo⚠️) . 
        
#     """
#     )
# st.header("Options pour deploy AI")
# st.markdown(
#         """
#         - Seveur intern
#         - Cloud: AWS, Google Cloud, Azure
#         - https://streamlit.io/ : Streamlit turns data scripts into shareable web apps in minutes. All in pure Python. No front‑end experience required.
#     """
#     )

st.title("Disputes classifcation")

@st.cache
def get_data(file):
    dtf = pd.read_csv(file, sep=';',encoding = 'utf-8',header=0,dtype=str)
    print('all data shape', dtf.shape)
    return dtf

nlp_model = KeyedVectors.load_word2vec_format("C:\\Users\\xinhuang\\Datasets\\frWiki_no_lem_no_postag_no_phrase_1000_skip_cut200.bin", 
    binary=True, unicode_errors="ignore")
nlp = spacy.load("fr_core_news_lg")

from nltk.stem.snowball import SnowballStemmer
def return_stem(text):

    stemmer = SnowballStemmer(language='french')
    doc = nlp(text)
    lst_text = [stemmer.stem(X.text) for X in doc]
    return " ".join(lst_text)

def return_lemm(text):
  
    doc = nlp(text)
    lst_text = [X.lemma_ for X in doc]
    return " ".join(lst_text)


def preprocess_text_fr(text, flg_stemm=False, flg_lemm=False, lst_stopwords=None):
    # Converting to Lowercase
    text = text.lower()
    text = re.sub(r'[,.\!\?\%\(\)\/\\\-"]', ' ', text)
    # text = re.sub(r'\&\S*\s', '', text)
    # text = re.sub(r"\-", "", text)
    # Remove all the special characters
    # text = re.sub(r'\W', ' ', text)
    # Substituting BL with bon livraison
    text = re.sub(r'\sbl', ' bon livraison ', text)
    text = re.sub(r'(^|\s)qt[y|é]', ' quantité ', text)
    text = re.sub(r'\spcs', ' pièces ', text)
    # remove all digit: Substituting digit with number
    # text = re.sub(r'\d+', ' nombre ', text)
     #remove cdlt at the end of ticket
    # text = re.sub(r'cd[lt|t].*$', '', text)
     # Substituting multiple spaces with single space
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    
    # remove 
    text = text.strip()

    lst_text = list()
    ## Tokenize (convert from string to list)
    # lst_text = return_token(text)
    lst_text = text.split(' ')

    # remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    lst_stopwords]

    ## back to string from list
    text = " ".join(lst_text)

    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        text = return_stem(text)
    
            
    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        text = return_lemm(text)
    # print(text)
    return text

le = preprocessing.LabelEncoder()
le1 = preprocessing.LabelEncoder()

with open(project_path+"data\\pody\\le_category.pkl", 'rb') as pkl_file:
    le = pickle.load(pkl_file) 
    pkl_file.close()
    
with open(project_path+"data\\pody\\le_sub_category.pkl", 'rb') as pkl_file1:
    le1 = pickle.load(pkl_file1) 
    pkl_file1.close()

## tokenize text
with open(project_path+"data\\pody\\tokenizer.pkl", 'rb') as handle:
    tokenizer = pickle.load(handle)
    handle.close()

def pody_demo():
   
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    


    st.write(
    """This demo show how to classify the tickets with AI"""
    )

    train_df = get_data(train_path)
    # st.dataframe(df)

    test_df = get_data(test_path)

    df = pd.concat([train_df, test_df], axis=0)

    X = df['text_clean']
    y = df['category']
    y1 = df['RTC detail']
    print(X.shape, y.shape,y1.shape)
    corpus = df['text']


    lst_stopwords = nltk.corpus.stopwords.words("french")
    lst_stopwords = list()
    lst_stopwords.append('bonjour')
    print(lst_stopwords)
    ## create list of lists of unigrams
    lst_corpus = []
    for string in corpus:
        lst_words = string.split()
        lst_grams = [" ".join(lst_words[i:i+1]) for i in range(0, len(lst_words), 1)]
        lst_corpus.append(lst_grams)
    print(len(lst_corpus))


    ## create sequence
    lst_text2seq= tokenizer.texts_to_sequences(lst_corpus)
    print(lst_text2seq[:5])
    # print(lst_text2seq.shape)
    ## padding sequence
    X = pad_sequences(lst_text2seq, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post")
    print('data shape: ',X.shape)

    embeddings = np.load(project_path+"data\\pody\\embeddings.npy")
  

    gb = GridOptionsBuilder.from_dataframe(test_df)
    # enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=False)
    gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
    gridOptions = gb.build()
    

    response = AgGrid(
        test_df,
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

    st.text("")

    # model1 = keras.models.load_model(project_path+'models\\pody_categories')
    # model2 = keras.models.load_model(project_path+'models\\pody_sub_categories')

    ModelType = st.radio("Choose your model",["TextCNN", "TextRNN","DistilBERT","etc."])

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


def pody_demo1():
    st.header("Enter the your dispute")

    # Add space for ticket
    dispute_text = st.text_area("Write your ticket", height=10)

    # if dtf.empty:
    #     dispute_text = st.text_area("Write your ticket", '')
    # else:
    #     dispute_text = st.text_area("Write your ticket", dtf.text[0])
    


    ## create sequence
    list_disputes = list()
    list_disputes.append(dispute_text.split())
    print(list_disputes)
    lst_text2seq= tokenizer.texts_to_sequences(list_disputes)
    print(lst_text2seq)
    X = pad_sequences(lst_text2seq, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post")

  

    # Add button to check for ticket
    if st.button("Predict"): 
        # Create input 
        model_input = dispute_text
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




st.sidebar.header("Pody Disputes Classification")


with st.expander("ℹ️ - About this app", expanded=True):

    st.write(
        """     
-   The *Pody* app is an easy-to-use interface built in Streamlit for classifying the tickets!
-   It uses a Deep Learning technique that leverages multiple NLP embeddings and relies on the libraries [Keras] (https://keras.io/) and [Transformers] (https://huggingface.co/transformers/).
	    """
    )

model1 = keras.models.load_model(project_path+'models\\pody_categories')
model2 = keras.models.load_model(project_path+'models\\pody_sub_categories')
pody_demo()
pody_demo1()

# show_code(pody_demo)