import streamlit as st

st.set_page_config(layout="wide")

st.title("Global Data Trend Analysis App")

if st.button("Navigation"):
    st.switch_page("app.py")
if st.button("Global data trend analysis"):
    st.switch_page("pages/page_1.py")
if st.button("Upload your own data"):
    st.switch_page("pages/page_2.py")