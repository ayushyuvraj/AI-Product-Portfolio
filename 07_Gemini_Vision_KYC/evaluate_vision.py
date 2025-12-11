import google.generativeai as genai
import os
import pandas as pd
import time

# --- 1. SETUP ---
if "GOOGLE_API_KEY" not in os.environ:
    print("🔑 Authentication Required")
    user_key = input("Enter your Google API Key: ").strip()
    genai.configure(api_key=user_key)
else:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. LOAD LOGS ---
log_file = 'vision_logs.csv'
if not os.path.exists(log_file):
    print("❌ No logs found! Please run the app and verify some images first.")
    exit()

print(f"📂 Loading logs from {log_file}...")
df_logs = pd.read_csv(log_file)
print(f"Found {len(df_logs)} interactions to audit.\n")

# --- 3. EVALUATION LOGIC (The "Consistency Check") ---
results = []

print("🕵️  Starting Logical Consistency Audit...")

for index, row in df_logs.iterrows():
    verdict = row['Verdict']
    reason = row['Reason_Short']
    full_text = row['Full_AI_Response']
    
    print(f"Auditing Case #{index+1} ({verdict})...")
    
    # We ask Gemini to act as a 'Supervisor' checking the 'Junior Officer's' work
    # Since we don't have the image, we check if the TEXT reasoning supports the VERDICT.
    audit_prompt = f"""
    You are a Quality Assurance Auditor.
    Review this log entry from an automated KYC AI.
    
    The AI's Verdict: {verdict}
    The AI's Reason: {reason}
    The Full Output: {full_text}
    
    Your Task: Check for LOGICAL CONSISTENCY.
    1. If Verdict is APPROVED, does the output contain extracted data (Name/ID)?
    2. If Verdict is REJECTED, is the reason valid (e.g., Blur, Glare)?
    3. Is there a contradiction? (e.g., Verdict Approved but reason says "Image is blurry")
    
    Output exactly one digit:
    1 = Logic is Consistent/Pass
    0 = Logic is Contradictory/Fail
    """
    
    try:
        response = model.generate_content(audit_prompt)
        score = int(response.text.strip())
    except:
        score = 0
        
    results.append({
        "Timestamp": row['Timestamp'],
        "Original_Verdict": verdict,
        "Logic_Consistency_Score": score
    })
    time.sleep(1) # Rate limit safety

# --- 4. REPORTING ---
df_results = pd.DataFrame(results)
print("\n📊 --- VISION CONSISTENCY REPORT ---")
print(df_results)

df_results.to_csv("vision_audit_report.csv", index=False)
print("\n✅ Audit Complete. Saved to 'vision_audit_report.csv'")