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

        # TODO 1: 과제 1의 Step 6 안쪽 코드를 옮겨오세요.
        #   - requests로 요청 → BeautifulSoup으로 파싱
        #   - 책 덩어리마다 title, link, price, rating을 딕셔너리로 만들어 rows에 추가
        #   - 정보가 빠진 책은 try-except로 건너뛰기

        response = requests.get(URL, params=params, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for book in soup.select(".ss_book_box"):
            try:
                title_tag = book.select_one(".bo3")
                rows.append({
                    "title": title_tag.text.strip(),
                    "link": title_tag["href"],
                    "price": book.select_one(".ss_p2").text.strip(),
                    "rating": book.select_one(".star_score").text.strip(),
                })
            except AttributeError:
                continue

        time.sleep(0.5)

    return rows


# 서버 만들기: 이름은 AI 앱 화면에 표시됩니다
mcp = FastMCP("aladin-bestseller")


# TODO 2: 아래 함수 위에 한 줄을 붙여서 MCP 도구로 만드세요
@mcp.tool()
def get_bestsellers(pages: int = 1) -> list[dict]:
    """TODO 3: AI가 읽을 도구 설명서를 쓰세요.

    알라딘 인터넷 서점의 현재 종합 베스트셀러 목록을 가져오는 도구입니다.
      
    사용자가 "요즘 인기 있는 책 알려줘", "알라딘 베스트셀러 찾아줘"와 같이 최근 트렌드나 인기 도서 정보를 요청할 때 사용하세요.
    
    Args:
        pages: 가져올 베스트셀러 목록의 페이지 수입니다. 1페이지당 약 50권의 책 정보를 포함합니다.기본값은 1이며, 최대 3페이지(약 150권)까지만 요청할 수 있습니다.
               
    Returns:
        각 책의 제목(title), 도서 링크(link), 할인가(price), 별점(rating) 정보를 포함하는 딕셔너리들의 리스트를 반환합니다.
    """
    pages = max(1, min(pages, 3))   # AI가 100페이지를 요청해도 3페이지까지만 (안전장치)
    return crawl_bestsellers(pages)


if __name__ == "__main__":
    mcp.run()
