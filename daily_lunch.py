import requests
import os
from datetime import datetime, timedelta, timezone

# ⏰ 한국 시간
KST = timezone(timedelta(hours=9))
now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# 🔑 Spoonacular API 키
API_KEY = os.getenv("FOOD")
if not API_KEY:
    raise ValueError("❌ 환경변수 'FOOD'가 설정되지 않았습니다.")

# 🍱 점심 메뉴 5개 요청
url = f"https://api.spoonacular.com/recipes/random?number=1&tags=lunch,korean&apiKey={API_KEY}"
res = requests.get(url)

main_title = main_image = main_url = ""
sub_menus = []

if res.status_code == 200:
    data = res.json().get("recipes", [])
    if len(data) >= 1:
        main = data[0]
        main_title = main.get('title', '제목 없음')
        main_image = main.get('image', '')
        main_url = main.get('sourceUrl', '')

    if len(data) > 1:
        sub_menus = [item.get('title', '메뉴 없음') for item in data[1:]]
else:
    main_title = "점심 메뉴를 불러오지 못했습니다."
    print(f"🚨 API 호출 실패: {res.status_code}")

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
            f.write(f"- {item}\n")
        f.write("\n")

    f.write("---\n")
    f.write("자동 점심봇 by Spoonacular API 🍱")
