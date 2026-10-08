"""
MCP 클라이언트 예제: AI 앱(Host)이 내부에서 하는 일을 파이썬으로 직접 해봅니다.

1) 서버 프로세스를 띄우고  2) 어떤 도구가 있는지 물어보고  3) 도구를 호출합니다.
Node.js가 없어 Inspector를 못 쓰는 경우에도 이 파일로 서버를 테스트할 수 있습니다.

실행: python mcp_client.py
"""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 지금 쓰고 있는 파이썬(가상환경)으로, 이 파일 옆의 서버를 실행
SERVER_FILE = Path(__file__).with_name("kin_mcp_server.py")
server = StdioServerParameters(command=sys.executable, args=[str(SERVER_FILE)])


async def main():
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()  # 악수: 서로 버전과 기능 확인

            # 1. 도구 목록 요청 (tools/list)
            tools = await session.list_tools()
            print("=== 서버가 제공하는 도구 ===")
            for tool in tools.tools:
                print(f"- {tool.name}")
                print(f"  입력 형식: {json.dumps(tool.inputSchema['properties'], ensure_ascii=False)}")

            # 2. 도구 호출 (tools/call): AI라면 사용자의 말을 보고 이 인자들을 스스로 채웁니다.
            print("\n=== search_kin 호출 결과 ===")
            result = await session.call_tool("search_kin", {"query": "삼성전자", "pages": 1})

            if result.isError:
                print("에러:", result.content[0].text)
                return

            questions = result.structuredContent["result"]
            for q in questions[:5]:
                print(f"[{q['category']}] {q['title']} (답변 {q['answers']}) - {q['date']}")
            print(f"... 총 {len(questions)}개")


if __name__ == "__main__":
    asyncio.run(main())
