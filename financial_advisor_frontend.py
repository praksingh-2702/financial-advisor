import streamlit as st
# Point to your correct backend file name
from financial_advisor_backend import finance_agent

# Initialize Streamlit Page Config
st.set_page_config(page_title="Financial AI Chat", page_icon="💬", layout="centered")

st.title("💬 Financial Advisor Chatbot")
st.caption("Ask me about stock trajectories, valuations, or trends (e.g., AAPL, NVDA, TSLA)")

# Maintain unique thread ID for the persistent session memory
if "thread_id" not in st.session_state:
    import uuid
    st.session_state.thread_id = f"session_{uuid.uuid4().hex[:8]}"

# Create or maintain chat history memory inside the browser session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI financial agent. Enter a stock ticker to start your analysis."}
    ]

# Render all previous messages stored in session history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# The Chat Window Input Box
if user_query := st.chat_input("Type your financial query here..."):
    
    # Render user query instantly inside a user bubble
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # Save user query to history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Render assistant container and process agent streaming execution
    with st.chat_message("assistant"):
        try:
            # Using standard list-of-tuples syntax directly inside the generator expression
            ai_message = st.write_stream(
                message_chunk.content 
                for message_chunk, metadata in finance_agent.stream(
                    {"messages": [("user", user_query)]},
                    config={"configurable": {"thread_id": st.session_state.thread_id}},
                    stream_mode="messages"
                )
                if metadata.get("langgraph_node") == "agent" and getattr(message_chunk, "content", None)
            )
            
            # Save the fully built streamed answer to session history
            st.session_state.messages.append({"role": "assistant", "content": ai_message})
            
        except Exception as e:
            st.error(f"Error calling agent: {e}")