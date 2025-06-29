import requests as rq
import streamlit as st

st.title("News")
res = rq.post("http://localhost:8000/news")
st.write(res.content)
