import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Zeeshu AI", page_icon="🤖")
st.title("🤖 Zeeshu AI Chat")

# OpenRouter client
client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein dikhayein
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Naya sawal
if prompt := st.chat_input("Apna sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
