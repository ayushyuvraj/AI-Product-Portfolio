# 🛡️ Technical Spec: Real-Time UPI Fraud Detection System

**Author:** Ayush Yuvraj | **Type:** System Design Doc | **Status:** Draft

## 1. Executive Summary
We are designing a low-latency fraud detection engine for UPI transactions. The system must process **5,000 Transactions Per Second (TPS)** and return a `Fraud/Safe` verdict in under **200ms**.

## 2. The Challenge (Constraints)
* **Scale:** 50M daily transactions.
* **Latency:** < 200ms p99 latency (strictly enforced to prevent checkout drops).
* **False Positives:** Must be < 0.1% (Block fraud, not real users).

## 3. High-Level Architecture

### A. Ingestion Layer (The Firehose)
* **Choice:** Apache Kafka.
* **Rationale:** We need an event streaming platform capable of handling burst traffic (e.g., Diwali sales) without losing data.

### B. The Brain (Inference Engine)
* **Architecture:** "Shadow Mode" Deployment.
* **Logic:**
    1.  **Rule Engine (Fast):** Checks basic logic (e.g., "Is amount > ₹1 Lakh?"). Latency: 5ms.
    2.  **ML Model (Slow):** A Random Forest model scoring the probability of fraud based on user history. Latency: 50ms.
* **Trade-off Decision:** We will run the ML model *asynchronously* for low-risk transactions to save time, but *synchronously* for high-value (>₹5k) transactions.

### C. The Memory (Feature Store)
* **Choice:** Redis (In-Memory Database).
* **Rationale:** The model needs to know: *"How many times did Ayush pay in the last 10 minutes?"* We cannot query a slow SQL DB for this. Redis provides sub-millisecond access to these counters.

## 4. Database Schema (Simplified)

| Field | Type | Description |
|:---|:---|:---|
| `transaction_id` | UUID | Unique Key |
| `user_id` | INT | Index Key |
| `risk_score` | FLOAT | 0.0 to 1.0 (Model Output) |
| `verdict` | ENUM | BLOCK / ALLOW / 2FA_CHALLENGE |
| `latency_ms` | INT | Processing time tracking |

## 5. Failure Scenarios & Recovery
* **Scenario:** The ML Model Service goes down.
* **Fallback:** The system automatically defaults to the "Rule Engine Only" mode. Better to let a few frauds slip through than to block all payments (Availability > Consistency).

## 6. Open Questions for Engineering
1.  Should we implement "Geofencing" rules at the Kafka layer or the App layer?
2.  What is the retention policy for the Redis Feature store? (Proposed: 24 hours).