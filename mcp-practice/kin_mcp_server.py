"""
네이버 지식인 크롤러를 MCP 서버로 만든 예제입니다.

크롤링 코드는 한 줄도 바뀌지 않았습니다.
kin_crawler.py의 함수를 가져와서 @mcp.tool()을 붙였을 뿐입니다.

실행 (MCP Inspector로 테스트):
    npx @modelcontextprotocol/inspector python kin_mcp_server.py
"""
from mcp.server.fastmcp import FastMCP

from kin_crawler import crawl_kin

# 1. 서버 만들기: 이름은 AI 앱(Host) 화면에 표시됩니다.
mcp = FastMCP("naver-kin")


# 2. 함수에 @mcp.tool()을 붙이면 AI가 호출할 수 있는 '도구(tool)'가 됩니다.
#    - 함수 이름      -> 도구 이름
#    - 타입 힌트      -> 입력 형식(JSON Schema)
#    - docstring     -> AI가 읽는 도구 설명서. AI는 이걸 보고 언제, 어떻게 쓸지 판단합니다.
@mcp.tool()
def search_kin(query: str, pages: int = 1) -> list[dict]:
    """네이버 지식인에서 질문을 검색합니다.

    사람들이 특정 주제에 대해 어떤 질문을 하는지 알고 싶을 때 사용하세요.

    Args:
        query: 검색어 (예: "삼성전자", "파이썬 설치")
        pages: 가져올 결과 페이지 수. 1~3 사이 (한 페이지에 약 10개)

    Returns:
        질문 목록. 각 질문은 title(제목), link(링크), date(날짜),
        category(카테고리), answers(답변 수)를 가집니다.
    """
    pages = max(1, min(pages, 3))  # AI가 100페이지를 요청해도 3페이지까지만
    return crawl_kin(query, pages)


# 3. 서버 실행: 기본값은 stdio (표준 입출력으로 AI 앱과 대화)
#    ⚠️ stdio 서버에서는 print()를 쓰면 안 됩니다! stdout이 곧 통신 채널이라 메시지가 깨집니다.
if __name__ == "__main__":
    mcp.run()
