import os
import urllib.parse

import requests as rq
from crew import news_agent_crew
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI()

news_api_key = os.getenv("NEWS_API_KEY")
category_news = {}
query_news = {}


@app.post("/get-category-news/{requested_category}")
def get_category_top_headlines(requested_category):
    category_output = []
    url = f"https://newsapi.org/v2/top-headlines?category={requested_category}&apiKey={news_api_key}"
    category_top_headlines = rq.get(url).json()
    articles_from_category = category_top_headlines.get("articles")
    articles_from_category = articles_from_category[:10]
    for each in articles_from_category:
        title = each.get("title")
        description = each.get("description")
        content = each.get("content")
        image_url = each.get("urlToImage")
        if title is not None:
            category_news[title] = [title, description, content, image_url]
            category_output.append(title)
    return category_output


@app.post("/get-query-news/{user_query}")
def get_user_query_top_headlines(user_query):
    query_output = []
    encoded_query = urllib.parse.quote_plus(user_query)
    url = f"https://newsapi.org/v2/everything?language=en&q={encoded_query}&apiKey={news_api_key}"
    query_top_headlines = rq.get(url).json()
    articles_from_query = query_top_headlines.get("articles")
    articles_from_query = articles_from_query[:10]
    for each in articles_from_query:
        title = each.get("title")
        description = each.get("description")
        content = each.get("content")
        image_url = each.get("urlToImage")
        title = each.get("title")
        if title is not None:
            query_news[title] = [title, description, content, image_url]
            query_output.append(title)
    return query_output


@app.post("/get-detailed-explanation/{read_more}")
def get_detailed_explanation_crew_ai(read_more):
    crew_test = news_agent_crew().crew
    article = category_news.get(read_more) or query_news.get(read_more)
    if not article:
        result = crew_test().kickoff(
            inputs={
                "title": read_more,
                "description": "No description available",
                "content": "No content available",
            }
        )
        return [result.raw]
    title, description, content, image_url = article
    result = crew_test().kickoff(
        inputs={
            "title": title,
            "description": description,
            "content": content,
        }
    )
    return [result.raw, image_url]
