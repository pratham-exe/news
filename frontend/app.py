import json
from io import BytesIO

import requests as rq
import streamlit as st
from PIL import Image

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
                st.subheader(each)
                with st.expander("Read more"):
                    read_more = rq.post(
                        f"http://localhost:8000/get-detailed-explanation/{each}"
                    )
                    result = json.loads(read_more.content.decode("utf-8"))
                    if len(result) == 2:
                        try:
                            response = rq.get(result[1], timeout=10)
                            image = Image.open(BytesIO(response.content))
                            st.image(image)
                        except Exception as e:
                            print(e)
                    st.write(result[0])

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
                st.subheader(each)
                with st.expander("Read more"):
                    read_more = rq.post(
                        f"http://localhost:8000/get-detailed-explanation/{each}"
                    )
                    result = json.loads(read_more.content.decode("utf-8"))
                    if len(result) == 2:
                        try:
                            response = rq.get(result[1], timeout=10)
                            image = Image.open(BytesIO(response.content))
                            st.image(image)
                        except Exception as e:
                            print(e)
                    st.write(result[0])
