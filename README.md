#  AI Financial Analysis Assistant

An AI-powered financial analysis assistant built using **LangGraph**, **LangChain**, **Groq Llama 3.3**, and **Streamlit**. The application leverages a **ReAct AI agent** to intelligently invoke financial analysis tools, retrieve live market data from Yahoo Finance, and maintain persistent conversation memory across multiple sessions.

---

##  Features

-  Real-time stock price retrieval
-  5-day stock trend analysis
-  Company valuation metrics
  - Trailing P/E Ratio
  - Forward P/E Ratio
  - Market Capitalization
-  ReAct AI Agent powered by LangGraph
-  Persistent conversation memory using LangGraph + SQLite
-  Multi-session chat support
-  Streaming AI responses
-  Interactive Streamlit interface

---

##  Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| AI Framework | LangGraph, LangChain |
| LLM | Groq (Llama 3.3 70B Versatile) |
| Frontend | Streamlit |
| Financial Data | yfinance (Yahoo Finance) |
| Database | SQLite |
| Memory | LangGraph SqliteSaver |

---

##  System Architecture

```text
                    User
                     │
                     ▼
               Streamlit UI
                     │
                     ▼
        LangGraph ReAct Agent
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
 Financial Analysis Tools      SQLite Memory
      │
      ▼
 Yahoo Finance (yfinance API)
```

---

##  Project Structure

```text
Financial-Analysis-Assistant/
│
├── app.py                         # Streamlit frontend
├── financial_advisor_backend.py   # LangGraph agent & financial tools
├── finance_agent_memory.db        # SQLite conversation memory
├── requirements.txt
├── .env.example
└── README.md
```

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Financial-Analysis-Assistant.git
cd Financial-Analysis-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the application

```bash
streamlit run app.py
```

---

##  Example Queries

- Analyze AAPL
- Show the current price of NVDA
- What is the valuation of TSLA?
- Compare AAPL and MSFT
- Is GOOGL overvalued?
- Show the 5-day trend for META

---

##  How It Works

1. The user submits a financial query through the Streamlit interface.
2. The LangGraph ReAct agent determines whether external financial tools are required.
3. Appropriate tools fetch live market data using Yahoo Finance.
4. The LLM analyzes the retrieved data and generates a natural-language response.
5. Chat history is stored in SQLite using LangGraph's checkpointing mechanism, enabling persistent multi-session conversations.

---

##  Screenshots

### Home Screen

<img width="959" alt="Home" src="https://github.com/user-attachments/assets/a25e7e0d-010f-4d46-941b-23574d06c5bb" />

### Company Valuation

<img width="953" alt="Valuation" src="https://github.com/user-attachments/assets/594580a5-256e-49c4-b49f-2b0246f03f1b" />

### Stock Trend Analysis

<img width="956" alt="Trend Analysis" src="https://github.com/user-attachments/assets/2171c7aa-d47d-4df1-9953-f73c44594794" />

### Persistent Conversation Memory

<img width="959" alt="Memory" src="https://github.com/user-attachments/assets/28bbadde-d457-4ae9-b6ef-9e695d7711f8" />

---

##  Future Improvements

-  Technical indicators (RSI, MACD, SMA)
-  News sentiment analysis
-  Portfolio performance tracking
-  Portfolio risk analysis
-  Interactive stock comparison dashboard
-  PDF investment reports
-  Watchlist management
-  Support for multiple LLM providers

---

##  Key Concepts Demonstrated

- AI Agents with LangGraph
- ReAct Agent Architecture
- Tool Calling
- LLM Integration
- Persistent Memory
- Function Calling
- Streamlit Application Development
- Financial Data Analysis
- SQLite Persistence

---

---

##  Acknowledgements

- LangGraph
- LangChain
- Groq
- Streamlit
- Yahoo Finance (yfinance)
