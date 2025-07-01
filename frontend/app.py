import json

import requests as rq
import streamlit as st

st.title("News Reporter Agent")

categories, user_query = st.tabs(["Categories", "Others"])

with categories:
    category = st.selectbox(
        "Select category",
        [
            "None",
            "Business",
            "Entertainment",
            "General",
            "Health",
            "Science",
            "Sports",
            "Technology",
        ],
    )
    if category != "None":
        category_search_button = st.button("Get news")
        if category_search_button:
            category_news = rq.post(
                f"http://localhost:8000/get-category-news/{category}"
            )
            category_top_headlines = json.loads(category_news.content.decode("utf-8"))
            for each in category_top_headlines:
                st.markdown(each, unsafe_allow_html=True)

with user_query:
    user_query_news = st.text_input("Ask me anything")
    if user_query_news:
        st.write("Query: ", user_query_news)
        user_query_search_button = st.button("Get query news")
        if user_query_search_button:
            query_news = rq.post(
                f"http://localhost:8000/get-query-news/{user_query_news}"
            )
            query_top_headlines = json.loads(query_news.content.decode("utf-8"))
            for each in query_top_headlines:
                st.markdown(each, unsafe_allow_html=True)
