# 4장 MCP 실습

2장에서 만든 네이버 지식인 크롤러를 **MCP 서버**로 만들어, AI가 호출할 수 있는 도구로 바꿔봅니다.

## 파일 구성

| 파일 | 역할 | MCP에서의 위치 |
|---|---|---|
| `kin_crawler.py` | 2장 지식인 크롤러를 함수로 정리 | (그냥 파이썬 코드) |
| `kin_mcp_server.py` | 크롤러에 `@mcp.tool()`을 붙인 서버 | **Server** |
| `mcp_client.py` | 서버에 접속해 도구 목록 조회, 호출 | **Client** (AI 앱이 내부에서 하는 일) |
| `../.vscode/mcp.json` | VS Code + Copilot 연결 설정 | Host 설정 |
| `claude_desktop_config.example.json` | Claude Desktop 연결 설정 예시 | Host 설정 |

## 준비물

| 항목 | 버전 / 설명 |
|---|---|
| conda 환경 | Python **3.12** |
| Node.js | **22.19 이상** (MCP Inspector 요구사항). `node -v`로 확인 |
| VS Code | 최신 버전 (Help → Check for Updates) |
| GitHub Copilot | VS Code 확장. GitHub 계정으로 로그인하면 무료 플랜(Copilot Free) 사용 가능 |

```bash
conda create -n 5-week4 python=3.12
conda activate 5-week4
pip install -r requirements.txt
playwright install chromium
```

> Windows PowerShell에서 `conda activate`가 안 되면 `conda init powershell`을 한 번 실행하고 터미널을 새로 여세요.

## 실습 1. 크롤러 단독 실행

```bash
conda activate 5-week4
cd mcp-practice
python kin_crawler.py
```

질문 10개 정도가 `{'title': ..., 'link': ..., 'category': ...}` 형태로 나오면 성공입니다.

## 실습 2. MCP Inspector로 도구 호출하기

```bash
npx @modelcontextprotocol/inspector@2.8.0 python kin_mcp_server.py
```

> 버전(`@2.8.0`)을 고정하는 이유: `npx`는 실행할 때마다 최신 버전을 받아와서 화면 구성이 바뀔 수 있습니다.

1. 브라우저에 Inspector가 열리면 `python` 서버 카드의 **토글 스위치**를 켭니다 → **Connected**
2. 서버 카드를 클릭해 상세 화면으로 들어갑니다
3. **Tools** 탭 → `search_kin` 선택
4. `query`에 검색어 입력 → 실행 → 결과 JSON 확인

> `conda activate` 한 터미널에서, `mcp-practice` 폴더 안에서 실행하세요. 그렇지 않으면 `No module named 'mcp'` 에러가 나거나 서버 파일을 찾지 못합니다.

## 실습 2-1. Node.js 없이 테스트하기

```bash
python mcp_client.py
```

`Processing request of type ...` 줄은 서버가 남기는 로그(stderr)라서 무시해도 됩니다.

## 실습 3. VS Code + Copilot에서 AI가 직접 호출하기

### 3-1. 설정 파일의 파이썬 경로 맞추기

AI 앱은 conda 환경을 활성화하지 않고 서버를 실행합니다.
그래서 `.vscode/mcp.json`에 **conda 환경 안의 파이썬 경로**를 직접 적어야 합니다.

```bash
conda activate 5-week4
python -c "import sys; print(sys.executable)"
```

출력된 경로를 `.vscode/mcp.json`의 `naver-kin` → `command`에 넣습니다.

| 설치 환경 | `command` 예시 |
|---|---|
| Windows + Anaconda | `C:\\Users\\내이름\\anaconda3\\envs\\5-week4\\python.exe` |
| Windows + Miniconda | `C:\\Users\\내이름\\miniconda3\\envs\\5-week4\\python.exe` |
| Mac + Miniconda | `${userHome}/miniconda3/envs/5-week4/bin/python` |
| Mac + Anaconda | `${userHome}/anaconda3/envs/5-week4/bin/python` 또는 `/opt/anaconda3/envs/5-week4/bin/python` |

