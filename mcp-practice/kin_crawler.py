"""
2장에서 만든 네이버 지식인 크롤러를 함수로 정리한 버전입니다.
MCP 서버(kin_mcp_server.py)는 이 파일의 crawl_kin 함수를 그대로 가져다 씁니다.

단독 실행: python kin_crawler.py
"""
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://kin.naver.com/search/list.naver"
HEADERS = {
    # User-Agent가 없으면 봇으로 판단해 막는 사이트가 많습니다.
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
    )
}


def _text(tag) -> str:
    """태그가 없으면(None) 빈 문자열을 돌려줍니다. 셀렉터가 하나 틀려도 전체가 죽지 않게 하기 위함."""
    return tag.get_text(strip=True) if tag else ""


def parse_kin_page(html: str) -> list[dict]:
    """지식인 검색 결과 HTML 한 페이지에서 질문 목록을 뽑아냅니다."""
    soup = BeautifulSoup(html, "html.parser")
    questions = []

    for item in soup.select(".basic1 > li > dl"):
        title_tag = item.select_one("._nclicks\\:qna\\.txt")
        hit_words = _text(item.select_one(".hit")).split()  # 예: "답변수 3" -> ["답변수", "3"]

        questions.append({
            "title": _text(title_tag),
            "link": title_tag["href"] if title_tag else "",
            "date": _text(item.select_one(".txt_inline")),
            "category": _text(item.select_one("._nclicks\\:qna\\.cat2")),
            "answers": hit_words[-1] if hit_words else "",
        })

    return questions


def crawl_kin(query: str, pages: int = 1) -> list[dict]:
    """검색어로 지식인을 검색해 pages 페이지만큼 질문 목록을 가져옵니다."""
    results = []
    for page in range(1, pages + 1):
        response = requests.get(
            BASE_URL,
            params={"query": query, "page": page},  # 한글 검색어도 requests가 알아서 인코딩
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()  # 200이 아니면 여기서 에러
        results.extend(parse_kin_page(response.text))
        time.sleep(0.5)  # 서버에 부담 주지 않도록 페이지 사이에 잠깐 쉬기
    return results


if __name__ == "__main__":
    for row in crawl_kin("삼성전자", pages=1):
        print(row)
