import streamlit as st
from dotenv import load_dotenv


def main():
    st.title("Code samples for Streamlit")
    st.info("Select a code sample from the sidebar to run it")


if __name__ == "__main__":
    load_dotenv()
    main()
