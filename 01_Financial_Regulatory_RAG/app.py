import streamlit as st
import os
from PyPDF2 import PdfReader

# --- IMPORTS ---
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Fintech Compliance Copilot", page_icon="🏦")

# --- HEADER ---
st.title("🏦 Fintech Compliance Copilot")
st.markdown("Upload a banking policy (PDF) to build the AI's knowledge base.")

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        st.success("API Key accepted!")
    else:
        st.warning("Please enter your API Key.")

# --- 1. INGESTION ENGINE (ETL) ---
st.subheader("1. Ingestion Engine")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None and api_key:
    if st.button("Process Document (Build Knowledge Base)"):
        with st.spinner("Processing... Extracting text, Chunking, and Embedding..."):
            try:
                # A. Extract
                pdf_reader = PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # B. Transform
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                chunks = text_splitter.split_text(text)

                # C. Load
                embeddings = OpenAIEmbeddings()
                vector_store = FAISS.from_texts(chunks, embeddings)
                
                # Save to session state
                st.session_state.vector_store = vector_store
                st.success("✅ Knowledge Base Created! You can now chat below.")
                
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()

# --- 2. QUERY ENGINE (MANUAL RAG) ---
st.subheader("2. Regulatory Chat Interface")

if "vector_store" in st.session_state:
    user_question = st.text_input("Ask a question about the document:")
    
    if user_question:
        with st.spinner("Thinking..."):
            try:
                # 1. RETRIEVE: Find the relevant chunks manually
                docs = st.session_state.vector_store.similarity_search(user_question, k=3)
                
                # 2. AUGMENT: Create the prompt with context
                context_text = "\n\n".join([doc.page_content for doc in docs])
                
                prompt = f"""
                You are a Banking Compliance AI. Answer the question based ONLY on the context below.
                
                Context:
                {context_text}
                
                Question: 
                {user_question}
                """
                
                # 3. GENERATE: Send to OpenAI
                llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
                
                # *** FIX: Use invoke() instead of predict() ***
                response = llm.invoke(prompt)
                
                # 4. Display
                st.success("Answer:")
                st.write(response.content) # We print the .content part of the response
                
                # (Optional) Show the sources
                with st.expander("View Source Evidence"):
                    st.write(context_text)
                
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("Please upload and process a document above to unlock the chat.")