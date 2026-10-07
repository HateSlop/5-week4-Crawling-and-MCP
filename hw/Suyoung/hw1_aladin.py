import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.aladin.co.kr/shop/common/wbest.aspx"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}

params = {"BestType": "Bestseller", "BranchType": 1, "CID": 0, "page": 1, "cnt": 1000, "SortOrder": 1}

response = ____
print(response.status_code)   # 200이면 성공

soup = ____

book = soup.select_one("____")
print(book.prettify()[:2000])

title_tag = book.select_one("____")
title = title_tag.____.strip()
link = title_tag[____]
price = book.select_one("____").text.strip()
rating = book.select_one("____").text.strip()

print(title, link, price, rating, sep=" | ")

books = soup.____("____")
print(len(books), "권 찾음")

rows = []
for book in books:
    try:
        title_tag = book.select_one("____")
        rows.append({
            "title": ____,
            "link": ____,
            "price": ____,
            "rating": ____,
        })
    except ____:
        continue   # 정보가 빠진 책은 건너뛰기

print(len(rows), "권 저장")
rows[:3]

rows = []
for page in range(1, 4):
    params["page"] = ____
    response = ____
    soup = ____

    for book in soup.select("____"):
        try:
            title_tag = book.select_one("____")
            rows.append({
                "title": title_tag.text.strip(),
                "link": title_tag["href"],
                "price": book.select_one("____").text.strip(),
                "rating": book.select_one("____").text.strip(),
            })
        except AttributeError:
            continue

    print(f"{page}페이지 완료, 지금까지 {len(rows)}권")
    time.sleep(____)

df = pd.____(rows)
df.to_csv("aladin.csv", index=False, encoding="____")
df.head()