- Windows는 역슬래시를 두 번(`\\`) 써야 합니다.
- `${userHome}`(홈 폴더), `${workspaceFolder}`(VS Code로 연 폴더)는 VS Code가 자동으로 채워줍니다.

### 3-2. 서버 시작하고 AI에게 시키기

1. VS Code에서 **레포 최상위 폴더**를 엽니다 (`.vscode`와 `mcp-practice`가 바로 보이는 폴더)
2. `.vscode/mcp.json`을 열고 `"naver-kin"` 위의 **▷ Start** 클릭 → 신뢰 확인 창에서 **Trust** → **Running** 확인
3. Copilot Chat(`Ctrl+Alt+I`)을 열고 모드를 **Agent**로 변경
4. 입력칸 옆 🔧 도구 아이콘에서 `search_kin`이 체크돼 있는지 확인
5. 질문하기:
   > 네이버 지식인에서 "파이썬 설치" 관련 질문들 찾아서 사람들이 주로 어떤 걸 어려워하는지 요약해줘
6. `search_kin` 실행 허락을 물으면 **Allow** → AI가 결과를 받아 요약하면 성공

AI가 도구를 안 쓰고 대답하면 질문에 `#search_kin`을 넣어 직접 지정하세요.

## 시연. Playwright MCP

`.vscode/mcp.json`에서 `playwright`의 **▷ Start**를 누르고, Agent 모드에서:

> 네이버 증권에서 코스피 시가총액 상위 5개 종목 알려줘

크롬 창이 새로 떠서 AI가 직접 클릭하며 이동하면 성공입니다.

Windows에서 `playwright` 서버가 시작되지 않으면 설정을 이렇게 바꾸세요:

```json
"playwright": {
  "type": "stdio",
  "command": "cmd",
  "args": ["/c", "npx", "@playwright/mcp@latest"]
}
```

## Claude Desktop에 연결하기 (집에서 해보기)

Claude Desktop 설정 파일은 `${...}` 변수를 쓸 수 없어서 `claude_desktop_config.example.json`처럼 **전부 절대경로**로 적습니다. 설정 저장 후 앱을 완전히 종료했다가 다시 켜세요.

## 자주 나는 에러

| 증상 | 원인과 해결 |
|---|---|
| `No module named 'mcp'` | conda 환경 밖의 파이썬으로 실행됨. 터미널은 `conda activate 5-week4`, 설정 파일은 `command`를 conda 파이썬 경로로 |
| 결과가 빈 리스트 `[]` | 질문 목록 셀렉터(`.basic1 > li > dl`)가 안 맞음. 개발자 도구로 재확인 |
| 날짜, 답변 수는 나오는데 제목, 카테고리만 빈 값 | 네이버가 클래스 이름을 바꿈 (2026.09에 `_nclicks:kin.txt` → `_nclicks:qna.txt`로 바뀐 사례). 개발자 도구로 제목 `<a>` 태그의 class 확인 후 `parse_kin_page` 수정 |
| Inspector 연결은 되는데 응답이 깨짐 | 서버 코드에서 `print()` 사용. stdio 서버는 stdout이 통신 채널이라 `print` 금지 (로그는 `sys.stderr`로) |
| `npx` 실행 시 Node 버전 에러 | Node.js 22.19 이상으로 업데이트 |
| VS Code에서 서버가 시작 안 됨 | `command` 경로 오타. 3-1의 명령어로 경로 재확인. 로그는 Start 자리의 **Show Output** 또는 `Ctrl+Shift+P` → `MCP: List Servers` |
| Copilot이 도구를 안 씀 | 모드가 Agent인지, 🔧 목록에서 `search_kin`이 체크됐는지 확인. 질문에 `#search_kin` 넣기 |
| Claude Desktop에서 서버가 안 보임 | 경로는 반드시 절대경로. Windows는 역슬래시 두 번. 앱 완전히 재시작 |