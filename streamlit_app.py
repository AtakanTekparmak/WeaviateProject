import streamlit as st

from main import setup, streamlit_generate

# Set up the model and function caller
model, function_caller, prefix_string, suffix_string = setup()

# Set the welcome string
WELCOME_STRING = "How can I help you? You can ask me to perform basic CRUD operations on the database. An example query is: 'Can you add a 2022 Opel Astra to the database?'"

st.title("💬 Database Interacting LLM")
st.caption("🚀 A Streamlit chatbot powered by Ollama")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": WELCOME_STRING}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    #response = streamlit_generate(prompt, model, function_caller, prefix_string, suffix_string)
    streamlit_generate(prompt, model, function_caller, prefix_string, suffix_string)
    #st.session_state.messages.append({"role": "assistant", "content": response})
    #st.chat_message("assistant").write(response)