# update_lunch.py
import requests
from datetime import datetime, timedelta, timezone

# KST 기준 시간
KST = timezone(timedelta(hours=9))
now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# Spoonacular API 키 (GitHub Actions 환경변수에서 받을 예정)
import os
API_KEY = os.getenv("FOOD")

url = f"https://api.spoonacular.com/recipes/random?number=1&tags=lunch,korean&apiKey={API_KEY}"
res = requests.get(url)


if res.status_code == 200:
    data = res.json()["recipes"]
    main = data[0]
    sub_menus = data[1:]  # 나머지 4개

    main_title = main['title']
    main_image = main['image']
    main_url = main['sourceUrl']
else:
    main_title = "점심 메뉴를 불러오지 못했습니다."
    main_image = ""
    main_url = ""
    sub_menus = []
    print("🚨 Spoonacular API 호출 실패:", res.status_code)

# 📄 README 작성
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 🥗 오늘의 점심 추천\n\n")
    f.write(f"**🕒 {now} (KST)**\n\n")
    f.write(f"🍽️ 오늘의 메뉴: **[{main_title}]({main_url})**\n\n")
    if main_image:
        f.write(f"![menu image]({main_image})\n\n")

    if sub_menus:
        f.write("📌 다른 추천 메뉴:\n")
        for item in sub_menus:
            f.write(f"- {item['title']}\n")
        f.write("\n")

    f.write("---\n")
    f.write("자동 점심봇 by Spoonacular API 🍱")