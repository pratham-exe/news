from fastapi import FastAPI

app = FastAPI()


@app.post("/news")
def home():
    return {"Hello News"}
