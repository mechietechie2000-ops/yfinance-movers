from flask import Flask, jsonify, render_template
import requests
import time

app = Flask(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    )
}

SCREENER_URL = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"

# simple in-memory cache so rapid tab-switching / refreshing doesn't hammer Yahoo
_cache = {}
CACHE_TTL = 20  # seconds


def fetch_screener(scr_id, count=100):
    now = time.time()
    cached = _cache.get(scr_id)
    if cached and now - cached["ts"] < CACHE_TTL:
        return cached["data"]

    params = {
        "formatted": "true",
        "lang": "en-US",
        "region": "US",
        "scrIds": scr_id,
        "count": count,
    }
    r = requests.get(SCREENER_URL, headers=HEADERS, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    quotes = data["finance"]["result"][0]["quotes"]

    out = []
    for q in quotes:
        out.append({
            "symbol": q.get("symbol"),
            "name": q.get("shortName") or q.get("longName") or "",
            "price": (q.get("regularMarketPrice") or {}).get("raw"),
            "change": (q.get("regularMarketChange") or {}).get("raw"),
            "changePct": (q.get("regularMarketChangePercent") or {}).get("raw"),
            "volume": (q.get("regularMarketVolume") or {}).get("raw"),
            "marketCap": (q.get("marketCap") or {}).get("fmt"),
        })

    _cache[scr_id] = {"ts": now, "data": out}
    return out


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/<kind>")
def api(kind):
    mapping = {
        "gainers": "day_gainers",
        "losers": "day_losers",
        "actives": "most_actives",
    }
    if kind not in mapping:
        return jsonify({"error": "unknown kind"}), 404
    try:
        return jsonify(fetch_screener(mapping[kind]))
    except Exception as e:
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    # Runs on http://127.0.0.1:5000
    app.run(host="0.0.0.0", debug=False, port=5000)
