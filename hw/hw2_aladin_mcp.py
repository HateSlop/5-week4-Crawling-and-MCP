import time

import requests
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

URL = "https://www.aladin.co.kr/shop/common/wbest.aspx"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
}


def crawl_bestsellers(pages: int = 1) -> list[dict]:
    """알라딘 베스트셀러를 pages 페이지만큼 가져와서 책 정보 리스트로 돌려줍니다."""
    params = {
        "BestType": "Bestseller",
        "BranchType": 1,
        "CID": 0,
        "page": 1,
        "cnt": 1000,
        "SortOrder": 1
    }

    rows = []

    for page in range(1, pages + 1):
        params["page"] = page

        response = requests.get(URL, headers=HEADERS, params=params)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.select("div.ss_book_box")

        for book in books:
            try:
                title_tag = book.select_one("a.bo3")
                title = title_tag.text.strip()
                link = title_tag["href"]

                price = book.select_one("span.ss_p2").text.strip()
                rating = book.select_one("span.star_score").text.strip()

                rows.append({
                    "title": title,
                    "link": link,
                    "price": price,
                    "rating": rating
                })

            except Exception:
                continue

        time.sleep(0.5)

    return rows


mcp = FastMCP("aladin-bestseller")


@mcp.tool()
def get_bestsellers(pages: int = 1) -> list[dict]:
    """
    알라딘 베스트셀러 목록을 조회합니다.

    요즘 인기 있는 책이나 베스트셀러 정보를 알고 싶을 때 사용합니다.

    Args:
        pages: 가져올 페이지 수입니다. 1~3 범위로 사용할 수 있습니다.

    Returns:
        각 책의 제목, 링크, 할인가, 별점을 담은 딕셔너리 리스트를 반환합니다.
    """
    pages = max(1, min(pages, 3))
    return crawl_bestsellers(pages)


if __name__ == "__main__":
    mcp.run()