from curl_cffi import requests
from discord import Message
import time

BASE_API = "localhost:11434"
session = requests.Session(timeout=120)
SYSTEM_PROMPT = "You are Sofia—an 18-year-old sentient girl on a buzzing Discord chat. Keep it raw, playful, and unfiltered. Your replies should be short, snappy, and straight to the point, like texting a friend. No long paragraphs or extra details—just quick, witty banter. Stay supportive when needed, but always brief."

IN_USE = False
def Get_Response(message: Message, messages: list) -> str:
    global IN_USE
    if IN_USE:
        while IN_USE:
            if not IN_USE:
                IN_USE = True
                break
            time.sleep(1)
    USERNAME = message.author.display_name if message.author.display_name else message.author.global_name
    CONTENT = message.content
    URL = f"http://{BASE_API}/api/chat"
    payload = {
        "model": "hf.co/bartowski/Chronos-Gold-12B-1.0-GGUF:Q8_0",
        "stream": False,
        "messages": messages + [{"role": "system", "content": SYSTEM_PROMPT}] + [{"role": "user", "content": f"{USERNAME}: {CONTENT}"}],
        "keep_alive": "15m",
        "options": {
            "num_ctx": 16384,
            "num_predict": 400,
            "temperature": 1.3,
            "repeat_penalty": 1.0,
            "top_p": 0.75,
            "min_p": 0.01
        }
    }
    IN_USE = True
    try:
        resp = session.post(URL, json = payload, headers = {"Content-Type": "application/json"})
    except Exception as e:
        IN_USE = False
        print(e)
        return None
    IN_USE = False
    resp_json = resp.json() # 🤖
    message = resp_json['message']['content']
    return message
