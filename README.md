# HateSlop 5기 실습 · Week 4

HateSlop 5기 4주차 (HTML, 크롤링, MCP) 실습 레포지토리입니다. 이번 주차에서는 웹 페이지의 구조(HTML)를 이해하고, 정적 크롤링(requests, BeautifulSoup)과 동적 크롤링(Playwright)으로 데이터를 수집한 뒤, 직접 만든 크롤러를 **MCP 서버**로 만들어 AI가 쓸 수 있는 도구로 바꿔봅니다.

> 📒 개념 설명과 실습 진행은 노션 강의자료(**HTML, 크롤링, MCP**)를, 환경 설정은 **4주차 사전 준비사항**을 참고하세요.

## 개요

| 강의 | 내용 | 실습 파일 |
|---|---|---|
| 1장 | HTML 기초, 크롬 개발자 도구 | (없음) |
| 2장 | 정적 크롤링: requests & BeautifulSoup | `static-crawling/kin_practice.ipynb` |
| 3장 | 동적 크롤링: Selenium 소개, Playwright | `dynamic-crawling/finance_practice.py` |
| 4장 | MCP: 내 크롤러를 AI 도구로 만들기 | `mcp-practice/` |
| 과제 | 알라딘 크롤링 + MCP 서버 | `hw/` |

## 저장소 구조

```
5-week4-Crawling-and-MCP/
├── README.md
├── requirements.txt              # Python 의존성
├── .vscode/
│   └── mcp.json                  # VS Code MCP 서버 설정 (본인 파이썬 위치 입력)
├── static-crawling/              # 2장 정적 크롤링 라이브 코딩
│   └── kin_practice.ipynb        #   네이버 지식인 검색 결과 크롤링
├── dynamic-crawling/             # 3장 동적 크롤링 라이브 코딩
│   └── finance_practice.py       #   Playwright로 네이버 증권 시가총액 순위 크롤링
├── mcp-practice/                 # 4장 MCP 실습
│   ├── README.md                 #   4장 실습 상세 가이드
│   ├── kin_crawler.py            #   2장 크롤러를 함수로 정리한 것
│   ├── kin_mcp_server.py         #   FastMCP로 만든 지식인 MCP 서버
│   ├── mcp_client.py             #   Inspector 없이 서버를 호출해보는 클라이언트
│   └── claude_desktop_config.example.json
└── hw/                           # 과제
    ├── hw1_aladin.ipynb          #   [과제 1] 알라딘 베스트셀러 정적 크롤링
    ├── hw2_aladin_mcp.py         #   [과제 2] 과제 1 크롤러를 MCP 서버로
    └── [본인이름]/                #   제출용 개인 폴더 (직접 생성)
        ├── hw1_aladin.py
        ├── hw2_aladin_mcp.py
        └── hw2_inspector.png
```

> 실습 정답 파일(`*_answer`)은 과제 마감 후에 올라옵니다.

## 시작하기

자세한 설명과 캡처는 노션 **4주차 사전 준비사항**에 있습니다. 여기는 요약입니다.

1. **Fork & Clone**
   이 레포를 Fork한 뒤, 내 계정의 레포를 Clone합니다.
   ```bash
   git clone [자신의 Fork Repository URL]
   cd 5-week4-Crawling-and-MCP
   ```

