#!/usr/bin/env python3
import json
import os
import re
import sys
import tempfile

import requests
import whisper
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

RECORD_PATH = os.getenv("RECORD_PATH")
BACKEND_URL = "http://127.0.0.1:8000"
CATEGORIES = [
    "Business",
    "Entertainment",
    "General",
    "Health",
    "Science",
    "Sports",
    "Technology",
]

NUMBER_WORDS = {
    "one": 1,
    "first": 1,
    "number one": 1,
    "1": 1,
    "two": 2,
    "second": 2,
    "number two": 2,
    "2": 2,
    "three": 3,
    "third": 3,
    "number three": 3,
    "3": 3,
    "four": 4,
    "fourth": 4,
    "number four": 4,
    "4": 4,
}


def agi_commands(cmd):
    sys.stdout.write(cmd + "\n")
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def read_agi_env():
    while True:
        line = sys.stdin.readline().strip()
        if line == "":
            break


def log(msg):
    agi_commands(f'VERBOSE "{msg}" 3')


def synthesize_and_play(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf_mp3:
        tts.save(tf_mp3.name)
        tf_mp3.flush()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tf_wav:
            os.system(f"ffmpeg -y -i {tf_mp3.name} -ar 8000 -ac 1 -f wav {tf_wav.name}")
            agi_commands(f'STREAM FILE {tf_wav.name[:-4]} ""')
            os.unlink(tf_wav.name)
        os.unlink(tf_mp3.name)


def record_and_transcribe(prompt):
    synthesize_and_play(prompt)
    agi_commands(f'RECORD FILE {RECORD_PATH[:-4]} wav "#" 10000')
    if not os.path.exists(RECORD_PATH):
        return ""
    model = whisper.load_model("base")
    result = model.transcribe(RECORD_PATH)
    transcript = result.get("text", "")
    return transcript.strip().lower()


def fetch_category_news(category):
    url = f"{BACKEND_URL}/get-category-news/{category}"
    r = requests.post(url)
    if r.status_code == 200 and r.json():
        return json.loads(r.content.decode("utf-8"))
    return []


def fetch_query_news(query):
    url = f"{BACKEND_URL}/get-query-news/{query}"
    r = requests.post(url)
    if r.status_code == 200 and r.json():
        return json.loads(r.content.decode("utf-8"))
    return []


def fetch_details(title):
    url = f"{BACKEND_URL}/get-detailed-explanation/{title}"
    r = requests.post(url)
    if r.status_code == 200:
        detail = r.json()
        if isinstance(detail, list) and detail:
            return json.loads(r.content.decode("utf-8"))[0]
    return "Sorry, no details found."


def extract_number_from_text(text):
    match = re.search(r"\\b(\\d)\\b", text)
    if match:
        return int(match.group(1))
    for word, idx in NUMBER_WORDS.items():
        if word in text:
            return idx
    return None


def main():
    read_agi_env()
    agi_commands("ANSWER")
    agi_commands('STREAM FILE beep ""')

    synthesize_and_play("Welcome to the News Reporter Agent")

    while True:
        user_choice = record_and_transcribe("Please say 'category' or 'query'.")
        log(user_choice)
        if not user_choice or "exit" in user_choice:
            synthesize_and_play("Thank you for calling. Goodbye.")
            break

        if "category" in user_choice:
            synthesize_and_play(
                "Please say a news category: Business, Entertainment, General, Health, Science, Sports, or Technology."
            )
            cat_resp = record_and_transcribe("Say the category.")
            log(cat_resp)
            category = next((c for c in CATEGORIES if c.lower() in cat_resp), None)
            if not category:
                synthesize_and_play(
                    "Sorry, I didn't catch a valid category. Please try again."
                )
                continue
            headlines = fetch_category_news(category)
            if not headlines:
                synthesize_and_play(f"No news found for {category}.")
                continue

        elif "query" in user_choice:
            synthesize_and_play("Please say your news query.")
            query_resp = record_and_transcribe("Say your query.")
            keywords = query_resp
            headlines = fetch_query_news(keywords)
            if not headlines:
                synthesize_and_play(f"No news found for your query.")
                continue

        else:
            synthesize_and_play(
                "Sorry, I didn't understand. Please say 'category' or 'query'."
            )
            continue

        i = 0
        while i < len(headlines):
            batch = headlines[i : i + 4]
            for idx, title in enumerate(batch):
                synthesize_and_play(f"Number {idx+1}. {title}")
                agi_commands("WAIT FOR DIGIT 1000")
            synthesize_and_play(
                "You can say the number for more details, say the title, 'next' to hear more headlines, 'back' or 'other news' to return to the main menu, or 'exit' to end."
            )
            user_action = record_and_transcribe(
                "Say the number, title, 'next', 'back', 'other news', or 'exit'."
            )
            log(user_action)
            if not user_action or "exit" in user_action:
                synthesize_and_play("Thank you for calling. Goodbye.")
                agi_commands('STREAM FILE goodbye ""')
                agi_commands("HANGUP")
                return
            if "back" in user_action or "other news" in user_action:
                break
            if "next" in user_action:
                i += 4
                continue
            selected_idx = extract_number_from_text(user_action)
            if selected_idx is not None and 1 <= selected_idx <= len(batch):
                matched = batch[selected_idx - 1]
            else:
                matched = next((t for t in batch if user_action in t.lower()), None)
            if matched:
                details = fetch_details(matched)
                synthesize_and_play(details)
                synthesize_and_play(
                    "Would you like to hear more headlines from this topic? Say 'yes' to continue, 'back' or 'other news' to return to the main menu, or 'no' or 'exit' to end."
                )
                more = record_and_transcribe(
                    "Say 'yes', 'back', 'other news', 'no', or 'exit'."
                )
                log(more)
                if more:
                    if "yes" in more:
                        i += 4
                        continue
                    elif "back" in more or "other news" in more:
                        break
                    else:
                        synthesize_and_play("Thank you for calling. Goodbye.")
                        agi_commands('STREAM FILE goodbye ""')
                        agi_commands("HANGUP")
                        return
            else:
                synthesize_and_play("Sorry, I didn't catch that. Please try again.")


if __name__ == "__main__":
    main()
