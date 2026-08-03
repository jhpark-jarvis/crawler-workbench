import json
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


TARGET_URL = "https://quotes.toscrape.com/js/"
SCENARIO_DIR = Path(__file__).resolve().parent
JSONL_OUTPUT_PATH = SCENARIO_DIR / "sample_output" / "quotes.jsonl"
REJECTED_JSONL_OUTPUT_PATH = SCENARIO_DIR / "sample_output" / "rejected_quotes.jsonl"
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


def validate_quotes(json_data):
    valid_quotes = []
    rejected_quotes = []
    seen_quote_keys = set()

    for row_index, quote in enumerate(json_data):
        reason_codes = []
        if not quote.get("text") or not quote.get("author"):
            reason_codes.append("missing_required_field")
        if not isinstance(quote.get("tags"), list):
            reason_codes.append("invalid_tags")

        quote_key = (quote.get("text"), quote.get("author"))
        if quote_key in seen_quote_keys:
            reason_codes.append("duplicate_quote")

        if reason_codes:
            rejected_quotes.append(
                {
                    "row_index": row_index,
                    "reason_codes": reason_codes,
                    "record": quote,
                }
            )
            continue

        seen_quote_keys.add(quote_key)
        valid_quotes.append(quote)

    return valid_quotes, rejected_quotes


def export_jsonl(records, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        for record in records:
            output_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    driver = initialize_driver()
    try:
        driver.get(TARGET_URL)
        elements = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, QUOTE_SELECTOR))
        )
        save_rendered_fixture(driver.page_source)

        quotes = extract_quotes(elements)
        valid_quotes, rejected_quotes = validate_quotes(quotes)
        export_jsonl(valid_quotes, JSONL_OUTPUT_PATH)
        export_jsonl(rejected_quotes, REJECTED_JSONL_OUTPUT_PATH)

        print(
            json.dumps(
                {
                    "fetched": len(quotes),
                    "valid": len(valid_quotes),
                    "rejected": len(rejected_quotes),
                },
                ensure_ascii=False,
            )
        )
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
