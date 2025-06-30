import os

import requests as rq
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI()

news_api_key = os.getenv("NEWS_API_KEY")


@app.post("/get-category-news/{requested_category}")
def get_category_top_headlines(requested_category):
    output = []
    url = f"https://newsapi.org/v2/top-headlines?category={requested_category}&apiKey={news_api_key}"
    category_top_headlines = rq.get(url).json()
    articles_from_category = category_top_headlines.get("articles")
    for each in articles_from_category:
        if each.get("description") is not None:
            output.append(each.get("description"))
        else:
            output.append(each.get("title"))
    return output
