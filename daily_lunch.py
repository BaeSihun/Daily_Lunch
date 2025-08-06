import requests
import os
from datetime import datetime, timedelta, timezone

#KST 시간
KST = timezone(timedelta(hours=9))
now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# API 키
API_KEY = os.getenv("FOOD")
if not API_KEY:
    raise ValueError("❌ 환경변수 'FOOD'가 설정되지 않았습니다.")

# Spoonacular API 요청 (한식 점심 메뉴 5개)
url = f"https://api.spoonacular.com/recipes/random?number=5&tags=lunch,korean&apiKey={API_KEY}"
res = requests.get(url)

# 기본값
main_title = "점심 메뉴를 불러오지 못했습니다."
main_image = ""
main_url = ""
sub_titles = []

# 응답 파싱
if res.status_code == 200:
    recipes = res.json().get("recipes", [])

    if len(recipes) >= 1:
        main = recipes[0]
        main_title = main.get("title", "제목 없음")
        main_image = main.get("image", "")
        main_url = main.get("sourceUrl", "")

        # 추가 추천 메뉴 (최대 4개)
        for r in recipes[1:5]:
            title = r.get("title")
            if title:
                sub_titles.append(title)
else:
    print(f"🚨 API 호출 실패: {res.status_code}")
    print(res.text)

# README 작성
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 🥗 오늘의 점심 추천\n\n")
    f.write(f"**🕒 {now} (KST)**\n\n")
    f.write(f"🍽️ 오늘의 메뉴: **[{main_title}]({main_url})**\n\n")
    if main_image:
        f.write(f"![menu image]({main_image})\n\n")

    if sub_titles:
        f.write("📌 다른 추천 메뉴:\n")
        for title in sub_titles:
            f.write(f"- {title}\n")
        f.write("\n")

    f.write("---\n")
    f.write("자동 점심봇 by Spoonacular API 🍱")
