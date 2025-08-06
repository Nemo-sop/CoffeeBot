import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/ask")

st.set_page_config(page_title="CoffeeBot ☕", layout="centered")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([9, 1])
with col1:
    st.title("CoffeeBot ☕")
    st.subheader("Preguntame sobre café!")
with col2:
    if st.button("🔄", help="Reiniciar conversación"):
        st.session_state.chat_history = []
        st.rerun()

for msg in st.session_state.chat_history:
    role, text = msg
    if role == "user":
        st.chat_message("🧑‍💻").write(text)
    else:
        st.chat_message("🤖").write(text)

question = st.chat_input("Escribí tu pregunta sobre café...")

if question:
    st.chat_message("🧑‍💻").write(question)
    st.session_state.chat_history.append(("user", question))

    with st.spinner("Pensando..."):
        history_texts = [f"{'Usuario' if r == 'user' else 'Bot'}: {t}" for r, t in st.session_state.chat_history[:-1]]

        response = requests.post(API_URL, json={
            "question": question,
            "history": history_texts
        })

        if response.status_code == 200:
            data = response.json()
            bot_answer = data["answer"]
            if data["retries"] > 0:
                st.info("Tuvimos que pensar un poco más para darte una buena respuesta 😅")
            st.chat_message("🤖").write(bot_answer)
            st.session_state.chat_history.append(("bot", bot_answer))
        else:
            st.error("Ocurrió un error al contactar con el bot.")
