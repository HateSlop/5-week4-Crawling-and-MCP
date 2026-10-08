"""
과제 2: 과제 1의 알라딘 크롤러를 MCP 서버로 만들기 🔌

할 일
  TODO 1. 과제 1의 크롤링 코드를 crawl_bestsellers() 함수 안으로 옮기기
  TODO 2. get_bestsellers()에 @mcp.tool()을 붙여서 AI가 쓸 수 있는 도구로 만들기
  TODO 3. get_bestsellers()의 docstring(도구 설명서)을 직접 쓰기

테스트 (5-week4 환경, 이 파일이 있는 폴더에서):
    python -c "from hw2_aladin_mcp import crawl_bestsellers; print(crawl_bestsellers(1)[:3])"
    npx @modelcontextprotocol/inspector@2.8.0 python hw2_aladin_mcp.py

제출: 이 파일 + Inspector에서 Execute Tool을 실행한 결과 캡처(hw2_inspector.png)

⚠️ 이 파일에서는 print()를 쓰지 마세요! (4장: stdio 서버는 stdout이 통신 채널)
"""
import time

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

URL = "https://www.aladin.co.kr/shop/common/wbest.aspx"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}


def crawl_bestsellers(pages: int = 1) -> list[dict]:
    """알라딘 베스트셀러를 pages 페이지만큼 가져와서 책 정보 리스트로 돌려줍니다."""
    params = {"BestType": "Bestseller", "BranchType": 1, "CID": 0, "page": 1, "cnt": 1000, "SortOrder": 1}
    rows = []

    for page in range(1, pages + 1):
        params["page"] = page
        response = requests.get(URL, params=params, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for book in soup.select(".ss_book_box"):
            try:
                title_tag = book.select_one("a.bo3")
                rows.append({
                    "title": title_tag.text.strip(),
                    "link": title_tag["href"],
                    "price": book.select_one("span.ss_p2").text.strip(),
                    "rating": book.select_one("span.star_score").text.strip(),
                })
            except AttributeError:
                continue
        
        time.sleep(0.5)

    return rows


# 서버 만들기: 이름은 AI 앱 화면에 표시됩니다
mcp = FastMCP("aladin-bestseller")

@mcp.tool()
def get_bestsellers(pages: int = 1) -> list[dict]:
    """알라딘 베스트셀러 목록을 가져옵니다.

    요즘 인기 있는 책이나 알라딘 베스트셀러 정보를 알고 싶을 때 사용합니다.

    Args:
        pages: 가져올 베스트셀러 페이지 수입니다. 1~3페이지를 지정할 수 있습니다.

    Returns:
        각 책의 제목(title), 링크(link), 할인가(price), 별점(rating)을
        담은 책 정보 리스트를 반환합니다.
    """
    pages = max(1, min(pages, 3))   # AI가 100페이지를 요청해도 3페이지까지만 (안전장치)
    return crawl_bestsellers(pages)


@mcp.tool()
def find_book(keyword: str) -> list[dict]:
    """알라딘 베스트셀러 중 제목에 키워드가 포함된 책을 찾습니다.

    베스트셀러 중 특정 주제나 단어가 제목에 들어간 책을 찾고 싶을 때 사용합니다.

    Args:
        keyword: 책 제목에서 찾을 키워드입니다.

    Returns:
        제목에 키워드가 포함된 책의 정보를 리스트로 반환합니다.
    """
    books = crawl_bestsellers(3)

    keyword = keyword.strip().lower()

    return [
        book
        for book in books
        if keyword in book["title"].lower()
    ]


if __name__ == "__main__":
    mcp.run()
