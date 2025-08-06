# update_lunch.py
import requests
from datetime import datetime, timedelta, timezone

# KST 기준 시간
KST = timezone(timedelta(hours=9))
now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# Spoonacular API 키 (GitHub Actions 환경변수에서 받을 예정)
import os
API_KEY = os.getenv("FOOD")

url = f"https://api.spoonacular.com/recipes/random?number=1&tags=lunch&apiKey={API_KEY}"
res = requests.get(url)

if res.status_code == 200:
    data = res.json()
    title = data['recipes'][0]['title']
    image = data['recipes'][0]['image']
    source_url = data['recipes'][0]['sourceUrl']
else:
    title = "점심 메뉴를 불러오지 못했습니다."
    image = ""
    source_url = ""

# README 업데이트
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 🥗 오늘의 점심 추천\n\n")
    f.write(f"**🕒 {now} (KST)**\n\n")
    f.write(f"🍽️ 오늘의 메뉴: **[{title}]({source_url})**\n\n")
    if image:
        f.write(f"![menu image]({image})\n\n")
    f.write("---\n")
    f.write("자동 점심봇 by Spoonacular API")
