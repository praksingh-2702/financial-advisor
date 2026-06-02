import streamlit as st
# Import your agent function directly from your backend file
from financial_advisor_backend import finance_agent

# 1. Initialize Streamlit Page Config
st.set_page_config(page_title="Financial AI Chat", page_icon="💬", layout="centered")

st.title("💬 Financial Advisor Chatbot")
st.caption("Ask me about stock trajectories, valuations, or trends (e.g., AAPL, NVDA, TSLA)")

# 2. Cache the backend agent so it doesn't reload on every keystroke

# 3. Create or maintain chat history memory inside the browser session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI financial agent. Enter a stock ticker to start your analysis."}
    ]

# 4. Render all previous messages stored in session history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. The Chat Window Input Box
if user_query := st.chat_input("Type your financial query here..."):
    
    # Render user query instantly inside a user bubble
    with st.chat_message("user"):
        st.markdown(user_query)
    # Save user query to history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Render assistant container and process agent execution
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Wrap input text string into the list structured format required by LangGraph
                inputs = {"messages": [("user", user_query)]}
                
                # Invoke backend agent execution
                response = finance_agent.invoke(inputs)
                
                # Grab the final text string payload from the response message array
                final_answer = response["messages"][-1].content
                
                # Print the final result inside the assistant chat window
                st.markdown(final_answer)
                
                # Save assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                
            except Exception as e:
                st.error(f"Error calling agent: {e}")