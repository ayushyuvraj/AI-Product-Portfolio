import streamlit as st
import os
import sqlite3
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Data Analyst", page_icon="📊")

st.title("📊 AI Data Analyst (Text-to-SQL)")
st.markdown("Ask questions about your database in plain English. No SQL knowledge required.")

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter OpenAI API Key:", type="password")
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        st.success("API Key accepted!")
    else:
        st.warning("Please enter your API Key.")

# --- 1. CONNECT TO DATABASE ---
# We connect to the SQLite DB we just created
db_path = "financial_data.db"

if os.path.exists(db_path) and api_key:
    
    # Initialize LangChain Database connector
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    
    st.info("✅ Connected to 'financial_data.db'")
    
    # --- 2. DEFINE THE AI AGENT ---
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # This 'agent' is a specialized bot that knows how to write SQL
    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="openai-tools",
        verbose=True
    )
    
    # --- 3. CHAT INTERFACE ---
    user_question = st.text_input("Ask a question (e.g., 'Total balance of all Corporate customers?')")
    
    if user_question:
        with st.spinner("Analyzing Database Schema & Writing SQL..."):
            try:
                # The agent thinks, writes SQL, runs it, and explains the result
                response = agent_executor.invoke(user_question)
                st.success("Answer:")
                st.write(response['output'])
                
            except Exception as e:
                st.error(f"Error: {e}")

elif not os.path.exists(db_path):
    st.error("❌ Database file 'financial_data.db' not found. Please run 'create_db.py' first.")