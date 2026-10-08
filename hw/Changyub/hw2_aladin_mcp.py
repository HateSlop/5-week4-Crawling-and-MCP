"""알라딘 베스트셀러 크롤러를 AI가 호출하는 stdio MCP 서버로 제공합니다.

실행: python hw2_aladin_mcp.py
검증: npx @modelcontextprotocol/inspector@2.8.0 python hw2_aladin_mcp.py
"""

import time

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

URL = "https://www.aladin.co.kr/shop/common/wbest.aspx"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    )
}


def crawl_bestsellers(pages: int = 1) -> list[dict]:
    """국내도서 종합 주간 베스트셀러의 첫 1~3페이지를 순서대로 수집합니다."""
    pages = max(1, min(pages, 3))
    params = {
        "BestType": "Bestseller",
        "BranchType": 1,
        "CID": 0,
        "page": 1,
        "cnt": 1000,
        "SortOrder": 1,
    }
    rows = []

    for page in range(1, pages + 1):
        params["page"] = page
        response = requests.get(URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select(".ss_book_box")
        if not books:
            raise ValueError(f"{page}페이지의 책 목록을 찾지 못했습니다. HTML을 확인하세요.")

        for book in books:
            try:
                title_tag = book.select_one("a.bo3")
                row = {
                    "title": title_tag.get_text(strip=True),
                    "link": title_tag["href"].strip(),
                    "price": book.select_one(".ss_p2").get_text(strip=True),
                    "rating": book.select_one(".star_score").get_text(strip=True),
                }
                if not all(row.values()):
                    continue
                rows.append(row)
            except (AttributeError, KeyError):
                # 별점이 없는 신간 등은 건너뛰되, HTTP 오류는 숨기지 않습니다.
                continue

        if page < pages:
            time.sleep(0.5)  # 연속 요청 사이에 쉬어 서버 부담을 줄입니다.

    return rows


mcp = FastMCP("aladin-bestseller")


@mcp.tool()
def get_bestsellers(pages: int = 1) -> list[dict]:
    """알라딘 국내도서 종합 주간 베스트셀러를 조회합니다.

    요즘 많이 구매하는 책의 제목, 구매 링크, 할인가, 별점이 궁금할 때 사용하세요.
    호출할 때 웹에서 새로 수집하며, 필수 정보가 없는 책은 결과에서 제외합니다.

    Args:
        pages: 첫 페이지부터 가져올 페이지 수. 기본값 1, 범위 1~3.
            범위를 벗어나면 1~3으로 보정합니다. 한 페이지는 최대 50권입니다.

    Returns:
        페이지 및 순위 순서의 책 딕셔너리 목록. 각 책은 title(제목),
        link(상세 페이지 URL), price(원 단위 할인가 문자열, 예: "16,650원"),
        rating(10점 만점 별점 문자열, 예: "8.9")을 가집니다.
    """
    return crawl_bestsellers(pages)


@mcp.tool()
def find_book(keyword: str, pages: int = 3) -> list[dict]:
    """알라딘 주간 베스트셀러 중 제목에 키워드가 들어간 책을 찾습니다.

    특정 단어가 제목에 포함된 인기 도서를 찾을 때 사용하세요.
    알라딘 전체 도서 검색이 아니라 베스트셀러 첫 1~3페이지에서만 검색합니다.

    Args:
        keyword: 비어 있지 않은 제목 검색어 (예: "트렌드"). 앞뒤 공백을
            제거하고 영문 대소문자를 구분하지 않습니다.
        pages: 수집할 페이지 수. 기본값 3, 범위 1~3이며 범위 밖은 보정합니다.

    Returns:
        제목에 키워드를 포함한 책 목록. title, link, price, rating 문자열을
        포함하며 일치하는 책이 없으면 빈 목록을 반환합니다.
    """
    keyword = keyword.strip().casefold()
    if not keyword:
        raise ValueError("keyword에는 비어 있지 않은 검색어를 입력하세요.")
    return [row for row in crawl_bestsellers(pages) if keyword in row["title"].casefold()]


if __name__ == "__main__":
    # stdout은 MCP 통신 전용입니다. 일반 출력이나 CSV 저장을 하지 않습니다.
    mcp.run(transport="stdio")
