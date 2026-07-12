import urllib.request
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "qwen2.5-coder:7b",
    "prompt": "Write a simple hello world script in Python.",
    "stream": True
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as response:
    for line in response:
        if line:
            chunk = json.loads(line.decode("utf-8"))
            print(chunk.get("response", ""), end="")