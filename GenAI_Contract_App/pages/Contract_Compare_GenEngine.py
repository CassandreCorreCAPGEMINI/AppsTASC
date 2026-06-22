#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   Untitled-1
@Time    :   2025/03/18 16:04:
@Author  :   Akhli RIOUFFREYT
@Version :   2.0
@Contact :   akhli.riouffreyt@capgemini.com
"""

#import lib
import streamlit as st
from pypdf import PdfReader
import fitz
import websocket
import json
from contextlib import closing
from uuid import uuid4


def header_app():
    st.image("TASC-orange-horizontal-logo.png", width=500, )
    st.header("Contract Compare", divider='rainbow')
    with st.expander("ℹ️ - About this app", expanded=True):
        st.write(
            """     
-   The *Contract Compare* app is used to compare the differences between two contracts and display the results in a table.
-   Our app is using Capgemini Generative Engine. 
-   Pdf and txt files are accepted by our app, Tick the checkbox OCR to read scanned PDF.
"""
        )


def load_file(counter):
    """Load text from file"""
    uploaded_file = st.file_uploader("Upload Contract:", type=['pdf', 'txt'], key=counter)
    file_name = " "
    raw_text = " "
    if uploaded_file is not None:
        print(uploaded_file.name)
        file_name = uploaded_file.name
        if uploaded_file.type == "text/plain":
            raw_text = str(uploaded_file.read(), "utf-8")
        elif uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            raw_text = text

    return raw_text, file_name


def extract_text_from_pdf(pdf_document):
    """for OCR"""
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


def load_ocr(counter):
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key=counter)
    file_name = " "
    raw_text = " "
    if uploaded_file is not None:
        print(uploaded_file.name)
        file_name = uploaded_file.name
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        extracted_text = extract_text_from_pdf(pdf_document)
        raw_text = extracted_text
    return raw_text, file_name


header_app()
count = 0
ocr1 = st.checkbox("Enable OCR: for reading pdf scanned on image", key="ocr1")
if ocr1:
    contract1, uploaded1 = load_ocr(count)
    count += 1
    if contract1 is not None and contract1 != '':
        with st.expander("See contract text"):
            st.write(contract1)
else:
    contract1, uploaded1 = load_file(count)
    count += 1
    if contract1 is not None and contract1 != '':
        with st.expander("See contract text"):
            st.write(contract1)

ocr2 = st.checkbox("Enable OCR: for reading pdf scanned on image", key="ocr2")
if ocr2:
    contract2, uploaded2 = load_ocr(count)
    count += 1
    if contract1 is not None and contract1 != '':
        with st.expander("See contract text"):
            st.write(contract2)
else:
    contract2, uploaded2 = load_file(count)
    count += 1
    if contract2 is not None and contract2 != '':
        with st.expander("See contract text"):
            st.write(contract2)

option_ques = st.selectbox(
    "Questions:",
    (
        "Above are two contract documents: contract 1 and contract 2. Can you compare their differences based on the elements of the contract 1 and contract 2? Please put the results in a table format.",
        "Above are two contract documents: contract 1 and contract 2. Can you check if there are any inconsistencies in the two contracts? Please put the results in a table."),
    index=0,
    placeholder="Select contact method...",
)

question = st.text_area(
    "Questions:",
    option_ques
)

text1 = "Contract 1:\n" + contract1 + "------" + "Contract 2:\n" + contract2 + "\n Question: " + question
textContract = "Contract 1:\n" + contract1 + "------" + "Contract 2:\n" + contract2

SOCKET_URL = "wss://ws.generative.engine.capgemini.com/"
API_TOKEN = "16zuz9jnWZ7WLRwkIXYtb7TO7igJnBhRadp6fPOj"


def extract_json(response):
    print("Response:", response)
    try:
        # Find the JSON part in the response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1

        # Extract the JSON substring
        json_data = response[json_start:json_end]

        # Load the JSON data to ensure it is valid
        parsed_json = json.loads(json_data)

        # Return the extracted JSON as a dictionary
        return parsed_json
    except (json.JSONDecodeError, ValueError) as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")
        return None


def generate():
    prompt = text1
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
                        "retrievalKwargs": {"topK": 3}
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


if st.button(label="✨ Submit", key=3):
    res = generate()
    re = st.markdown(res)
