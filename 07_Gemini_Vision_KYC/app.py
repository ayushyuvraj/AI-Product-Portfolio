import streamlit as st
from PIL import Image
import google.generativeai as genai
import csv
import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Gemini Vision KYC", page_icon="👁️")
st.title("👁️ Gemini Vision KYC Verifier")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔐 Configuration")
    api_key = st.text_input("Enter Google API Key:", type="password")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("API Key Accepted!")
        except Exception as e:
            st.error(f"Invalid Key: {e}")

# --- LOGGING FUNCTION (The MLOps Layer) ---
def log_interaction(verdict, reason, full_response):
    file_exists = os.path.isfile('vision_logs.csv')
    
    with open('vision_logs.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header if new file
        if not file_exists:
            writer.writerow(['Timestamp', 'Verdict', 'Reason_Short', 'Full_AI_Response'])
        
        # Write data
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Sanitize strings to prevent CSV breaking
        clean_response = full_response.replace('\n', ' ').replace('\r', '')[:500] 
        writer.writerow([timestamp, verdict, reason, clean_response])

# --- GUARDRAIL FUNCTION ---
def check_image_safety(image_file):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = """
    You are a Content Safety Filter for a Bank. Analyze this image.
    Strict Policy:
    1. The image MUST contain a document that looks like an ID card.
    2. The image MUST NOT contain explicit, violent, or offensive content.
    Return EXACTLY one word: SAFE or UNSAFE.
    """
    response = model.generate_content([prompt, image_file])
    return response.text.strip()

# --- MAIN LOGIC ---
uploaded_file = st.file_uploader("Upload ID Document", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_column_width=True)

    if st.button("Verify Document"):
        if not api_key:
            st.error("Please enter your Google API Key.")
        else:
            with st.spinner("Running Security Protocols..."):
                try:
                    # 1. GUARDRAIL
                    safety_status = check_image_safety(image)
                    
                    if "UNSAFE" in safety_status:
                        st.error("🚫 Security Block: Image rejected.")
                        log_interaction("BLOCKED", "Safety Guardrail Triggered", "Image flagged as Unsafe/Non-ID")
                    else:
                        # 2. EXTRACTION
                        with st.spinner("Guardrail passed. Analyzing ID..."):
                            model = genai.GenerativeModel('gemini-2.5-flash')
                            
                            extraction_prompt = """
                            Act as a strict Bank KYC Officer. Analyze this image.
                            
                            Output format:
                            VERDICT: [APPROVED / REJECTED]
                            REASON: [Short 1 sentence reason]
                            DETAILS: [Full extraction of Name, ID, DOB]
                            """
                            
                            response = model.generate_content([extraction_prompt, image])
                            text_response = response.text
                            
                            # Display
                            st.subheader("✅ Verification Report")
                            st.markdown(text_response)
                            
                            # Parse for Logging (Simple string parsing)
                            verdict = "UNKNOWN"
                            reason = "N/A"
                            
                            if "APPROVED" in text_response: verdict = "APPROVED"
                            elif "REJECTED" in text_response: verdict = "REJECTED"
                            
                            if "REASON:" in text_response:
                                parts = text_response.split("REASON:")
                                if len(parts) > 1:
                                    reason = parts[1].split("DETAILS:")[0].strip()
                            
                            # Log It
                            log_interaction(verdict, reason, text_response)
                            print("📝 Interaction Logged.")
                            
                except Exception as e:
                    st.error(f"Error: {e}")