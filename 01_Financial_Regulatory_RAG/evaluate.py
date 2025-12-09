import os
import pandas as pd
from langchain_community.chat_models import ChatOpenAI

# --- 1. SECURITY & SETUP ---
if "OPENAI_API_KEY" not in os.environ:
    print("🔑 Authentication Required")
    user_key = input("Enter your OpenAI API Key: ").strip()
    os.environ["OPENAI_API_KEY"] = user_key

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# --- 2. LOAD REAL LOGS ---
log_file = 'interaction_logs.csv'
if not os.path.exists(log_file):
    print("❌ No logs found! Run the app and ask questions first.")
    exit()

print(f"📂 Loading logs from {log_file}...")
df_logs = pd.read_csv(log_file)

# --- 3. DEFINE THE METRICS (The Logic) ---

def evaluate_faithfulness(answer, context):
    """
    Metric 1: Faithfulness (Hallucination Check)
    Does the answer contain information NOT present in the context?
    0 = Hallucinated (Lied). 1 = Faithful (Truth).
    """
    prompt = f"""
    You are a Fact-Checking AI. 
    Task: Compare the 'Actual Answer' against the 'Source Context'.
    
    Source Context:
    {context}
    
    Actual Answer:
    {answer}
    
    Determination:
    - If the answer contains ANY claims that are not supported by the context, return 0.
    - If the answer is fully supported by the context, return 1.
    
    Return ONLY the number (0 or 1).
    """
    score = llm.invoke(prompt).content
    return int(score) if score.strip() in ['0', '1'] else 0

def evaluate_relevance(question, answer):
    """
    Metric 2: Answer Relevance (Utility Check)
    Does the answer actually address the user's question?
    0 = Irrelevant/Dodge. 1 = Relevant.
    """
    prompt = f"""
    You are a Teacher grading an exam.
    Task: Determine if the 'Actual Answer' answers the 'Student Question'.
    
    Student Question:
    {question}
    
    Actual Answer:
    {answer}
    
    Determination:
    - If the answer ignores the question or is unhelpful, return 0.
    - If the answer addresses the core of the question, return 1.
    
    Return ONLY the number (0 or 1).
    """
    score = llm.invoke(prompt).content
    return int(score) if score.strip() in ['0', '1'] else 0

# --- 4. EXECUTION LOOP ---
print(f"🕵️  Grading {len(df_logs)} interactions on Faithfulness & Relevance...\n")
results = []

for index, row in df_logs.iterrows():
    question = row['Question']
    answer = row['Answer']
    context = row['Context']
    
    print(f"Processing Q{index+1}: {question[:50]}...")
    
    # Run Metric 1
    faith_score = evaluate_faithfulness(answer, context)
    
    # Run Metric 2
    rel_score = evaluate_relevance(question, answer)
    
    results.append({
        "Question": question,
        "Faithfulness_Score": faith_score, # 0 or 1
        "Relevance_Score": rel_score,      # 0 or 1
        "Answer": answer
    })

# --- 5. REPORTING ---
df_results = pd.DataFrame(results)

# Calculate Averages
avg_faith = df_results['Faithfulness_Score'].mean()
avg_rel = df_results['Relevance_Score'].mean()

print("\n📊 --- DETAILED QUALITY REPORT ---")
print(f"Overall Faithfulness: {avg_faith:.2f} (Target: >0.9)")
print(f"Overall Relevance:    {avg_rel:.2f} (Target: >0.8)")
print("-" * 30)
print(df_results[["Question", "Faithfulness_Score", "Relevance_Score"]])

df_results.to_csv("detailed_eval_report.csv", index=False)
print("\n✅ Report saved to 'detailed_eval_report.csv'")