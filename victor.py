import os
import requests
import json
import sys
import random
from functools import wraps
from dotenv import load_dotenv
from constants import PERSONALITY, MODEL, DEFAULT_RESPONSES, OPEN_API_CHAT_URL

load_dotenv()


def no_response(no_threshold):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if random.randint(1, 100) < no_threshold:
                return "NO!"
            return func(*args, **kwargs)
        return wrapper
    return decorator


class Victor:
    def __init__(self):
        secret = os.environ.get("OPENAI_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {secret}",
        }
        self.messages = [{"role": "system", "content": PERSONALITY}]

    @no_response(no_threshold=30)
    def tells(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})

        data = {
            "model": MODEL,
            "messages": self.messages,
            "temperature": 1,
        }

        response = requests.post(
            OPEN_API_CHAT_URL, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    try:
        message = sys.argv[1]
        response = Victor().tells(message)
    except IndexError:
        response = random.choice(DEFAULT_RESPONSES)
    print('\n' + response)
