import os
from langchain_groq import ChatGroq
import yfinance as yf
import pandas as pd
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv



load_dotenv()
model=ChatGroq(model="llama-3.3-70b-versatile")


@tool
def check_stock_price_and_trend(ticker :str) -> str:
    """Fethes the current price and 5-day historical trend for a given stock ticker."""
    stock=yf.Ticker(ticker)
    hist=stock.history(period="5d")

    if hist.empty:
        return f"No data found for ticker '{ticker}'. Please check the ticker symbol and try again."

    latest_price=hist['Close'].iloc[-1]
    start_price=hist['Close'].iloc[0]
    pct_change=((latest_price - start_price) / start_price) * 100

    return f"Ticker: {ticker.upper()}. Current Price: ${latest_price:.2f}. 5-Day Trend: {pct_change:.2f}%."

@tool
def get_company_valuation_metrics(ticker: str) -> str:
    """Fetches key valuation metrics like P/E Ratio to assess if a stock is overvalued."""
    stock = yf.Ticker(ticker)
    info = stock.info

    pe_ratio = info.get('trailingPE', 'N/A')
    forward__pe = info.get('forwardPE', 'N/A')
    market_cap = info.get('marketCap', 'N/A')
    return f"Ticker: {ticker.upper()}, Trailing P/E: {pe_ratio}, Forward P/E: {forward__pe}, Market Cap: {market_cap}."


tools=[check_stock_price_and_trend, get_company_valuation_metrics]
checkpointer =InMemorySaver()
finance_agent=create_react_agent(model=model, tools=tools, checkpointer=checkpointer)



