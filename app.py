import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Zeeshu AI", page_icon="🤖")
st.title("🤖 Zeeshu AI Chat")

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Apna sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        stream = client.chat.completions.create(
            model="nvidia/nemotron-3.5-super-vl:free",
            messages=st.session_state.messages,
            max_tokens=2000,
            stream=True
        )
        reply = st.chat_message("assistant").write_stream(
            chunk.choices[0].delta.content or ""
            for chunk in stream
            if chunk.choices[0].delta.content
        )
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.chat_message("assistant").write(f"⚠️ Error: {e}")
