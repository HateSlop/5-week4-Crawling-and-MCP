"""알라딘 베스트셀러 크롤러를 MCP 도구로 제공한다."""

import time

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

URL = "https://www.aladin.co.kr/shop/common/wbest.aspx"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
}


def crawl_bestsellers(pages: int = 1) -> list[dict]:
    """요청한 페이지 수만큼 베스트셀러의 제목, 링크, 할인가, 별점을 수집한다."""
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

        for book in soup.select(".ss_book_box"):
            try:
                title_tag = book.select_one("a.bo3")
                rows.append(
                    {
                        "title": title_tag.get_text(strip=True),
                        "link": title_tag["href"],
                        "price": book.select_one(".ss_p2").get_text(strip=True),
                        "rating": book.select_one(".star_score").get_text(strip=True),
                    }
                )
            except (AttributeError, TypeError, KeyError):
                continue

        if page < pages:
            time.sleep(0.5)

    return rows

mcp = FastMCP("aladin-bestseller")


@mcp.tool()
def get_bestsellers(pages: int = 1) -> list[dict]:
    """요즘 인기 있는 책이 궁금할 때 알라딘 베스트셀러를 조회한다.

    Args:
        pages: 조회할 페이지 수. 1~3 범위로 제한하며 기본값은 1이다.

    Returns:
        책마다 title, link, price, rating을 담은 딕셔너리의 리스트.
        필수 정보가 없는 책은 제외한다.
    """
    pages = max(1, min(pages, 3))
    return crawl_bestsellers(pages)


if __name__ == "__main__":
    mcp.run()
