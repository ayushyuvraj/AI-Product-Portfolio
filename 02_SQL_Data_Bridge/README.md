# 📊 AI Data Analyst (Text-to-SQL Agent)

**A LangChain-powered Agent that translates natural language questions into SQL queries, enabling non-technical stakeholders to query databases instantly.**

## 🚀 The Business Problem
Data teams are often bottlenecked by ad-hoc reporting requests ("How many users signed up last week?", "What is the average transaction size?"). This project solves that by creating a **Self-Serve Analytics Interface** where managers can ask questions in plain English and get data-backed answers immediately.

## 🛠️ Technical Architecture
* **Orchestration:** LangChain (`create_sql_agent`).
* **LLM:** GPT-3.5 Turbo (via OpenAI API).
* **Database:** SQLite (Relational DB) with a schema mimicking a Banking Ledger (Customers, Accounts, Transactions).
* **Agentic Reasoning:** The AI inspects the database schema first, generates a valid SQL query, executes it, and synthesizes the result.

## ⚠️ Safety & Governance
* **Read-Only Access:** In a production environment, this agent would be restricted to a read-only database user to prevent `DROP TABLE` or injection attacks.
* **Schema Limiting:** The agent is only exposed to specific tables (`customers`, `accounts`, `transactions`) to ensure privacy.

## ⚙️ Setup & Usage
1.  **Navigate to the folder:**
    ```bash
    cd 02_SQL_Data_Bridge
    ```
2.  **Install Requirements:**
    ```bash
    pip install langchain-experimental sqlalchemy
    ```
3.  **Generate Dummy Data:**
    ```bash
    python create_db.py
    ```
4.  **Run the Analyst:**
    ```bash
    streamlit run app.py
    ```