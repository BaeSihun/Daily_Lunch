import requests
import os
from datetime import datetime, timedelta, timezone

# ⏰ KST 시간
KST = timezone(timedelta(hours=9))
now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# 🔐 Spoonacular API 키 (환경변수: FOOD)
API_KEY = os.getenv("FOOD")
if not API_KEY:
    raise ValueError("❌ 환경변수 'FOOD'가 설정되지 않았습니다.")

# 📦 Spoonacular API 요청 (한식 점심 5개)
url = f"https://api.spoonacular.com/recipes/random?number=5&tags=lunch,korean&apiKey={API_KEY}"
res = requests.get(url)

recipes = []

if res.status_code == 200:
    data = res.json().get("recipes", [])
    for r in data:
        title = r.get("title", "Unknown")
        image = r.get("image", "")
        source_url = r.get("sourceUrl", "#")
        recipes.append((title, image, source_url))
else:
    print(f"🚨 API 호출 실패: {res.status_code}")
    print(res.text)

# 📄 README.md 생성
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 🍽️ 오늘의 점심 추천\n\n")
    f.write(f"🕒 **업데이트 시간:** {now} (KST)\n\n")

    if recipes:
        for idx, (title, image, url) in enumerate(recipes, start=1):
            f.write(f"## {idx}. [{title}]({url})\n\n")
            if image:
                f.write(f"![menu image]({image})\n\n")
    else:
        f.write("❌ 점심 메뉴를 불러오지 못했습니다.\n\n")

    f.write("---\n")
    f.write("자동 점심봇 by Spoonacular API 🍱")
