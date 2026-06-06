import streamlit as st
import sqlite3
import uuid
from financial_advisor_backend import finance_agent

# Initialize Streamlit Page Config
st.set_page_config(page_title="Financial AI Chat", page_icon="💬", layout="centered")

DB_PATH = "finance_agent_memory.db"

# =========================================================================
# DATABASE HELPERS
# =========================================================================
def get_saved_threads(db_path=DB_PATH):
    """Queries the LangGraph checkpoint table to fetch unique saved thread IDs,

    ordered strictly by their creation timestamp so they don't appear randomly.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # FIXED QUERY: Groups by thread_id and orders chronologically by the checkpoint timestamp
        cursor.execute("""
            SELECT thread_id 
            FROM checkpoints 
            GROUP BY thread_id 
            ORDER BY MIN(checkpoint_id) ASC
        """)
        
        threads = [row[0] for row in cursor.fetchall() if row[0]]
        conn.close()
        return threads
    except Exception:
        return []

# =========================================================================
# MEMORY MANAGEMENT (STATE INITIALIZATION)
# =========================================================================

# 1. Initialize a master dictionary to hold message histories for active sessions
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

# 2. Sync tracking list with actual database checkpoints on first run or refresh
if "chat_sessions" not in st.session_state:
    saved_threads = get_saved_threads()
    if saved_threads:
        st.session_state.chat_sessions = saved_threads
        for thread in saved_threads:
            if thread not in st.session_state.all_chats:
                st.session_state.all_chats[thread] = []
    else:
        st.session_state.chat_sessions = []

# 3. Initialize or load the current active thread ID
if "thread_id" not in st.session_state:
    if st.session_state.chat_sessions:
        st.session_state.thread_id = st.session_state.chat_sessions[-1]
    else:
        first_session = f"session_{uuid.uuid4().hex[:8]}"
        st.session_state.thread_id = first_session
        st.session_state.chat_sessions.append(first_session)
        
    if st.session_state.thread_id not in st.session_state.all_chats:
        st.session_state.all_chats[st.session_state.thread_id] = [
            {"role": "assistant", "content": "Hello! I am your AI financial agent. Enter a stock ticker to start your analysis."}
        ]

# Lazy-load historical messages from LangGraph into UI memory if empty
if not st.session_state.all_chats.get(st.session_state.thread_id):
    try:
        state = finance_agent.get_state({"configurable": {"thread_id": st.session_state.thread_id}})
        messages = state.values.get("messages", [])
        
        formatted_history = []
        for msg in messages:
            if msg.type == "human":
                formatted_history.append({"role": "user", "content": msg.content})
            elif msg.type == "ai" and msg.content:
                formatted_history.append({"role": "assistant", "content": msg.content})
        
        if formatted_history:
            st.session_state.all_chats[st.session_state.thread_id] = formatted_history
        else:
            st.session_state.all_chats[st.session_state.thread_id] = [
                {"role": "assistant", "content": "Welcome back! History loaded from memory database."}
            ]
    except Exception:
        st.session_state.all_chats[st.session_state.thread_id] = [
            {"role": "assistant", "content": "Hello! Enter a stock ticker to start your analysis."}
        ]

# =========================================================================
# SIDEBAR PANEL (CHAT SWITCHER Interface - LATEST FIRST)
# =========================================================================
with st.sidebar:
    st.header("Conversations")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_session = f"session_{uuid.uuid4().hex[:8]}"
        st.session_state.chat_sessions.append(new_session)
        st.session_state.all_chats[new_session] = [
            {"role": "assistant", "content": "Hello! This is a fresh chat thread. What asset are we analyzing next?"}
        ]
        st.session_state.thread_id = new_session
        st.rerun()
        
    st.write("---")
    st.write("📂 Recent History:")
    
    # Reverse chronological array slice 
    reversed_sessions = list(enumerate(st.session_state.chat_sessions))[::-1]
    
    for idx, session_id in reversed_sessions:
        is_active = "🔹 " if session_id == st.session_state.thread_id else "📄 "
        
        # Simple full-width button switcher
        if st.button(f"{is_active} Chat Session {idx + 1}", key=f"sel_{session_id}", use_container_width=True):
            st.session_state.thread_id = session_id
            st.rerun()

    st.write("---")
    if "thread_id" in st.session_state:
        st.caption(f"Active Thread Tracker: `{st.session_state.thread_id}`")

# =========================================================================
# ACTIVE CHAT WINDOW VIEWPORT
# =========================================================================
st.title("💬 Financial Advisor Chatbot")
st.caption("Ask me about stock trajectories, valuations, or trends (e.g., AAPL, NVDA, TSLA)")

if "thread_id" in st.session_state:
    active_history = st.session_state.all_chats[st.session_state.thread_id]

    for msg in active_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_query := st.chat_input("Type your financial query here..."):
        with st.chat_message("user"):
            st.markdown(user_query)
            
        active_history.append({"role": "user", "content": user_query})
        
        with st.chat_message("assistant"):
            try:
                ai_message = st.write_stream(
                    message_chunk.content 
                    for message_chunk, metadata in finance_agent.stream(
                        {"messages": [("user", user_query)]},
                        config={"configurable": {"thread_id": st.session_state.thread_id}},
                        stream_mode="messages"
                    )
                    if metadata.get("langgraph_node") == "agent" and getattr(message_chunk, "content", None)
                )
                active_history.append({"role": "assistant", "content": ai_message})
            except Exception as e:
                st.error(f"Error calling agent: {e}")
else:
    st.rerun()