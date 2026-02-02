import streamlit as st
# import sys
# sys.path.append(
#     "/Users/edwardlauv/Desktop/learn-ai-with-python/projects/chat_bot/hugging-chat-api"
# )
from hugchat.login import Login
from hugchat import hugchat

st.title("Simple ChatBot")

with st.sidebar:
    st.title("Login HugChat")
    hf_email = st.text_input("Enter E-mail: ")
    hf_password = st.text_input("Enter Password: ", type='password')
    if not (hf_email and hf_password):
        st.warning("Please enter your account!")
    else:
        st.success("Proceed to entering your prompt message!")

if "message" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content" : "How may I help you?"}]
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input(disabled=not (hf_email and hf_password)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# chú ý chỗ này, khi login nếu bị lỗi từ thư viện thì hãy clone API từ github về 
# sửa code theo PR: https://github.com/Soulter/hugging-chat-api/pull/290
# chạy cd hugging-chat-api -> pip install -e .
def generate_response(prompt_input, email, password):
    sign = Login(email, password)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"
    return chatbot.chat(prompt_input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_password)
            st.write(response)
    message = {"role": "assistant", "content": response }
    st.session_state.messages.append(message)