import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.aladin.co.kr/shop/common/wbest.aspx"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}

params = {"BestType": "Bestseller", "BranchType": 1, "CID": 0, "page": 1, "cnt": 1000, "SortOrder": 1}

rows = []
for page in range(1, 4):
    params["page"] = page
    response = requests.get(URL, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select(".ss_book_box"):
        try:
            title_tag = book.select_one("a.bo3")
            rows.append({
                "title": title_tag.text.strip(),
                "link": title_tag["href"],
                "price": book.select_one(".ss_p2").text.strip(),
                "rating": book.select_one(".star_score").text.strip(),
            })
        except (AttributeError, TypeError, KeyError):
            continue

    print(f"{page}페이지 완료, 지금까지 {len(rows)}권")
    if page < 3:
        time.sleep(0.5)

df = pd.DataFrame(rows)
df.to_csv("aladin.csv", index=False, encoding="utf-8-sig")
