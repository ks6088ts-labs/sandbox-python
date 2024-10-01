import streamlit as st
from dotenv import load_dotenv

from sandbox_python.slms.core import SlmClient

load_dotenv()

with st.sidebar:
    selected_model = st.selectbox(
        label="Model",
        index=0,
        options=[
            ".onnx/cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4",
            # add more models here
        ],
        key="selected_model",
    )
    selected_prompt = st.selectbox(
        label="Prompt",
        index=0,
        options=[
            "Proofread the following text",
            "Summarize the following text",
            "Generate a report based on the following text",
        ],
    )
    "[View the source code](https://github.com/ks6088ts-labs/sandbox-python/tree/main/sandbox_python/streamlits/pages/3_slm_apps.py)"


def initialize_session():
    if "target_text" not in st.session_state:
        st.session_state.target_text = "Please input text here."


initialize_session()

st.title("SLM Playground")

uploaded_file = st.file_uploader(
    "Upload an audio file",
    type=(
        "mp3",
        "wav",
        "ogg",
        "flac",
        "m4a",
    ),
)

if transcribe_button := st.button("Transcribe", disabled=not uploaded_file):
    with st.spinner("Transcribing..."):
        # FIXME: Implement the transcription logic here
        st.session_state.target_text = "FIXME: Implement the transcription logic"


target_text = st.text_area(
    label="Target text",
    value=st.session_state.target_text,
    height=200,
    key="target_text",
)
st.write(f"You wrote {len(target_text)} characters.")

if run_button := st.button("Run", disabled=not target_text or not selected_model or not selected_prompt):
    with st.spinner("Running..."):
        slm = SlmClient(model_path=selected_model)
        result = slm.invoke(f"{selected_prompt}: {target_text}")
    st.chat_message("ai").write(result)
