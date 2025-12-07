# 🛡️ Qubic Guardian — Real-Time On-Chain Risk & Anomaly Detection System
### AI-powered transaction monitoring with EasyConnect → n8n → Google Sheets → Streamlit → Telegram Alerts

## 🚀 Overview
Qubic Guardian is an AI-driven real-time on-chain monitoring system built for the Qubic ecosystem.

It continuously:
- Listens to live QX asset trades  
- Enriches trades with real-time price data  
- Performs anomaly detection  
- Assigns risk scores + tags  
- Stores clean data in Google Sheets  
- Sends Telegram alerts for high-risk events  
- Updates a real-time Streamlit dashboard  

This system emulates exchange-grade surveillance engines, but using decentralized Qubic data + AI.

---

## 🔍 What Qubic Guardian Detects
- **Suspicious Transactions**
- **Whale Movements**
- **Token-Specific Trading Behavior**
- **Category-Level Risks**
- **Liquidity Anomalies**
- **Historic & Real-Time Trends**

---

## 🧠 Key Features

### 1️⃣ Real-Time Transaction Ingestion
- QX trades are streamed through **Qubic EasyConnect Webhooks**.
- Every trade instantly flows into **n8n** for processing.

---

### 2️⃣ Live Price Enrichment
- Uses **MEXC QUBIC/USDT price API** to calculate real USD impact.
- Enables accurate **risk scoring** based on trade size and value.

---

### 3️⃣ AI-Powered Summaries
LLM (Gemini 2 Flash / DeepSeek / Groq) generates:
- Human-readable explanation  
- Risk interpretation  
- Recommendation: **Monitor / Caution / Urgent**

---

### 4️⃣ Multi-Layer Risk Engine

#### **A. Base Risk (Features & Risk Node)**
Risk based on `trade_value_usdt`:
- **< $50 → LOW**
- **$50–$500 → MEDIUM**
- **> $500 → HIGH**

#### **B. Anomaly Detection Engine**
Analyzes multiple signals:
- Trade size  
- Shares  
- Whale thresholds  
- Illiquid assets  
- New / experimental tokens  
- Selling pressure  
- Price/volume irregularities  
- Other rule-based anomaly flags  

Outputs:
- `risk_score_anamoly`  
- `risk_level_anamoly`  
- `risk_tags_anamoly` (comma-separated)

---

### 5️⃣ Structured Transaction Logging
Every transaction entry stored in **Google Sheets**, including:
- Raw trade values  
- QUBIC price + USDT conversion  
- Risk levels (base + anomaly)  
- AI summary  
- Anomaly tags  
- Timestamp  
- TxID  

This acts as the **data warehouse** for the dashboard.

---

### 6️⃣ Telegram Alerts

- Risk Level
- Risk Score
- Asset   
- Shares
- Trade Value
- TxID
- AI-generated summary  

---

### 7️⃣ Live Analytics Dashboard (Streamlit)
Professional dashboard featuring:
- Filterable transaction table  
- Risk distribution  
- Token performance  
- Whale movements  
- Real-time synced updates  
- Category-level trends  
- Anomaly tag distribution  
- Top high-risk transactions  
- Historical time-series data  

Data refreshes through a **lightweight n8n API route**.

---
## 🏗️ Architecture

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/73993afc-a481-43a7-a474-68abc9423a5a" />


## 🛑 Why This System Matters

This system solves real-world, high-value problems in crypto trading:

- Detects abnormalities before they turn into exploits  
- Warns users of suspicious wallet behavior  
- Monitors high-risk assets  
- Identifies whales and market manipulation  
- Provides easy-to-understand summaries for non-technical users  

No exchange or trader wants to manually monitor hundreds of trades.  
**This system automates all of it.**

---

## ⚙️ Technical Stack

### **Data Ingestion**
- Qubic EasyConnect Webhooks  
- n8n automation engine  

### **Data Enrichment**
- MEXC QUBIC/USDT Price API  

### **AI Engine**
- Gemini 2 Flash / DeepSeek / Groq LLM  
- Configurable inside n8n  

