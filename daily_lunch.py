import requests, os, random
from datetime import datetime, timedelta, timezone

# ⏰ 한국 시간
KST = timezone(timedelta(hours=9))
now = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

# 🔐 Spoonacular API 키
API_KEY = os.getenv("FOOD")
if not API_KEY:
    raise ValueError("❌ 환경변수 'FOOD'가 설정되지 않았습니다.")

# ✅ 한국인 선호 메뉴 키워드
preferred_keywords = [
    # 한식
    "kimchi", "bulgogi", "bibimbap", "tteokbokki", "galbi", "samgyeopsal",
    "gochujang", "japchae", "soy sauce", "korean", "kimchi stew", "doenjang",
    "soondubu", "dakgalbi", "kalbi", "gimbap", "rice bowl", "stir fry",
    "spicy chicken", "seaweed soup", "pork belly",

    # 양식/퓨전
    "pasta", "carbonara", "tomato pasta", "pizza", "cheese", "hamburger",
    "burger", "steak", "steak rice", "cutlet", "chicken cutlet", "salad",
    "egg", "omelette", "gratin", "risotto", "wrap", "bowl", "hotdog", "meatball",

    # 아시아 요리
    "ramen", "noodle", "udon", "japanese", "donburi", "teriyaki",
    "chicken katsu", "curry", "thai", "pad thai", "pho", "spring roll",
    "vietnamese", "rice noodle", "laksa",

    # 기타
    "fried rice", "soy garlic", "katsu", "baked rice", "mapo tofu",
    "spicy", "soup", "casserole", "mayo", "corn cheese"
]

def is_preferred(title: str) -> bool:
    return any(keyword in title.lower() for keyword in preferred_keywords)

# 📦 Spoonacular API 요청
url = f"https://api.spoonacular.com/recipes/random?number=10&tags=lunch&cuisine=korean&apiKey={API_KEY}"
res = requests.get(url)

recipes = []

if res.status_code == 200:
    data = res.json().get("recipes", [])
    filtered = [r for r in data if is_preferred(r.get("title", ""))]
    final = random.sample(filtered, k=min(5, len(filtered)))

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
