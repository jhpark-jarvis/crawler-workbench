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
            page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=10_000)

            # 2015 링크 클릭으로 발생하는 AJAX 응답 하나만 정확히 기다린다.
            with page.expect_response(
                lambda response: (
                    response.request.method == "GET"
                    and "ajax=true" in response.url
                    and "year=2015" in response.url
                )
            ) as response_info:
                # 숫자로 시작하는 id는 '#2015' CSS 선택자로 사용할 수 없다.
                page.locator('[id="2015"]').click()

            response = response_info.value
            observation = {
                "request_url": response.url,
                "method": response.request.method,
                "status": response.status,
                "content_type": response.headers.get("content-type"),
            }

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
