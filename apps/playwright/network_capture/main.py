from pathlib import Path
import json

from playwright.sync_api import sync_playwright


SCENARIO_DIR = Path(__file__).resolve().parent
OBSERVATION_PATH = SCENARIO_DIR / "sample_output" / "network_observation.json"
TARGET_URL = "https://www.scrapethissite.com/pages/ajax-javascript/"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        try:
            # 클릭할 연도 링크가 준비될 만큼만 페이지의 초기 DOM 로딩을 기다린다.
            page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=10_000)

            # 클릭 전에 대상 AJAX 응답을 기다리도록 등록해 빠른 응답도 놓치지 않는다.
            with page.expect_response(
                lambda response: (
                    response.request.method == "GET"
                    and "ajax=true" in response.url
                    and "year=2015" in response.url
                )
            ) as response_info:
                # 숫자 ID는 속성 선택자로 찾고, 이 클릭이 2015년 영화 데이터 요청을 발생시킨다.
                page.locator('[id="2015"]').click()

            response = response_info.value

            # 직접 호출에 필요한 요청 URL과 응답 상태를 재현 가능한 형태로 기록한다.
            observation = {
                "request_url": response.url,
                "method": response.request.method,
                "status": response.status,
                "content_type": response.headers.get("content-type"),
            }

            # 실행 환경과 무관하게 관찰 결과를 UTF-8 JSON 파일로 저장한다.
            OBSERVATION_PATH.parent.mkdir(parents=True, exist_ok=True)
            OBSERVATION_PATH.write_text(
                json.dumps(observation, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            print(json.dumps(observation, ensure_ascii=False, indent=2))
            print(response.json())
        finally:
            browser.close()



if __name__ == "__main__":
    main()
