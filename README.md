# 💹 AI Financial Analysis Assistant

An AI-powered financial analysis assistant built using **LangGraph**, **LangChain**, **Groq Llama 3.3**, and **Streamlit**. The application provides real-time stock insights by combining live market data with an intelligent ReAct agent capable of invoking financial analysis tools and maintaining persistent conversation memory.

---

## 🚀 Features

- 📈 Real-time stock price retrieval
- 📊 5-day stock trend analysis
- 💰 Company valuation metrics
  - Trailing P/E Ratio
  - Forward P/E Ratio
  - Market Capitalization
- 🤖 ReAct AI Agent powered by LangGraph
- 🧠 Persistent chat memory using SQLite
- 💬 Multi-session conversation support
- ⚡ Streaming AI responses
- 🎨 Interactive Streamlit interface

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| AI Framework | LangGraph, LangChain |
| LLM | Groq (Llama 3.3 70B Versatile) |
| Frontend | Streamlit |
| Financial Data | yfinance |
| Database | SQLite |
| Language | Python |

---

## 🏗️ Project Architecture

```text
                Streamlit UI
                     │
                     ▼
        Financial Analysis Agent
          (LangGraph ReAct)
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
 Financial Analysis Tools      SQLite Memory
      │
      ▼
  Yahoo Finance API
```

---

## 📂 Project Structure

```
Financial-Analysis-Assistant/
│
├── financial_advisor_backend.py
├── app.py
├── finance_agent_memory.db
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### Create a virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file.

```
GROQ_API_KEY=your_api_key_here
```

### Run the application

```bash
streamlit run app.py
```

---

## 💬 Example Queries

- Analyze AAPL
- Show me the valuation of NVDA
- What is the current trend of TSLA?
- Is MSFT overvalued?
- Compare the valuation metrics of GOOGL

---

## 🧠 How It Works

1. User submits a financial query through the Streamlit interface.
2. The LangGraph ReAct agent determines whether a financial tool is required.
3. Appropriate tools retrieve live market data from Yahoo Finance.
4. The LLM interprets the results and generates a natural-language response.
5. Conversation history is stored using SQLite, enabling persistent multi-session memory.

---

## 📸 Screenshots

Add screenshots of:
- Home page
- Chat interface
- Sidebar conversation history
- Sample stock analysis

---

## 🔮 Future Improvements

- Portfolio risk analysis
- News sentiment analysis
- Technical indicators (RSI, MACD, SMA)
- Stock comparison dashboard
- Price prediction models
- Portfolio performance tracking
- Watchlist management
- PDF investment reports

---

## 📜 License

This project is intended for educational and learning purposes.

---

## ⭐ Acknowledgements

- LangChain
- LangGraph
- Groq
- Streamlit
- Yahoo Finance (yfinance)