2. **conda 환경 생성 및 활성화** (Python 3.12)
   ```bash
   conda create -n 5-week4 python=3.12
   conda activate 5-week4
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **Playwright 브라우저 설치** (3장)
   ```bash
   playwright install chromium
   ```

5. **Node.js 22.19 이상 설치** (4장 MCP Inspector, Playwright MCP)
   ```bash
   node -v
   ```

6. **`.vscode/mcp.json`에 내 파이썬 위치 넣기** (4장)
   ```bash
   python -c "import sys; print(sys.executable)"
   ```
   출력된 위치를 `naver-kin`의 `"command"`에 넣습니다. **Windows는 `\`를 전부 `/`로 바꿔서** 넣으세요.

## 실습 실행 방법

| 실습 | 실행 방법 |
|---|---|
| 2장 | VS Code에서 노트북을 열고 커널을 `5-week4`로 선택 |
| 3장 | ⚠️ Jupyter 말고 **터미널**에서 `cd dynamic-crawling` → `python finance_practice.py` |
| 4장 | `mcp-practice/README.md` 참고 |

## .ipynb → .py 변환 가이드 (과제 제출용)

GitHub에서 코드 리뷰를 원활하게 진행하기 위해, **`hw/` 폴더에 제출하는 노트북 과제**는 반드시 `.py` 파일로 변환하여 제출해 주세요.

1. 노트북이 있는 폴더로 이동합니다.
2. 다음 명령어를 실행합니다.
   ```bash
   python -m jupyter nbconvert --to script [파일명].ipynb
   ```
   *예시: `python -m jupyter nbconvert --to script hw1_aladin.ipynb`*

## 과제 (Assignment)

### 1. 정적 크롤링: 알라딘 베스트셀러 크롤링 ([hw1_aladin.ipynb](./hw/hw1_aladin.ipynb))
- `requests`와 `BeautifulSoup`로 알라딘 베스트셀러 1~3페이지에서 **제목, 링크, 할인가, 별점**을 모아 `aladin.csv`로 저장합니다.
- 셀렉터는 크롬 개발자 도구로 **직접** 찾아야 합니다. (1장, 2장 복습)
- 별점이 없는 신간처럼 정보가 빠진 책은 `try-except`로 건너뜁니다.

### 2. MCP: 내 크롤러를 AI 도구로 ([hw2_aladin_mcp.py](./hw/hw2_aladin_mcp.py))
- 과제 1의 크롤링 코드를 `crawl_bestsellers()` 안으로 옮기고(TODO 1), `@mcp.tool()`로 도구를 등록하고(TODO 2), AI가 읽을 docstring을 씁니다(TODO 3).
- `hw/` 폴더에서 테스트합니다.
  ```bash
  # 크롤러 함수 확인
  python -c "from hw2_aladin_mcp import crawl_bestsellers; print(crawl_bestsellers(1)[:3])"

  # MCP Inspector로 도구 확인
  npx @modelcontextprotocol/inspector@2.8.0 python hw2_aladin_mcp.py
  ```
- Inspector에서 **Connected** → **Tools** 탭 → `get_bestsellers` → **Execute Tool** 결과를 캡처해 `hw2_inspector.png`로 함께 제출합니다.
- ⚠️ MCP 서버 파일에서는 `print()`를 쓰지 마세요. (stdout이 통신 채널입니다)

### 선택 도전 🏆
- 도구 하나 더 만들기: 예) 베스트셀러 중 제목에 키워드가 들어간 책만 돌려주는 `find_book(keyword)`
- VS Code + Copilot(Agent 모드)에 서버를 연결하고 AI에게 질문한 화면 캡처하기

## 제출 방법 및 규칙

1. **브랜치 및 폴더 생성**: 본인 이름으로 브랜치를 만들고, `hw/` 폴더 안에 **개인 폴더**를 만듭니다.
   ```bash
   git checkout -b "본인이름"
   mkdir hw/"본인이름"
   ```
2. **제출 파일 정리**: 아래 3개 파일을 개인 폴더에 넣습니다.

   | 파일 | 설명 |
   |---|---|
   | `hw1_aladin.py` | 과제 1 노트북을 `.py`로 변환한 파일 |
   | `hw2_aladin_mcp.py` | 과제 2 MCP 서버 |
   | `hw2_inspector.png` | Inspector에서 Execute Tool을 실행한 결과 캡처 |

3. **커밋 및 푸시**
   ```bash
   git add hw/"본인이름"
   git commit -m "[feat] week4 과제 제출"
   git push origin "본인이름"
   ```
4. **Pull Request (PR)**: 원래 레포(`HateSlop/5-week4-Crawling-and-MCP`)의 `main` 브랜치로 PR을 보내주세요.
   - PR 제목 예시: `week4_본인이름`

> ⚠️ 실습하면서 생긴 `aladin.csv`, `kin.csv`, `market_cap.json` 같은 결과 파일은 PR에 넣지 마세요.

### 커밋 컨벤션
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅 등
- `refactor`: 코드 리팩토링
- `chore`: 패키지 매니저 수정 등
