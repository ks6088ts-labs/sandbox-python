from pprint import pprint

import streamlit as st
from dotenv import load_dotenv

from sandbox_python.llms.graphs.core import get_graph

load_dotenv()


with st.sidebar:
    k = st.text_input(
        label="K",
        value=1,
        key="K",
        type="default",
    )
    "[Azure Portal](https://portal.azure.com/)"
    "[Azure OpenAI Studio](https://oai.azure.com/resource/overview)"
    "[View the source code](https://github.com/ks6088ts-labs/sandbox-python/tree/main/sandbox_python/streamlits/pages/2_lang_graph.py)"


def is_configured():
    return True


st.title("LangGraph")

if not is_configured():
    st.warning("Please fill in the required fields at the sidebar.")

# Receive user input
if prompt := st.chat_input(disabled=not is_configured()):
    st.chat_message("user").write(prompt)

    for output in get_graph().stream(
        {
            "question": prompt,
            "k": int(k),
        },
        config={
            "configurable": {
                "thread_id": "2",
            },
        },
    ):
        for key, value in output.items():
            pprint(f"Finished running: {key}:")
    st.chat_message("assistant").write(value["generation"])
