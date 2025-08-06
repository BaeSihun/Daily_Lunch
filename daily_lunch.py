import requests, os, random
from datetime import datetime, timedelta, timezone

# ⏰ 한국 시간
KST = timezone(timedelta(hours=9))
now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# 🔐 API 키
API_KEY = os.getenv("FOOD")
if not API_KEY:
    raise ValueError("❌ 환경변수 'FOOD'가 설정되지 않았습니다.")

# 📦 Spoonacular API 요청 (한국인들이 자주 먹는 메뉴 기반)
tags = "lunch,korean,bibimbap,bulgogi,kimchi,pork,ramen,noodle,rice,stir-fry,soup,spicy"
url = f"https://api.spoonacular.com/recipes/random?number=10&tags={tags}&cuisine=korean&apiKey={API_KEY}"
res = requests.get(url)

recipes = []

if res.status_code == 200:
    data = res.json().get("recipes", [])
    final = random.sample(data, k=min(5, len(data)))

    for r in final:
        title = r.get("title", "No Title")
        image = r.get("image", "")
        source = r.get("sourceUrl", "#")
        recipes.append((title, image, source))
else:
    print("🚨 API 호출 실패:", res.status_code)
    print(res.text)

# 📄 README.md 생성
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 🍱 오늘의 점심 추천\n\n")
    f.write(f"🕒 업데이트 시간: {now} (KST)\n\n")

    if recipes:
        for i, (title, img, url) in enumerate(recipes, 1):
            f.write(f"## {i}. [{title}]({url})\n\n")
            if img:
                f.write(f"![menu image]({img})\n\n")
    else:
        f.write("❌ 조건에 맞는 점심 메뉴가 없습니다.\n\n")

    f.write("---\n자동 점심봇 by Spoonacular API 🍽️")
