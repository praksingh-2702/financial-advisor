import streamlit as st
from financial_advisor_backend import finance_agent

# Initialize Streamlit Page Config
st.set_page_config(page_title="Financial AI Chat", page_icon="💬", layout="centered")

# =========================================================================
# MEMORY MANAGEMENT (STATE INITIALIZATION)
# =========================================================================

# 1. Initialize a master dictionary to hold message histories for ALL sessions
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

# 2. Initialize a tracking list to maintain the order of active chat sessions
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []

# 3. Initialize or load the current active thread ID
if "thread_id" not in st.session_state:
    import uuid
    first_session = f"session_{uuid.uuid4().hex[:8]}"
    st.session_state.thread_id = first_session
    
    # Register this initial session into our global tracking state
    st.session_state.chat_sessions.append(first_session)
    st.session_state.all_chats[first_session] = [
        {"role": "assistant", "content": "Hello! I am your AI financial agent. Enter a stock ticker to start your analysis."}
    ]

# =========================================================================
# SIDEBAR PANEL (CHAT SWITCHER Interface)
# =========================================================================
with st.sidebar:
    st.header("Conversations")
    
    # "New Chat" button logic
    if st.button("➕ New Chat", use_container_width=True):
        import uuid
        new_session = f"session_{uuid.uuid4().hex[:8]}"
        
        # Register the new session fields
        st.session_state.chat_sessions.append(new_session)
        st.session_state.all_chats[new_session] = [
            {"role": "assistant", "content": "Hello! This is a fresh chat thread. What asset are we analyzing next?"}
        ]
        
        # Switch the active target thread to this new ID and refresh
        st.session_state.thread_id = new_session
        st.rerun()
        
    st.write("---")
    
    # 4. DYNAMIC SWITCHER LIST: Render a button for every historical session
    st.write("📂 Recent History:")
    for idx, session_id in enumerate(st.session_state.chat_sessions):
        # Visually highlight which session is currently open
        is_active = "🔹 " if session_id == st.session_state.thread_id else "📄 "
        
        # Display the button. If clicked, change active thread ID and rerun
        if st.button(f"{is_active} Chat Session {idx + 1}", key=session_id, use_container_width=True):
            st.session_state.thread_id = session_id
            st.rerun()

    st.write("---")
    st.caption(f"Active Thread Tracker: `{st.session_state.thread_id}`")

# =========================================================================
# ACTIVE CHAT WINDOW VIEWPORT
# =========================================================================
st.title("💬 Financial Advisor Chatbot")
st.caption("Ask me about stock trajectories, valuations, or trends (e.g., AAPL, NVDA, TSLA)")

# Point active_history reference to the current thread's log array
active_history = st.session_state.all_chats[st.session_state.thread_id]

# Render all previous messages belonging to this SPECIFIC thread session
for msg in active_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# The Chat Window Input Box
if user_query := st.chat_input("Type your financial query here..."):
    
    # Render user query instantly inside a user bubble
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # Append the message directly into the sub-session history array
    active_history.append({"role": "user", "content": user_query})
    
    # Render assistant container and process agent streaming execution
    with st.chat_message("assistant"):
        try:
            # Using your clean single-line generator expression
            ai_message = st.write_stream(
                message_chunk.content 
                for message_chunk, metadata in finance_agent.stream(
                    {"messages": [("user", user_query)]},
                    config={"configurable": {"thread_id": st.session_state.thread_id}},
                    stream_mode="messages"
                )
                if metadata.get("langgraph_node") == "agent" and getattr(message_chunk, "content", None)
            )
            
            # Save the fully built streamed answer into the sub-session history
            active_history.append({"role": "assistant", "content": ai_message})
            
        except Exception as e:
            st.error(f"Error calling agent: {e}")