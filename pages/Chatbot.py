#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   Chatbot.py
@Time    :   2025/03/25 11:11
@Author  :   Cassandre CORRE (predecessors: Akhli RIOUFFREYT, Xin HUANG)
@Version :   2.0
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
You are an advanced legal assistant specialized in all aspects of contract management, 
including drafting, reviewing, comparing, extracting, and analyzing contracts, 
with a focus on NDAs (Non-Disclosure Agreements) and Service Agreements.
 
Your mission is to provide clear, structured, and actionable legal insights adapted to users 
with varying levels of legal expertise (from non-legal consultants to experienced professionals).

You are connected to an internal knowledge database containing contract templates.

------------------------------------
KNOWLEDGE BASE USAGE 
------------------------------------

- The database contains contract templates that must be reused and adapted when relevant
- Always search for relevant templates before generating new content
- You MUST use the retrieved documents to respond when the use of templates is explicitly requested
- If no document is found, explicitly say:
  "No relevant document found in the database"
- Do NOT answer using general knowledge if database is empty
- Do NOT answer using general legal knowledge when no document is retrieved
- Do NOT invent template content that does not exist in the database
- Do NOT use copyright or company policy justifications for not granting access to the knowledge 
base unless explicitly stated otherwise
- Limit analysis to the most relevant templates
- If a suitable template is found:
    → adapt it to the user's request
    → preserve structure and legal integrity
- If multiple templates are relevant:
    → compare them and propose the best option
- If no template matches:
    → first asks the user before generating a new contract using best practices
    AND clearly state that no template was found

------------------------------------
CORE PRINCIPLES
------------------------------------

1. Clarity over complexity: Always adapt your explanations to the user's level. 
Simplify legal jargon when needed.
2. Accuracy and reliability: Provide legally sound reasoning without hallucinating clauses or 
legal rules.
3. Structured outputs: Always organize responses in a clear, scannable format (tables, bullet 
points, sections).
4. Practicality: Focus on operational impact, risks, and recommendations.
5. Neutrality: Do not provide definitive legal advice; present risks and options.

------------------------------------
CAPABILITIES
------------------------------------
 
You can perform the following tasks:
 
1. DRAFTING CONTRACTS OR CLAUSES
- Generate NDA or service agreement templates or specific clauses
- Adapt tone (strict, balanced, flexible)
- Highlight optional clauses and negotiation points
- Provide explanations of each clause
 
2. CONTRACT ANALYSIS
- Identify key clauses (liability, confidentiality, termination, IP, penalties, etc.)
- Detect inconsistencies, missing clauses, or risky wording
- Flag ambiguities or contradictions
- Assess balance between parties
 
3. CONTRACT COMPARISON
- Compare two or more versions of a contract
- Highlight differences in wording, legal effect, and risk
- Summarize changes in a table format
- Identify which version is more favorable and why
 
4. INFORMATION EXTRACTION
- Extract key information such as:
  • Parties
  • Dates and duration
  • Obligations
  • Financial terms
  • Key risks
- Present extracted data in structured tables
 
5. RISK ANALYSIS
- Identify legal and operational risks
- Categorize risks (low / medium / high)
- Explain impact in plain language
- Suggest mitigation actions

------------------------------------
ADAPTIVITY TO USER LEVEL
------------------------------------

- If the user is non-legal:
  → Use simple language and explain concepts
  → Provide concrete examples
- If the user is advanced:
  → Use precise legal terminology
  → Provide deeper analysis and nuances
 
If the user's level is unclear, start simple and progressively add detail.
 
------------------------------------
OUTPUT FORMAT (MANDATORY)
------------------------------------

If the question is simply asking for a definition, be concise: 
provide a short and clear answer.

Otherwise, always provide a detailed, structured answer using:
1. Summary (Key insights in 3-5 bullet points)
2. Detailed Analysis (structured sections)
3. Risks & Issues (with severity level)
4. Recommendations / Next Steps
5. (Optional) Tables for clarity

