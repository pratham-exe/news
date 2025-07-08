#!/usr/bin/env python3
import sys


def agi_write(cmd):
    sys.stdout.write(cmd + "\n")
    sys.stdout.flush()
    response = sys.stdin.readline().strip()
    return response


def read_agi_env():
    while True:
        line = sys.stdin.readline().strip()
        if line == "":
            break


if __name__ == "__main__":
    read_agi_env()

    agi_write("ANSWER")
    agi_write('STREAM FILE goodbye ""')
    agi_write("HANGUP")
