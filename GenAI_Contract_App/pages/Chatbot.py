#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   Chatbot.py
@Time    :   2025/03/25 11:11
@Author  :   Akhli RIOUFFREYT
@Version :   1.0
@Contact :   akhli.riouffreyt@capgemini.com
"""

import streamlit as st
import websocket
import json
from contextlib import closing
from uuid import uuid4
from pypdf import PdfReader
import fitz


def header_app():
    st.image("TASC-orange-horizontal-logo.png", width=500, )
    with st.expander("ℹ️ - About this app", expanded=True):
        st.write(
            """     
-   The *Contract assistant* app is used to answer questions relative to any contract.
-   Our assistant can perform the following tasks:
      - Compare contracts
      - Draft contracts
      - Extract specific information from a contract
      - Look for inconsistencies (if any) in a contract
       
-   Our app is using Capgemini Generative engine.
"""
        )


header_app()

SOCKET_URL = "wss://ws.generative.engine.capgemini.com/"
API_TOKEN = "16zuz9jnWZ7WLRwkIXYtb7TO7igJnBhRadp6fPOj"

# system prompt of the chatbot utilisé dans la fonction send_query
system_prompt = """
You are a Senior Contract Manager at a leading tech company. 
Your role involves overseeing all aspects of contract management, including drafting, reviewing, negotiating, and ensuring compliance with contractual agreements. 
You have extensive knowledge of contract law, industry standards, and best practices in contract management.

Your task is to assist users by answering their questions related to contract management. 
You can provide detailed explanations, offer guidance on specific contract issues, and share insights on best practices. 
You are knowledgeable, professional, and approachable, ensuring users feel supported and informed.

Capabilities:
General Contract Management: Explain the principles and processes involved in contract management, including drafting, reviewing, negotiating, and compliance.
Specific Contract Issues: Provide detailed answers to questions about particular contracts, including terms, conditions, and potential issues.
Best Practices: Share industry standards and best practices for effective contract management.
Legal Insights: Offer insights into contract law and how it applies to various scenarios.
Problem-Solving: Help users troubleshoot and resolve contract-related problems.

Tone and Style:
Professional: Maintain a professional and knowledgeable tone.
Approachable: Be friendly and easy to understand, ensuring users feel comfortable asking questions.
Supportive: Offer support and guidance, validating users' concerns and providing clear, actionable advice.
Detailed: Provide thorough and detailed responses to ensure users have a comprehensive understanding of contract management.

Example Interactions:
1 - General Question:
User: "What are the key elements of a contract?"
LLM: "A contract typically includes key elements such as the offer, acceptance, consideration, mutual consent, and legality. Each element plays a crucial role in forming a legally binding agreement."

2 - Specific Issue:
User: "I'm having trouble with a clause in my contract regarding termination. Can you help?"
LLM: "Certainly. Termination clauses outline the conditions under which a contract can be ended. It's important to review the specific language and understand the rights and obligations of both parties. If you provide more details, I can offer more specific guidance."

3 - Best Practices:
User: "What are some best practices for negotiating contracts?"
LLM: "Effective contract negotiation involves clear communication, understanding the needs and priorities of both parties, being prepared with relevant information, and aiming for a mutually beneficial agreement. It's also important to document all changes and agreements thoroughly."

IMPORTANT: when comparing several contracts, provide the answer in a table format.
"""

# Initialize sessionId as a session state variable to preserve context in GenEngine
if "sessionId" not in st.session_state:
    st.session_state.sessionId = str(uuid4())


def extract_text_from_pdf_ocr(pdf_document):
    """for OCR"""
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text


def extract_text_from_pdf(uploaded_file):
    if (uploaded_file is not None) and ocr1:
        file_name = uploaded_file.name
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        extracted_text = extract_text_from_pdf_ocr(pdf_document)
        raw_text = extracted_text
        return raw_text, file_name
    else:
        if uploaded_file is not None:
            file_name = uploaded_file.name
            if uploaded_file.type == "text/plain":
                raw_text = str(uploaded_file.read(),"utf-8")
            elif uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                raw_text = text

        return raw_text, file_name


def extract_text_from_multiple_files(uploaded_files):
    """
    extract text from multiple files and return a list of file text
    """
    files_text = []

    # Create a progress bar
    progress_text = "extracting files content..."
    progress_bar = st.progress(0)

    total_files = len(uploaded_files)
    for i, uploaded_file in enumerate(uploaded_files):
        # Update progress
        progress_bar.progress(i / total_files)
        st.write(f"extracting content of {uploaded_file.name}")

        # Extract the content
        file_content, file_name = extract_text_from_pdf(uploaded_file)
        print(f"file name: {file_name}")
        if file_name:
            files_text.append({
                'content': file_content,
                'name': file_name
            })
            st.write(f"✅ {uploaded_file.name} content extracted successfully")
        else:
            st.error(f"❌ Failed to extract content from {uploaded_file.name}")

    # Complete the progress bar
    progress_bar.progress(1.0)

    return files_text


def send_query(ws, message_utilisateur):
    data = {
            "action": "run",
            "modelInterface": "langchain",
            "data": {
                "mode": "chain",
                "text": message_utilisateur,
                "files": [],
                "modelName": "anthropic.claude-v2",
                "provider": "bedrock",
                "systemPrompt": system_prompt,
                "sessionId": st.session_state.sessionId,
                "workspaceId": "",
                "modelKwargs": {
                    "streaming": False,
                    "maxTokens": 4096,
                    "temperature": 0.5,
                    "topP": 0.5
                }
            }
        }
    ws.send(json.dumps(data))


def response_generator(prompt_to_send):
    print("Input prompt:", prompt_to_send)
    url = SOCKET_URL
    with closing(websocket.create_connection(url, header={"x-api-key": API_TOKEN})) as ws:
        try:
            send_query(ws, prompt_to_send)
        except Exception as e:
            print(f"Une erreur inattendue est survenue dans la fonction send_query : {e}")
        generated_response = None
        while generated_response is None:
            try:
                generated_message = ws.recv()
                print(generated_message)
                generated_message = json.loads(generated_message)
                action = generated_message.get("action")
                if "final_response" == action:
                    generated_response = generated_message.get("data", {}).get("content")
            except json.JSONDecodeError:
                print(f"Error parsing generated message: {generated_message}")
                break
    return generated_response


def prompt_constructor(files, msg):
    if files:
        files_content = extract_text_from_multiple_files(files)
        for i, file in enumerate(files_content):
            user_prompt = msg + f"\ncontract n°{i} called " + file["name"] + "\n" + file["content"]
            # Add user file to file history
            st.session_state.files.append(file)
        return user_prompt
    else:
        return msg


st.header('Contract assistant', divider='rainbow')  # titre
ocr1 = st.checkbox("Enable OCR: for reading pdf scanned on image", key="ocr1")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize files history
if "files" not in st.session_state:
    st.session_state.files = []

# React to user input
if prompt := st.chat_input("How can I help you?", accept_file="multiple"):
    user_message, user_files = prompt["text"], prompt["files"]
    if user_message is None:
            response = st.markdown(response_generator("hello, "))
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_message)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_message})
    # Display assistant response in chat message container
    response = st.markdown(response_generator(prompt_constructor(user_files, user_message)))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

options = ["Comparison", "Drafting", "Extraction", "Inconsistencies check"]
selection = st.pills("Directions", options, selection_mode="single", label_visibility="hidden")

# if selection == "Comparison":
#     if
#     response = st.markdown(response_generator(prompt_constructor(user_files, user_message)))
