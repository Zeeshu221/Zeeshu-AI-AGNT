import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Zeeshu AI",
    page_icon="🤖",
    layout="wide"
)

# ==================== DEEPSEEK STYLE CSS ====================
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
    }
    .main-header {
        color: #ffffff;
        font-size: 2rem;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #4b6cb7, #182848);
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .chat-message-user {
        background-color: #2d5a8c;
        color: white;
        padding: 12px 16px;
        border-radius: 15px 15px 5px 15px;
        margin: 8px 0;
        margin-left: 20%;
        text-align: right;
    }
    .chat-message-ai {
        background-color: #2a2a2a;
        color: #e0e0e0;
        padding: 12px 16px;
        border-radius: 15px 15px 15px 5px;
        margin: 8px 0;
        margin-right: 20%;
        border-left: 3px solid #4b6cb7;
    }
    .stChatInput {
        position: fixed;
        bottom: 20px;
        background-color: #2a2a2a;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d0d0d;
    }
    h1, h2, h3, p, div {
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<div class="main-header">🤖 Zeeshu AI Chat</div>', unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 📋 Menu")
    
    # Clear chat button
    if st.button("🗑️ Nayi Chat Shuru Karein", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📁 File Upload")
    uploaded_file = st.file_uploader(
        "PDF ya Text file upload karein",
        type=["txt", "pdf", "md", "py", "csv"]
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "text/plain" or uploaded_file.name.endswith(('.txt', '.md', '.py', '.csv')):
                file_content = uploaded_file.read().decode("utf-8")
            else:
                file_content = uploaded_file.read().decode("utf-8", errors="ignore")
            
            st.success(f"✅ {uploaded_file.name} load ho gayi!")
            
            if st.button("📄 File ke baare mein poochein"):
                st.session_state.file_content = file_content
                st.session_state.messages.append({
                    "role": "user",
                    "content": f"Main ne ye file upload ki hai:\n\n{file_content[:2000]}\n\nIs ke baare mein batao."
                })
                st.rerun()
        except Exception as e:
            st.error(f"File padhne mein error: {e}")
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    # Model selection
    model_choice = st.selectbox(
        "Model chunein:",
        [
            "nvidia/nemotron-3.5-super-vl:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "google/gemini-2.0-flash-exp:free",
        ]
    )
    
    # Temperature
    temperature = st.slider("Creativity:", 0.0, 1.0, 0.7, 0.1)
    
    st.markdown("---")
    st.markdown("### ℹ️ Info")
    st.caption("Made with ❤️ by Zeeshu")

# ==================== AI CLIENT ====================
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# ==================== CHAT HISTORY ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================== SHOW OLD MESSAGES ====================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-message-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message-ai">{msg["content"]}</div>', unsafe_allow_html=True)

# ==================== CHAT INPUT ====================
if prompt := st.chat_input("Apna sawal likhein..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-message-user">{prompt}</div>', unsafe_allow_html=True)
    
    # AI response
    try:
        stream = client.chat.completions.create(
            model=model_choice,
            messages=st.session_state.messages,
            max_tokens=2000,
            temperature=temperature,
            stream=True
        )
        
        # Live typing
        response_placeholder = st.empty()
        full_reply = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_reply += chunk.choices[0].delta.content
                response_placeholder.markdown(
                    f'<div class="chat-message-ai">{full_reply}▌</div>',
                    unsafe_allow_html=True
                )
        
        response_placeholder.markdown(
            f'<div class="chat-message-ai">{full_reply}</div>',
            unsafe_allow_html=True
        )
        
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        
    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"
        st.markdown(f'<div class="chat-message-ai">{error_msg}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
