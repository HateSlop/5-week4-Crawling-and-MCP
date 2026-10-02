#!/usr/bin/env python
# coding: utf-8

# # 과제 1: 알라딘 베스트셀러 정적 크롤링 📚
# 
# 2장에서 배운 requests + BeautifulSoup으로 알라딘 베스트셀러의 **제목, 링크, 할인가, 별점**을 1~3페이지에서 모아 CSV로 저장합니다.
# 
# | Step | 할 일 |
# |---|---|
# | 1 | 라이브러리 준비 |
# | 2 | HTML 받아오기 |
# | 3 | 책 **한 권** 덩어리 찾기 |
# | 4 | 한 권에서 제목, 링크, 할인가, 별점 뽑기 |
# | 5 | 한 페이지의 책 **전부** 뽑기 |
# | 6 | **여러 페이지** 뽑기 |
# | 7 | DataFrame으로 정리하고 CSV 저장 |
# 
# > ✏️ `____` 빈칸을 채우세요. 셀렉터는 **크롬 개발자 도구**(1장)로 직접 찾아야 합니다!

# ## Step 1. 라이브러리 준비

# In[1]:


import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.aladin.co.kr/shop/common/wbest.aspx"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}


# ## Step 2. HTML 받아오기
# 
# 베스트셀러 주소 `...wbest.aspx?BestType=Bestseller&BranchType=1&...` 에서 `?` 뒤의 옵션들을 `params` 딕셔너리로 정리했어요.
# 
# 💡 2장 복습: `requests.get(주소, params=..., headers=..., timeout=10)`

# In[2]:


params = {
    "BestType": "Bestseller",
    "BranchType": 1,
    "CID": 0,
    "page": 1,
    "cnt": 1000,
    "SortOrder": 1
}

response = requests.get(
    URL,
    params=params,
    headers=HEADERS,
    timeout=10
)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")


# ## Step 3. 책 한 권 덩어리 찾기
# 
# 개발자 도구로 첫 번째 책을 찍어보고, **책 한 권 전체를 감싸는 상자**를 찾으세요.
# 
# 💡 힌트: 책마다 **똑같은 class 이름으로 반복되는** 상자가 있어요. 2장 지식인의 `.basic1 > li > dl`처럼요.

# In[3]:


book = soup.select_one(".ss_book_box")
print(book.prettify()[:2000])


# ## Step 4. 한 권에서 제목, 링크, 할인가, 별점 뽑기
# 
# - 제목과 링크는 같은 `a` 태그에 있어요: 글자는 `.text`, 주소는 `["href"]`
# - 할인가, 별점도 개발자 도구로 class를 찾아보세요

# In[5]:


title_tag = book.select_one("a.bo3")
title = title_tag.text.strip()
link = title_tag["href"]
price = book.select_one(".ss_p2").text.strip()
rating = book.select_one(".star_score").text.strip()

print(title, link, price, rating, sep=" | ")


# ## Step 5. 한 페이지의 책 전부 뽑기
# 
# `select`로 책 덩어리를 **전부** 찾고, for문으로 Step 4를 반복합니다.
# 
# ⚠️ **예외 처리**: 신간은 아직 별점이 없는 등, 모든 책의 정보가 똑같지 않아요. 정보가 빠진 책을 만나면 `select_one`이 `None`을 돌려주고, 거기에 `.text`를 붙이면 `AttributeError`가 납니다. `try-except`로 그런 책은 건너뛰세요.

# In[6]:


books = soup.select(".ss_book_box")
print(len(books), "권 찾음")

rows = []

for book in books:
    try:
        title_tag = book.select_one("a.bo3")

        rows.append({
            "title": title_tag.text.strip(),
            "link": title_tag["href"],
            "price": book.select_one(".ss_p2").text.strip(),
            "rating": book.select_one(".star_score").text.strip(),
        })

    except AttributeError:
        continue

print(len(rows), "권 저장")
rows[:3]


# ## Step 6. 여러 페이지 뽑기
# 
# `params["page"]` 숫자만 바꿔가며 1~3페이지를 반복합니다. 요청 사이에는 `time.sleep()`으로 꼭 쉬어주세요!

# In[8]:


rows = []

for page in range(1, 4):
    params["page"] = page

    response = requests.get(
        URL,
        params=params,
        headers=HEADERS,
        timeout=10
    )

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

        except AttributeError:
            continue

    print(f"{page}페이지 완료, 지금까지 {len(rows)}권")
    time.sleep(1)


# ## Step 7. DataFrame으로 정리하고 CSV 저장
# 
# 💡 윈도우 엑셀에서 한글이 안 깨지게 하는 인코딩, 2장에서 배웠죠?

# In[9]:


df = pd.DataFrame(rows)

df.to_csv(
    "aladin.csv",
    index=False,
    encoding="utf-8-sig"
)

df.head()


# ## 제출 전: .py로 변환하기
# 
# 코드 리뷰를 위해 노트북을 `.py` 파일로 변환해서 제출합니다. 터미널에서 이 노트북이 있는 폴더로 이동한 뒤:
# 
# ```bash
# python -m jupyter nbconvert --to script hw1_aladin.ipynb
# ```
