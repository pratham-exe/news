#!/usr/bin/env python3
import os
import sys

import whisper
from dotenv import load_dotenv

load_dotenv()

RECORD_PATH = os.getenv("RECORD_PATH")


def agi(cmd):
    sys.stdout.write(cmd + "\n")
    sys.stdout.flush()
    return sys.stdin.readline().strip()


def read_agi_env():
    while True:
        line = sys.stdin.readline().strip()
        if line == "":
            break


def log(msg):
    agi(f'VERBOSE "{msg}" 3')


def main():
    read_agi_env()

    agi("ANSWER")
    agi('STREAM FILE beep ""')

    agi(f'RECORD FILE {RECORD_PATH[:-4]} wav "#" 3600000')

    if not os.path.exists(RECORD_PATH):
        log(f"Recording not found at: {RECORD_PATH}")
    else:
        try:
            log("Loading Whisper model (base)...")
            model = whisper.load_model("base")
            log("Starting transcription...")

            result = model.transcribe(RECORD_PATH)
            transcript = result.get("text", "")

            if transcript:
                log(f"Transcription: {transcript}")
            else:
                log("Transcription empty or no speech detected.")

        except Exception as e:
            log(f"Whisper error: {e}")

    agi('STREAM FILE goodbye ""')
    agi("HANGUP")


if __name__ == "__main__":
    main()
