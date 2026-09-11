#!/usr/bin/env python3
import json, re, sys
from datetime import datetime, date, timedelta
import requests
from bs4 import BeautifulSoup

USERNAME = "abhay23459"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = "data/contributions.json"

def level_from_count(n):
    if n <= 0: return 0
    if n <= 2: return 1
    if n <= 5: return 2
    if n <= 9: return 3
    return 4

r = requests.get(URL, timeout=30, headers={"User-Agent":"abhay23459-profile-art/1.0"})
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

days=[]
for el in soup.select("[data-date]"):
    ds=el.get("data-date")
    if not ds or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", ds):
        continue
    raw=el.get("data-count")
    if raw is None:
        raw=el.get("data-level")
        if raw is not None:
            try: count=int(raw)
            except: count=0
        else:
            label=el.get("aria-label","")
            m=re.search(r"(\d[\d,]*)\s+contribution", label)
            count=int(m.group(1).replace(",","")) if m else 0
    else:
        try: count=int(raw)
        except: count=0
    days.append({"date":ds,"count":count,"level":level_from_count(count)})

# De-duplicate by date
uniq={d["date"]:d for d in days}
days=[uniq[k] for k in sorted(uniq)]

# Stats
counts=[d["count"] for d in days]
total=sum(counts)
best=max(days,key=lambda d:d["count"],default=None)

def streaks(items):
    active={datetime.strptime(d["date"],"%Y-%m-%d").date() for d in items if d["count"]>0}
    longest=current=0
    today=date.today()
    for d in sorted(active):
        if d-timedelta(days=1) in active:
            current += 1
        else:
            current = 1
        longest=max(longest,current)
    cur=0
    d=today
    while d in active:
        cur+=1; d-=timedelta(days=1)
    return cur,longest

current,longest=streaks(days)
monthly={}
for d in days:
    monthly[d["date"][:7]]=monthly.get(d["date"][:7],0)+d["count"]

payload={
    "username":USERNAME,
    "fetched_at":datetime.utcnow().isoformat()+"Z",
    "total_last_year":total,
    "days":days,
    "current_streak":current,
    "longest_streak":longest,
    "best_day":best,
    "monthly_totals":monthly
}
with open(OUT,"w",encoding="utf-8") as f: json.dump(payload,f,indent=2)
print(f"Wrote {len(days)} days, {total} contributions -> {OUT}")
