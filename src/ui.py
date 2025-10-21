import streamlit as st

def handle_user_query(question, conversation_chain):
    if conversation_chain is None:
        st.warning("Please upload PDFs and click 'Get Started' first.")
        return
    
    response = conversation_chain({"question": question})
    answer = response.get("answer", "Sorry, I couldn’t find an answer.")

    st.write("### 🧠 Answer")
    st.write(answer)

    st.divider()
    st.write("**Chat History:**")
    for msg in response.get("chat_history", []):
        st.write(f"**{msg.type.capitalize()}:** {msg.content}")
