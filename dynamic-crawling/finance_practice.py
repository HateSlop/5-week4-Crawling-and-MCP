"""
3장 라이브 코딩: Playwright로 네이버 증권 시가총액 순위 크롤링하기
✏️ ____ 빈칸을 채우면서 따라오세요. 정답은 수업 후에 공개됩니다.

실행 방법 (⚠️ Jupyter 말고 터미널에서!):
    conda activate 5-week4
    cd dynamic-crawling
    python finance_practice.py

흐름: 네이버 증권 접속 → 안내 패널 닫기 → '국내' → '전체 종목보기' → '시가총액' → 표 읽기 → JSON 저장
"""
import json

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # ── 준비: 브라우저(창)와 페이지(탭) 열기 ──────────────────────────
    # headless=False: 브라우저가 눈에 보이게 / slow_mo=500: 동작마다 0.5초씩 천천히 (수업용)
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # ── Step 1. 네이버 증권 접속 ──────────────────────────────────────
    page.____("https://stock.naver.com/")

    # 💡 주석을 풀면 여기서 멈추고 Playwright Inspector 창이 뜹니다.
    #    Inspector의 'Pick locator'로 요소를 찍어보고, ▶(Resume)을 누르면 다음 줄로 진행해요.
    # page.pause()

    # 처음 접속하면 '새로운 증권 안내' 사이드 패널이 화면을 가릴 수 있어요.
    # 3초 동안 닫기 버튼을 찾아보고, 있으면 닫고 없으면 그냥 넘어갑니다.
    try:
        page.get_by_role("button").filter(has_text="사이드 패널 닫기").click(timeout=3000)
    except Exception:
        pass

    # ── Step 2. 클릭해서 시가총액 순위 페이지로 이동 ──────────────────
    # get_by_role("link", name="...") : 화면에 '...'이라고 적힌 링크를 찾기
    page.get_by_role("____", name="국내").____()
    page.get_by_role("link", name="전체 종목보기").first.click()   # 같은 링크가 여러 개라 첫 번째(.first)
    page.get_by_role("link", name="____").click()

    # ── Step 3. 표 찾고, 채워질 때까지 기다리기 ───────────────────────
    # 이 표에는 '국내 종목 주식 테이블'이라는 이름(직함)이 붙어 있어요.
    # class 이름(Table_table___uVrn)은 배포할 때마다 바뀌지만, 이름은 잘 안 바뀝니다.
    table = page.get_by_role("____", name="국내 종목 주식 테이블")

    # ⚠️ click() 같은 '행동'은 알아서 기다려주지만(auto-wait),
    #    .all(), all_inner_texts() 같은 '목록 읽기'는 기다려주지 않아요.
    #    JavaScript가 표를 채울 때까지, 첫 번째 줄이 나타나길 기다립니다.
    table.locator("tbody tr").first.____()

    # ── Step 4. 데이터 읽고 JSON으로 저장 ─────────────────────────────
    header = table.locator("th").____()   # th: 표의 제목 칸 (열 이름들)
    print("열 이름:", header)

    rows = []
    # 이 사이트는 표의 줄(tr)에 role="button"을 붙여놔서 get_by_role("row")로는 안 찾아져요.
    # 이럴 땐 2장에서 배운 CSS 선택자로!
    for tr in table.locator("tbody tr").all():
        cells = tr.locator("td").all_inner_texts()
        cells = [c.replace("\n", " ") for c in cells]   # "3,000\n(-1.10%)" → "3,000 (-1.10%)"
        if len(cells) > 1:
            rows.append(cells)

    print(f"{len(rows)}개 종목을 가져왔습니다.")
    for row in rows[:5]:
        print(row[:3])              # "순위 종목명", 현재가, 전일대비

    with open("market_cap.json", "w", encoding="utf-8") as f:
        json.dump({"header": header, "rows": rows}, f, ensure_ascii=____, indent=2)
    print("market_cap.json 저장 완료!")

    browser.close()
