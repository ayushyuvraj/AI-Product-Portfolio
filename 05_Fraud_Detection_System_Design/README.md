# 🛡️ Fraud Command Center (FCC) - Dynamic Friction Engine

**Role:** Product Lead | **Tech Stack:** Python (Streamlit), Logic Simulation

## 🚀 The Product Vision
In high-frequency payment environments (UPI/Cards), **Latency is Revenue**. Traditional banking systems rely on binary "Block/Allow" rules that are often hard-coded, leading to high False Positives or delayed fraud response.

This **Fraud Command Center** demonstrates a **"Dynamic Friction" Strategy**:
1.  **Green Zone:** Allow instantly (<200ms).
2.  **Yellow Zone:** Challenge via OTP (Step-Up Auth).
3.  **Red Zone:** Block immediately.

## 🛠️ How to Use This Dashboard
This is a **Functional Prototype** designed to simulate the decision-making logic of a Risk Product Manager.

1.  **Configure Rules:** Use the Sidebar to set "High Value" thresholds.
2.  **Adjust Risk Appetite:** Move the sliders to expand or shrink the "Challenge Zone" (Yellow).
3.  **Simulate Impact:** Watch how the "Revenue Saved via OTP" metric changes. This represents legitimate users who would have been blocked in a legacy system but are saved by our friction strategy.

## 🧠 The Logic (Under the Hood)
- **Trust Scoring:** Simulates a ML model scoring transactions (0-100).
- **Decision Engine:** Applies policy rules in real-time.
- **Architecture Note:** In production, this logic sits on top of **Redis** for <10ms inference, fed by **Kafka** streams.