### **Storage**
- Google Sheets (lightweight warehouse)

### **Analytics Layer**
- Streamlit  
- pandas  
- Plotly  

### **Alerting**
- Telegram Bot API  

---

## 🖥️ Dashboard 

### 📌 Page 1 — Real-Time Transaction Monitor

This page displays the live trade feed coming directly from the **Qubic EasyConnect → n8n** pipeline.

### **Key Features**
- Live transaction table  
- Base + Anomaly risk score  
- AI summary insights  
- Whale detection badges  
- Category & asset filters  
- Trade direction + value breakdown  
- Auto-refresh enabled  

<img width="1920" height="1779" alt="page1_realtime" src="https://github.com/user-attachments/assets/250f4831-fe73-48af-9bbd-e17452f505c7" />

---

### 📌 Page 2 — Risk Analytics & Distribution

This page provides a complete breakdown of **risk levels** across the Qubic ecosystem.

### **Key Features**
- Risk distribution charts  
- Category-wise risk bar charts  
- Asset-level risk concentration  
- Anomaly tag frequency analysis  
- High-risk transaction leaderboard  

<img width="1920" height="1814" alt="page2_risk_analytics" src="https://github.com/user-attachments/assets/732dcd3e-b978-4f93-8735-e57c4676c055" />

---

### 📌 Page 3 — Whale Movements & Token Behavior

This page focuses on large trades, major market movers, and token-level behavioral patterns.

### **Key Features**
- Whale buy/sell tracking  
- Token-wise volume & volatility analysis  
- Top whale-impacted assets  
- Price × volume correlations  
- Suspicious directional patterns  

<img width="1920" height="2529" alt="page3_whales" src="https://github.com/user-attachments/assets/668c7b65-b662-48a4-8e9b-288011170a6c" />

---

### 📌 Page 4 — Historical Trends & Category Insights

This page offers deeper historical and aggregated ecosystem intelligence.

### **Key Features**
- Daily / hourly trend charts  
- Category activity timelines  
- Historical anomaly frequency  
- Asset performance over time  
- Liquidity fluctuation monitoring  

<img width="1920" height="1330" alt="page4_historical" src="https://github.com/user-attachments/assets/3f0497b8-2c95-41a1-8de6-e58a40aeaa3a" />

---

**Live Dashboard:**  
🔗 https://qubic-guardian-dashboardgit-xqfe2bufpxkqdcm99mqn22.streamlit.app/

---

## 🧩 Risk Logic Details

### **Base Risk**
` bash
LOW: trade_value_usdt < 50
MEDIUM: 50 <= trade_value_usdt < 500
HIGH: trade_value_usdt >= 500
`

### **Anomaly Tags (Examples)**
- very_large  
- whale_shares  
- illiquid_category  
- high_sell_pressure  
- new_token  
- suspicious_direction_pattern  

### **Composite Risk**
risk_score_final = base_score + anomaly_score
risk_level_final = derived from risk_score_final

---

## 📡 API Endpoint (via n8n)
GET /webhook/qx-dashboard

Returns full JSON dataset for Streamlit.

---

## 📱 Telegram Alert Format

Alert:

<img width="717" height="600" alt="image" src="https://github.com/user-attachments/assets/b31f4294-6cba-4430-bd05-20497231ed7e" />



---

## 🧪 Testing

You can test the system by POSTing JSON to the incoming webhook:


### **Sample Payload**
```json
{
  "AssetName": "QXTRADE",
  "NumberOfShares": 5000000,
  "Price": 3,
  "RawTransaction": { 
    "transaction": { 
      "txId": "sample-tx" 
    } 
  }
}
```

## 💡 Summary

**Qubic Guardian** is a full-stack real-time risk monitoring system that combines:

- On-chain data  
- Off-chain market feeds  
- Automated risk rules  
- AI reasoning  
- Interactive Streamlit analytics  
- Instant Telegram alerts  

It delivers **exchange-grade intelligence** for Qubic traders, developers, and governance teams.

