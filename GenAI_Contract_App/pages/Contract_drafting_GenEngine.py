#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   contract_drafting_GenEngine.py
@Time    :   2025/03/18 16:04:
@Author  :   Akhli RIOUFFREYT
@Version :   1.0
@Contact :   akhli.riouffreyt@capgemini.com
"""

import streamlit as st
import websocket
import json
from contextlib import closing
from uuid import uuid4


def header_app():
    st.image("TASC-orange-horizontal-logo.png", width=500, )
    with st.expander("ℹ️ - About this app", expanded=True):
        st.write(
            """     
-   The *Contract drafting* app is used to quickly generate corresponding contracts or terms according to needs.
-   Our app is based on the model from Generative engine de Capgemini.
"""
        )


header_app()

SOCKET_URL = "wss://ws.generative.engine.capgemini.com/"
API_TOKEN = "16zuz9jnWZ7WLRwkIXYtb7TO7igJnBhRadp6fPOj"


def generate(prompt):
    print("Input prompt:", prompt)
    url = SOCKET_URL
    with closing(websocket.create_connection(url, header={"x-api-key": API_TOKEN})) as ws:
        send_query(ws, prompt, session_id=uuid4())
        response = None
        while response is None:
            message = ws.recv()
            print(message)
            message = json.loads(message)
            action = message.get("action")
            if "final_response" == action:
                response = message.get("data", {}).get("content")
    return response


def send_query(ws, prompt, session_id):
    data = {
        "action": "run",
        "modelInterface": "langchain",
        "data": {
            "mode": "chain",
            "text": prompt,
            "workspaceId": "6fb9a8ac-1649-417d-8437-b2f8703c2d4c",
            "dataSources":[
                    {
                        "type": "database",
                        "id": "cf3b4fae-353d-4cc0-9219-f51c494a945c",
                        "retrievalKwargs": 3
                    }
                ],
            "files": [],
            "modelName": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "provider": "bedrock",
            "sessionId": str(session_id),
            "modelKwargs": {
                "streaming": False,
                "maxTokens": 8192,
                "temperature": 0.7,
                "topP": 0.7
            }
        }
    }
    ws.send(json.dumps(data))


# contract drafting
st.header('Contract drafting', divider='rainbow')  # titre
# menu déroulant qui propose des exemples de prompt
option_contract = st.selectbox(
    "Contract requirements:",
    ("Write a procurement contract for Company BBB to purchase network equipment from the AAA company.",
     "Write a procurement contract",
     "Write a procurement contract for Company BBB to purchase network equipment from the AAA company. The contract needs to contain a Renewal Term  clause, and all disputes will be subject to the jurisdiction of the EU."),
    index=0,
    placeholder="Select contract ...",
)

# entrée pour recevoir le prompt utilisateur
contract_req = st.text_area(
    "Contract requirements:",
    option_contract
)
st.warning("The more detailed the contract requirements are, the higher the quality of the generated contract will be.")
text1 = contract_req

if st.button(label="✨ Submit", key=2):
    res1 = generate(text1)
    show_res1 = "".join(res1)
    re1 = st.markdown(show_res1)

# clause drafting
st.header('Clause drafting', divider="rainbow")  # titre de la section
# menu déroulant qui propose des exemples de prompt
option_clause = st.selectbox(
    "Clause requirements:",
    ("Write a contract clause of Renewal Term ", "Write a contract clause of insurance",
     "Write a contract clause of Termination for Convenience "),
    index=0,
    placeholder="Select clause ...",
)

# entrée pour recevoir le prompt utilisateur
clause_req = st.text_area(
    "Clause requirements:",
    option_clause
)
st.warning("The more detailed the clause requirements are, the higher the quality of the generated clause will be.")
text2 = clause_req

# bouton pour soumettre la requête utilisateur
if st.button(label="✨ Submit", key=3):
    res2 = generate(text2)
    show_res2 = "".join(res2)
    re1 = st.markdown(show_res2)
