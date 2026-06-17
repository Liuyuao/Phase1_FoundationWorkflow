import streamlit as st
from agent_engine import agent_app

st.set_page_config(page_title="Insurance Multi-Agent Assistant", page_icon="🛡️", layout="wide")
st.title("🛡️ Insurance Multi-Agent Assistant")
st.caption("Powered by LangGraph Routing Workflow + Amazon Bedrock Knowledge Bases")

# UI Layout Side Info
with st.sidebar:
    st.header("🧠 System Overview")
    st.markdown("""
    This frontend feeds queries directly into a **LangGraph StateGraph**. 
    The graph analyzes your question and routes it to the specific domain KB:
    - **Policy Agent**: Coverages & Terms
    - **Claims Agent**: Accidents & Process
    - **Product Agent**: Discounts & Savings
    """)

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "agent_used" in message:
            st.caption(f"⚙️ Routed to: {message['agent_used']}")

# Main User Input
prompt = st.chat_input("Ask about your insurance policy, claims, or discounts...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("LangGraph is evaluating routing workflow..."):
            # EXECUTE THE ACTUAL LANGGRAPH!
            inputs = {"question": prompt, "messages": []}
            output = agent_app.invoke(inputs)
            
            final_ans = output.get("final_answer", "No answer found.")
            routed_to = output.get("active_agent", "Unknown")
            
            st.markdown(final_ans)
            st.caption(f"⚙️ Routed to: {routed_to}")
            
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_ans,
        "agent_used": routed_to
    })