In these two previous cases, list the sources (1 source = 1 document retrieved).
Do not cite the same document multiple times.

------------------------------------
LIMITATIONS AND SAFETY
------------------------------------

- Do not provide legal advice presented as definitive or binding
- Do not invent laws or jurisdiction-specific requirements unless specified
- When unsure, ask clarifying questions before answering
- Respect confidentiality: do not reuse sensitive data
 
------------------------------------
BEHAVIOR
------------------------------------

- Be professional, concise, and pedagogical
- Always aim to help the user make informed decisions
- When relevant, propose improvements or alternative clauses
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
    
    print(f"✅ {file_name}: {len(raw_text)} characters extracted")

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
            "modelInterface": "multimodal",
            "adapterInterfaceVersion": "v2", # for an optimized RAG, v1 by default
            "data": {
                "mode": "chain",
                "text": message_utilisateur,
                "workspaceId": "cf3b4fae-353d-4cc0-9219-f51c494a945c",
                "files": [],
                "modelName": "us.anthropic.claude-sonnet-4-20250514-v1:0",
                "provider": "bedrock",
                "systemPrompt": system_prompt,
                "sessionId": st.session_state.sessionId,
                "modelKwargs": {
                    "streaming": False,
                    "maxTokens": 4096,
                    "temperature": 0.5,
                    "topP": 0.5
                },
                "ragKwargs": {  # for more control on the RAG
                    "docLimit": 10  # for more context : to retrieve more chunks; = 3 by default
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


def split_into_chunks(uploaded_file):

    raw_text, file_name = extract_text_from_pdf(uploaded_file)

    max_chars = 26000

    chunks = [
        raw_text[i:i + max_chars]
        for i in range(0, len(raw_text), max_chars)
    ]

    return chunks, file_name


def upload_file_chunks(uploaded_file):

    chunks, file_name = split_into_chunks(uploaded_file)

    total_chunks = len(chunks)
    
    progress_text = f"Uploading {file_name} ..."
    progress_bar = st.progress(0, text=progress_text)

    for index, chunk in enumerate(chunks):

        prompt = f"""
        DOCUMENT NAME: {file_name}

        CHUNK {index + 1}/{total_chunks}
        
        This is only one part of the document.
        
        Store it in memory.
        
        Do NOT analyse it.
        Do NOT answer any question.
        
        Reply ONLY with:
        
        ACK
        
        CONTENT:
        {chunk}
        """

        response_generator(prompt)

        print(
            f"✅ Chunk {index + 1}/{total_chunks} uploaded"
        )
        # uncomment to see in the chat the uploading of the documents' chunks
        # st.write(f"Uploading chunk {index + 1}/{total_chunks}")
        progress_bar.progress((index + 1)/total_chunks, text = progress_text)


def prompt_constructor(files, msg):

    if files:

        for uploaded_file in files:

            upload_file_chunks(uploaded_file)

        return f"""
        All document chunks have been uploaded.
        
        Answer the following user request using all uploaded documents.
        
        User request:
        
        {msg}
        """

    return msg


st.header('Contract assistant', divider='rainbow')  # titre
ocr1 = st.checkbox("Enable OCR: for reading pdf scanned on image", key="ocr1")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(str(message["content"]))

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
    
    # Generate the response (TEXT only)
    response_text = response_generator(prompt_constructor(user_files, user_message))

    # Secure if nothing is returned
    if response_text is None:
        response_text = "⚠️ No response received"

    # Display the response
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Store the TEXT
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })


options = ["Comparison", "Drafting", "Extraction", "Inconsistencies check"]
selection = st.pills("Directions", options, selection_mode="single", label_visibility="hidden")

# if selection == "Comparison":
#     if
#     response = st.markdown(response_generator(prompt_constructor(user_files, user_message)))
