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

        for book in soup.select("div.ss_book_box"):
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


# TODO 2: 아래 함수 위에 한 줄을 붙여서 MCP 도구로 만드세요
def get_bestsellers(pages: int = 1) -> list[dict]:
    """알라딘 온라인 서점의 주간 베스트셀러(국내도서) 목록을 실시간으로 가져옵니다.

    언제 쓰나요:
      - 사용자가 요즘 인기 있는 책, 잘 팔리는 책, 베스트셀러를 물어볼 때
      - 책 추천을 요청받았을 때 최신 인기 도서를 근거로 삼고 싶을 때
        (예: "요즘 베스트셀러 중에 경제 관련 책 추천해줘")

    입력값:
      pages (int): 가져올 페이지 수. 1페이지에 50위까지 들어 있습니다.
        1이면 1~50위, 2면 1~100위, 3이면 1~150위. 범위는 1~3이며 기본값은 1입니다.
        3보다 큰 값을 넣어도 3페이지까지만 가져옵니다.

    돌려주는 값:
      책 정보 딕셔너리의 리스트. 순위 순서대로 정렬되어 있습니다.
        [{"title": "책 제목",
          "link": "알라딘 상품 페이지 URL",
          "price": "할인가 (예: '16,650원')",
          "rating": "별점, 10점 만점 (예: '8.9')"}, ...]
      별점이 아직 없는 신간이나 세트 상품은 목록에서 빠지므로,
      한 페이지에 50권보다 적게 나올 수 있습니다.
    """
    pages = max(1, min(pages, 3))   # AI가 100페이지를 요청해도 3페이지까지만 (안전장치)
    return crawl_bestsellers(pages)


if __name__ == "__main__":
    mcp.run()
