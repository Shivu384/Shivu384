"""Scrape the public contribution calendar (no token) -> data/contributions.json"""
import json, re
import datetime as dt
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USER = "Shivu384"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch(user):
    r = requests.get(
        f"https://github.com/users/{user}/contributions",
        headers={"User-Agent": "Mozilla/5.0 (profile-art)"},
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.find_all("td", attrs={"data-date": True}):
        level = int(td.get("data-level", 0))
        m = re.match(r"(\d+)\s+contribution", tips.get(td.get("id"), ""))
        count = int(m.group(1)) if m else (level if not tips else 0)
        days.append({"date": td["data-date"], "count": count, "level": level})
    days.sort(key=lambda d: d["date"])
    if not days:
        raise SystemExit("No contribution cells found - GitHub markup may have changed.")
    return days


def stats(days):
    total = sum(d["count"] for d in days)
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    # current streak: today may still be empty, so allow starting from yesterday
    i = len(days) - 1
    if days[i]["count"] == 0:
        i -= 1
    current = 0
    while i >= 0 and days[i]["count"] > 0:
        current += 1
        i -= 1
    best = max(days, key=lambda d: d["count"])
    months = {}
    for d in days:
        months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]
    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": months,
    }


if __name__ == "__main__":
    days = parse(fetch(USER))
    data = {
        "user": USER,
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "stats": stats(days),
        "days": days,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1))
    print(f"{len(days)} days, {data['stats']['total']} contributions -> {OUT}")
