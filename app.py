import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Maria ka AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Maria ka Personal Chatbot")
st.markdown("---")

llm = ChatGroq(model="llama-3.1-8b-instant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="Tum ek helpful assistant ho jo Urdu aur English mein jawab deta hai. Tumhara naam Aria hai.")
    ]

if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

for msg in st.session_state.chat_display:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Kuch poochho...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.chat_display.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hun..."):
            response = llm.invoke(st.session_state.messages)
            st.write(response.content)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.chat_display.append({
        "role": "assistant",
        "content": response.content
    })