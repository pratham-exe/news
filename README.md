# news - News Reporter Agent

A multi-modal, conversational news agent that delivers news via both a web interface and phone calls.  
It uses FastAPI, Streamlit, CrewAI, Whisper, and gTTS, and can be accessed through a web browser or by calling an Asterisk-powered phone line.

## Features

- **Web Frontend:** Streamlit app for interactive news browsing and querying.
- **Conversational Phone Agent:** Call a SIP number and interact with the news agent using your voice.
- **Category & Query News:** Get top headlines by category or ask for news on any topic.
- **AI-Powered Summaries:** CrewAI agents generate professional, broadcast-style news summaries.
- **Keyword Extraction:** An AI agent extracts keywords from user queries for more relevant news retrieval.
- **Voice Transcription & Synthesis:** Uses Whisper for speech-to-text and gTTS for text-to-speech.

## Setup

### 1. **Clone the Repository**

```
git clone https://github.com/pratham-exe/news.git
cd news
```

### 2. **Prerequisites**

- **Python 3.8+**
- **Asterisk** (for SIP/phone call integration)
- **ffmpeg** (for audio conversion)
- **A NewsAPI API key** (for fetching news)
- **GROQ API key** (for CrewAI LLM integration)
- **A SIP client** (e.g., Zoiper, Linphone, MizuDroid) for testing phone calls

### 3. **Install Python Packages**

```
pip install -r requirements.txt
```

### 4. **Environment Variables**

Create a `.env` file in the backend directory with:

```
NEWS_API_KEY=your_newsapi_key
GROQ_API_KEY=your_groq_api_key
RECORD_PATH=/absolute/path/to/recording.wav
VIRTUAL_ENV=/absolute/path/to/virtual/environment/bin/python3
AGI_SCRIPT=/absolute/path/to/agi.py
```

### 5. **Run the Backend**

```
cd backend
fastapi dev main.py
```

### 6. **Run the Web Frontend**

```
cd frontend
streamlit run app.py
```

### 7. **Set Up Asterisk for Phone Calls**

- Configure your SIP users and dialplan to point to `agi.sh` as an AGI script.
- Example dialplan:

```
exten = 1000,1,Answer()
same = n,AGI(/absolute/path/to/backend/agi.sh)
same = n,Hangup()
```

- Register a SIP client (Zoiper, Linphone, MizuDroid etc.) to your Asterisk server and dial the extension.

## Usage

### **Web Interface**

- Open the Streamlit app in your browser.
- Select a news category or enter a custom query.
- Click on headlines to get detailed, AI-generated summaries.

### **Phone Interface**

- Call the configured SIP extension.
- Interact with the agent using your voice:
- Choose category or query news.
- Listen to headlines (with pauses and numbering).
- Say a number to get more details.
- Say "back" to return to the main menu.

## How It Works

- **FastAPI Backend:** Handles all news fetching, keyword extraction, and summary generation.
- **CrewAI Agents:**
  - `explainer_agent`: Summarizes news articles in a professional style.
  - `keyword_extractor_agent`: Extracts keywords from user queries for precise news search.
- **AGI Script:**
  - Handles phone call logic, voice prompts, and interaction flow.
  - Uses Whisper for speech-to-text and gTTS+ffmpeg for text-to-speech.
- **Streamlit Frontend:**
  - Provides a user-friendly web interface for browsing and querying news.
