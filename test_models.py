import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GEMINI_API_KEY", "")
models = [
    m.strip().replace("models/", "")
    for m in os.environ.get(
        "GEMINI_MODELS",
        "gemini-3.8-flash,gemini-3.6-flash,gemini-3.5-flash-lite",
    ).split(",")
    if m.strip()
]
print("จะทดสอบ:", models, flush=True)

body = {"contents": [{"parts": [{"text": "ตอบสั้นๆ ว่า ok"}]}]}

for model in models:
    print(f"... กำลังเรียก {model}", flush=True)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    t = time.time()
    try:
        r = requests.post(url, headers={"x-goog-api-key": key}, json=body, timeout=25)
        print(f"{model}: HTTP {r.status_code} ใช้เวลา {time.time() - t:.1f} วินาที", flush=True)
        if r.status_code != 200:
            print("   ", r.text[:200], flush=True)
    except Exception as e:
        print(f"{model}: {type(e).__name__} หลัง {time.time() - t:.1f} วินาที", flush=True)