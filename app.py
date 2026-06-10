import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import base64

load_dotenv()

# Page config
st.set_page_config(
    page_title="Maria ka AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS - Card Style
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .chat-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .user-card {
        background: #667eea;
        color: white;
        border-radius: 20px;
        padding: 15px 20px;
        margin: 10px 0;
        margin-left: 50px;
        box-shadow: 0 2px 10px rgba(102,126,234,0.3);
    }
    .ai-card {
        background: white;
        border-radius: 20px;
        padding: 15px 20px;
        margin: 10px 0;
        margin-right: 50px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .header-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 5px 20px rgba(102,126,234,0.4);
    }
    .stChatInput {
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# Photo load karo
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Header Card
try:
    img_base64 = get_image_base64("images/maria.jpeg")
    st.markdown(f"""
    <div class="header-card">
        <img src="data:image/jpeg;base64,{img_base64}" 
             style="width:100px; height:100px; border-radius:50%; 
                    border:3px solid white; object-fit:cover; margin-bottom:10px;">
        <h2 style="margin:0; color:white;">Maria ka Personal Chatbot</h2>
        <p style="margin:5px 0 0 0; opacity:0.8;">Powered by Aria AI ✨</p>
    </div>
    """, unsafe_allow_html=True)
except:
    st.markdown("""
    <div class="header-card">
        <h2 style="margin:0; color:white;">🤖 Maria ka Personal Chatbot</h2>
        <p style="margin:5px 0 0 0; opacity:0.8;">Powered by Aria AI ✨</p>
    </div>
    """, unsafe_allow_html=True)

# LLM setup
llm = ChatGroq(model="llama-3.1-8b-instant")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="Tum ek helpful assistant ho jo Urdu aur English mein jawab deta hai. Tumhara naam Aria hai.")
    ]
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

# Chat history dikhao
for msg in st.session_state.chat_display:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-card">
            👤 <b>Tum:</b> {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ai-card">
            🤖 <b>Aria:</b> {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# User input
user_input = st.chat_input("Kuch poochho...")

if user_input:
    st.markdown(f"""
    <div class="user-card">
        👤 <b>Tum:</b> {user_input}
    </div>
    """, unsafe_allow_html=True)

    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.chat_display.append({
        "role": "user", "content": user_input
    })

    with st.spinner("Aria soch rahi hai..."):
        response = llm.invoke(st.session_state.messages)

    st.markdown(f"""
    <div class="ai-card">
        🤖 <b>Aria:</b> {response.content}
    </div>
    """, unsafe_allow_html=True)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.chat_display.append({
        "role": "assistant", "content": response.content
    })