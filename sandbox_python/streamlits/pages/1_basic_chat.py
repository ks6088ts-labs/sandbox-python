from os import getenv

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

with st.sidebar:
    azure_openai_endpoint = st.text_input(
        label="AZURE_OPENAI_ENDPOINT",
        value=getenv("AZURE_OPENAI_ENDPOINT"),
        key="AZURE_OPENAI_ENDPOINT",
        type="default",
    )
    azure_openai_api_key = st.text_input(
        label="AZURE_OPENAI_API_KEY",
        # value=getenv("AZURE_OPENAI_API_KEY"),
        key="AZURE_OPENAI_API_KEY",
        type="password",
    )
    azure_openai_api_version = st.text_input(
        label="AZURE_OPENAI_API_VERSION",
        value=getenv("AZURE_OPENAI_API_VERSION"),
        key="AZURE_OPENAI_API_VERSION",
        type="default",
    )
    azure_openai_deployment_chat = st.text_input(
        label="AZURE_OPENAI_DEPLOYMENT_CHAT",
        value=getenv("AZURE_OPENAI_DEPLOYMENT_CHAT"),
        key="AZURE_OPENAI_DEPLOYMENT_CHAT",
        type="default",
    )
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/sandbox-python/tree/main/sandbox_python/streamlits/pages/1_basic_chat.py)"


def is_configured():
    return azure_openai_api_key and azure_openai_endpoint and azure_openai_api_version and azure_openai_deployment_chat


st.title("Basic Chat")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Hello! I'm a helpful assistant.",
        }
    ]

# Show chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Receive user input
if prompt := st.chat_input(disabled=not is_configured()):
    llm = AzureChatOpenAI(
        temperature=0,
        api_key=azure_openai_api_key,
        api_version=azure_openai_api_version,
        azure_endpoint=azure_openai_endpoint,
        model=azure_openai_deployment_chat,
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    st.chat_message("user").write(prompt)
    with st.spinner("Thinking..."):
        response = llm.invoke(prompt)
    msg = response.content
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": msg,
        }
    )
    st.chat_message("assistant").write(msg)
