import sqlite3
import random
from datetime import datetime, timedelta

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('financial_data.db')
cursor = conn.cursor()

# --- 1. CREATE TABLES ---
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    segment TEXT,  -- Retail, Corporate, HNI (High Net-worth)
    risk_score INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    account_type TEXT, -- Savings, Current, Loan
    balance REAL,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    account_id INTEGER,
    date TEXT,
    amount REAL,
    type TEXT, -- Credit, Debit
    category TEXT, -- Utilities, Travel, Investment, Operations
    FOREIGN KEY (account_id) REFERENCES accounts (id)
)
''')

# --- 2. POPULATE WITH DUMMY DATA ---
segments = ['Retail', 'Corporate', 'HNI']
names = ['Amit Sharma', 'Priya Iyer', 'Rahul Verma', 'Sneha Gupta', 'Vikram Singh', 'KPMG Corp', 'Tech Solutions Ltd']
account_types = ['Savings', 'Current', 'Loan']
categories = ['Utilities', 'Travel', 'Investment', 'Operations', 'Salary']

# Create 50 Customers
print("Generating Customers...")
for i in range(1, 51):
    name = random.choice(names) + f" {i}"
    segment = random.choice(segments)
    risk_score = random.randint(300, 900)
    cursor.execute('INSERT INTO customers (name, segment, risk_score) VALUES (?, ?, ?)', (name, segment, risk_score))

# Create Accounts (1-2 per customer)
print("Generating Accounts...")
for i in range(1, 51):
    num_accounts = random.randint(1, 2)
    for _ in range(num_accounts):
        acc_type = random.choice(account_types)
        balance = random.uniform(1000, 1000000)
        cursor.execute('INSERT INTO accounts (customer_id, account_type, balance) VALUES (?, ?, ?)', (i, acc_type, balance))

# Create Transactions
print("Generating Transactions...")
cursor.execute("SELECT id FROM accounts")
account_ids = [row[0] for row in cursor.fetchall()]

for _ in range(500): # 500 random transactions
    acc_id = random.choice(account_ids)
    date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
    amount = random.uniform(100, 50000)
    trans_type = random.choice(['Credit', 'Debit'])
    category = random.choice(categories)
    cursor.execute('INSERT INTO transactions (account_id, date, amount, type, category) VALUES (?, ?, ?, ?, ?)', 
                   (acc_id, date, amount, trans_type, category))

# Commit and Close
conn.commit()
conn.close()
print("✅ Database 'financial_data.db' created successfully with dummy data.")