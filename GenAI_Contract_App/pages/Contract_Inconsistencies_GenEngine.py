#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Contract_inconsistencies_GenEngine.py
@Time    :   2025/03/20 10:56
@Author  :   Akhli RIOUFFREYT
@Version :   1.0
@Contact :   akhli.riouffreyt@capgemini.com
'''

# here put the import lib
import streamlit as st
from pypdf import PdfReader
import fitz  # PyMuPDF
import websocket
import json
from contextlib import closing
from uuid import uuid4


def header_app():
    st.image("TASC-orange-horizontal-logo.png", width=500, )
    with st.expander("ℹ️ - About this app", expanded=True):
        st.write(
            """     
-   The *Contract_Inconsistencies* app is used to determine if a contract has inconsistencies that do not comply with pre-specified rules and laws.
-   Our app is using Capgemini GenEngine model. 
-   pdf and txt files are accepted by our app, Tick the checkbox OCR to read scanned PDF.
"""
        )
    st.header("Contract Inconsistencies", divider='rainbow')


def load_file(count):
    """Load text from file"""
    uploaded_file = st.file_uploader("Upload Contract:", type=['pdf', 'txt'], key=count)
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
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


def load_ocr(count):
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key=count)
    file_name = " "
    raw_text = " "
    if uploaded_file is not None:
        print(uploaded_file.name)
        file_name = uploaded_file.name
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        # for page_num in range(len(pdf_document)):
        #     page = pdf_document.load_page(page_num)
        # # Convert page to an image
        #     pix = page.get_pixmap()
        #     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        # # Use Tesseract to extract text
        #     page_text = pytesseract.image_to_string(img)
        #     raw_text += page_text + "\n"

        extracted_text = extract_text_from_pdf(pdf_document)
        raw_text = extracted_text
    return raw_text, file_name


header_app()
contract, uploaded = "", ""
count = 0
ocr1 = st.checkbox("Enable OCR: for reading pdf scanned on image", key="ocr1")
if ocr1:
    contract, uploaded = load_ocr(count)
    count += 1
    if contract is not None and contract != '':
        with st.expander("See contract text"):
            st.write(contract)
else:
    contract, uploaded = load_file(count)
    count += 1
    if contract is not None and contract != '':
        with st.expander("See contract text"):
            st.write(contract)

option_rules = st.selectbox(
    "Rules:",
    ("A contract cannot be governed by the laws of more than one country",
     "A contract cannot have multiple insurance clauses"),
    index=0,
    placeholder="Select contact method...",
)

selected_rules = st.text_area(
    "Rules selected or Customized rules:",
    option_rules
)

SOCKET_URL = "wss://ws.generative.engine.capgemini.com/"
API_TOKEN = "Skez00ykD41q9jG3JR3jl4kOY4Fyp4Q6pgKlbJE3"


def generate(user_prompt):
    system_prompt = """Answer the question below based on the contract and the rules provided. Extract the exact full sentence that contains the answer. If the question cannot be answered using the information provided, then answer with “I cannot find the information”"""
    prompt = system_prompt + "\n" + user_prompt
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
            "files": [],
            "modelName": "anthropic.claude-v2",
            "provider": "bedrock",
            "sessionId": str(session_id),
            "workspaceId": "",
            "modelKwargs": {
                "streaming": False,
                "maxTokens": 8192,
                "temperature": 0.7,
                "topP": 0.7
            }
        }
    }
    ws.send(json.dumps(data))


input_prompt = "Contract:\n" + contract + "\n Rules: " + selected_rules + "\n Question: Is this contract compliant with the defined rules?"

if st.button(label="✨ Submit", key=1):
    res = generate(input_prompt)
    show_res = "".join(res)
    re = st.markdown(show_res)
