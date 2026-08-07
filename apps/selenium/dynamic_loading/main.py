import json
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


TARGET_URL = "https://the-internet.herokuapp.com/dynamic_loading/1"
SCENARIO_DIR = Path(__file__).resolve().parent
RUN_RESULT_PATH = SCENARIO_DIR / "sample_output" / "run_result.json"
FAILURE_SCREENSHOT_PATH = SCENARIO_DIR / "sample_output" / "failure_screenshot.png"
START_BUTTON_SELECTOR = "#start button"
RESULT_SELECTOR = "#finish h4"
WAIT_TIMEOUT_SECONDS = 10
WAIT_CONDITION = "visibility_of_element_located(#finish h4)"


def initialize_driver():
    return webdriver.Chrome()


def export_json(record, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(record, output_file, ensure_ascii=False, indent=2)


def main():
    driver = initialize_driver()

    try:
        # 버튼 클릭 전후의 상태를 분리해, 각 단계에 맞는 명시적 대기 조건을 사용한다.
        driver.get(TARGET_URL)
        start_button = WebDriverWait(driver, WAIT_TIMEOUT_SECONDS).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, START_BUTTON_SELECTOR))
        )
        start_button.click()

        result_element = WebDriverWait(driver, WAIT_TIMEOUT_SECONDS).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, RESULT_SELECTOR))
        )
        run_result = {
            "target": "dynamic_loading/1",
            "status": "success",
            "result_text": result_element.text,
            "wait_condition": WAIT_CONDITION,
        }
        export_json(run_result, RUN_RESULT_PATH)
        print(json.dumps(run_result, ensure_ascii=False))
    except TimeoutException:
        # timeout 시 마지막 화면과 현재 URL을 남겨 대기 조건 실패를 재현할 수 있게 한다.
        FAILURE_SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(FAILURE_SCREENSHOT_PATH))

        run_result = {
            "target": "dynamic_loading/1",
            "status": "timeout",
            "wait_condition": WAIT_CONDITION,
            "timeout_seconds": WAIT_TIMEOUT_SECONDS,
            "current_url": driver.current_url,
            "screenshot_path": str(FAILURE_SCREENSHOT_PATH.relative_to(SCENARIO_DIR)),
        }
        export_json(run_result, RUN_RESULT_PATH)
        print(json.dumps(run_result, ensure_ascii=False))
    finally:
        # 성공·실패와 관계없이 Chrome 프로세스가 남지 않도록 종료한다.
        driver.quit()


if __name__ == "__main__":
    main()
