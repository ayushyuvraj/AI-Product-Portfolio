import streamlit as st
import os
import csv
import datetime
from PyPDF2 import PdfReader

# --- IMPORTS ---
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI

# --- PAGE CONFIG ---
st.set_page_config(page_title="Fintech Compliance Copilot", page_icon="🏦")
st.title("🏦 Fintech Compliance Copilot")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key

# --- LOGGING FUNCTION ---
def log_interaction(question, answer, context):
    file_exists = os.path.isfile('interaction_logs.csv')
    with open('interaction_logs.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Question', 'Answer', 'Context'])
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, question, answer, context])

# --- GUARDRAIL FUNCTION (The Safety Layer) ---
def check_safety(question):
    """
    Returns 'SAFE' if the question is compliant.
    Returns a 'BLOCK_REASON' if it violates policy.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    safety_prompt = f"""
    You are a Security Guard for a Banking AI.
    Your job is to screen user questions for 'Toxic' or 'Illegal' content.
    
    Policy:
    1. BLOCK requests for illegal acts (money laundering, fraud).
    2. BLOCK requests for specific investment advice (e.g., "buy this stock").
    3. BLOCK hate speech or profanity.
    4. ALLOW questions about banking regulations, policies, and definitions.
    
    Question: "{question}"
    
    If the question is safe, return word: SAFE
    If unsafe, return a short reason why (e.g., "Illegal Activity Detected").
    """
    
    response = llm.invoke(safety_prompt).content.strip()
    return response

# --- 1. INGESTION ENGINE ---
st.subheader("1. Ingestion Engine")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and api_key:
    if st.button("Process Document"):
        with st.spinner("Processing..."):
            pdf_reader = PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
            chunks = text_splitter.split_text(text)
            
            embeddings = OpenAIEmbeddings()
            vector_store = FAISS.from_texts(chunks, embeddings)
            st.session_state.vector_store = vector_store
            st.success("✅ Knowledge Base Created!")

st.divider()

# --- 2. SECURE QUERY ENGINE ---
st.subheader("2. Regulatory Chat Interface")

if "vector_store" in st.session_state:
    user_question = st.text_input("Ask a question about the document:")
    
    if user_question:
        with st.spinner("Running Security Checks..."):
            
            # A. GUARDRAIL CHECK
            safety_status = check_safety(user_question)
            
            if safety_status == "SAFE":
                with st.spinner("Retrieving Answer..."):
                    # B. Retrieve
                    docs = st.session_state.vector_store.similarity_search(user_question, k=3)
                    context_text = "\n\n".join([doc.page_content for doc in docs])
                    
                    # C. Generate
                    prompt = f"""
                    You are a Banking Compliance AI. Answer based ONLY on the context below.
                    
                    Context:
                    {context_text}
                    
                    Question: 
                    {user_question}
                    """
                    
                    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
                    response = llm.invoke(prompt)
                    
                    # D. Display & Log
                    st.success("Answer:")
                    st.write(response.content)
                    log_interaction(user_question, response.content, context_text)
            
            else:
                # E. BLOCK ACTION
                st.error(f"🚫 Request Blocked: {safety_status}")
                st.warning("Our AI Safety Policy prevents answering queries related to illegal activities or financial advice.")
                # We log the blockage too
                log_interaction(user_question, f"BLOCKED: {safety_status}", "N/A")