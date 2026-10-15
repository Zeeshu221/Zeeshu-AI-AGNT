import streamlit as st
from groq import Groq

st.set_page_config(page_title="Zeeshu AI", page_icon="🤖")
st.title("🤖 Zeeshu AI Chat")

# API Key (Streamlit secrets se aayegi)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
