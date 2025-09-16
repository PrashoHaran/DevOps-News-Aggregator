import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

@app.route("/")
def home():
    q = request.args.get("q", "technology")
    articles = []
    if NEWSAPI_KEY:
        try:
            resp = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={"q": q, "pageSize": 10, "language": "en", "apiKey": NEWSAPI_KEY},
                timeout=5
            )
            if resp.status_code == 200:
                articles = resp.json().get("articles", [])
        except Exception:
            articles = []
    else:
        articles = [{"title":"NEWSAPI_KEY missing","description":"Set NEWSAPI_KEY env var","url":"#","source":{"name":"local"}}]
    return render_template("index.html", articles=articles, query=q)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
