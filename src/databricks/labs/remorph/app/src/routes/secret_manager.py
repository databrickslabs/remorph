import streamlit as st  # type: ignore


def main():
    st.title("Secret Manager")
    st.write("Manage your secrets securely here.")
    st.text_input("Enter your secret key:")
