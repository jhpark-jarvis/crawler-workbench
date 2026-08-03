import json
from datetime import datetime, timezone
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


TARGET_URL = "https://quotes.toscrape.com/js-delayed/?delay=2000"
SCENARIO_DIR = Path(__file__).resolve().parent

FAILURE_JSON_OUTPUT_PATH = SCENARIO_DIR / "sample_output" / "run_failure.json"
SUCCESS_JSON_OUTPUT_PATH = SCENARIO_DIR / "sample_output" / "run_success.json"

FIXTURE_PATH = SCENARIO_DIR / "fixtures" / "quotes_rendered.html"
QUOTE_SELECTOR = "div.quote"


def initialize_driver():
    return webdriver.Chrome()


def save_rendered_fixture(html):
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(html, encoding="utf-8")


def extract_quotes(elements):
    quotes = []

    for element in elements:
        text = element.find_element(By.CSS_SELECTOR, "span.text").text.replace("“", "").replace("”", "")
        author = element.find_element(By.CSS_SELECTOR, "small.author").text
        tags = [tag.text for tag in element.find_elements(By.CSS_SELECTOR, "div.tags a.tag")]
        quotes.append({"text": text, "author": author, "tags": tags})

    return quotes

            
def export_json(records, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(records, output_file, ensure_ascii=False, indent=4)

def get_time():
    # 현재 UTC 시간 가져오기
    now_utc = datetime.now(timezone.utc)

    # 포맷팅하여 출력
    return now_utc.strftime("%Y%m%dT%H%M%SZ")

def main():
    driver = initialize_driver()
    wait_time_s = 0
    failure_list = []
    success_list = []
    attempt = 1
    while wait_time_s < 10:
        try:
            print(f"Attempt {attempt}: Waiting for {wait_time_s} seconds...")
            driver.get(TARGET_URL)
            elements = WebDriverWait(driver, wait_time_s).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, QUOTE_SELECTOR))
            )
            save_rendered_fixture(driver.page_source)

            quotes = extract_quotes(elements)            
            count_quotes = len(quotes)
            
            success_list.append({
                "run_id": get_time(),
                "attempt": attempt,
                "status": "success",
                "waited_seconds": wait_time_s,
                "records": count_quotes,
            })
            
            print(quotes)
            break
            
        except Exception as e:
            err_msg = repr(e)
            driver.save_screenshot(SCENARIO_DIR / f"sample_output" / f"error_screenshot_{get_time()}.png")
            if "Timeout" in str(err_msg):
                print(f"Timeout occurred after {wait_time_s} seconds. Retrying...")
                failure_list.append({
                                "run_id": get_time(),
                                "attempt": attempt,
                                "status": "timeout",
                                "waited_seconds": wait_time_s,
                                "reason": "quote card not visible"
                            })
                wait_time_s += 0.5
                
            else:
                print(f"An error occurred: {e}")
                failure_list.append({
                    "run_id": get_time(),
                    "attempt": attempt,
                    "status": "error",
                    "waited_seconds": wait_time_s,
                    "reason": str(e),
                })
                break
        finally:
            print(f"Attempt {attempt} completed. Waiting for {wait_time_s} seconds before next attempt.")
            attempt += 1
            
    try:
        export_json(failure_list, FAILURE_JSON_OUTPUT_PATH)
        export_json(success_list, SUCCESS_JSON_OUTPUT_PATH)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
