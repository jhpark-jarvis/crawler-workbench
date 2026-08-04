import json
from pathlib import Path
from time import perf_counter

from playwright.sync_api import sync_playwright


TARGET_URL = "https://quotes.toscrape.com/js-delayed/?delay=2000"
SCENARIO_DIR = Path(__file__).resolve().parent
JSONL_OUTPUT_PATH = SCENARIO_DIR / "sample_output" / "quotes.jsonl"
REJECTED_JSONL_OUTPUT_PATH = SCENARIO_DIR / "sample_output" / "rejected_quotes.jsonl"
RUN_SUMMARY_PATH = SCENARIO_DIR / "sample_output" / "run_summary.json"
FAILURE_SCREENSHOT_PATH = SCENARIO_DIR / "sample_output" / "failure_screenshot.png"
FIXTURE_PATH = SCENARIO_DIR / "fixtures" / "quotes_rendered.html"
QUOTE_SELECTOR = "div.quote"


def save_rendered_fixture(html):
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(html, encoding="utf-8")


def extract_quotes(quote_locator):
    quotes = []

    for index in range(quote_locator.count()):
        quote = quote_locator.nth(index)
        text = quote.locator("span.text").inner_text().replace("“", "").replace("”", "")
        author = quote.locator("small.author").inner_text()
        tags = quote.locator("div.tags a.tag").all_inner_texts()
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


def save_run_summary(summary):
    RUN_SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUN_SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main():
    started_at = perf_counter()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # 초기 HTML이 아니라 quote card가 화면에 나타난 시점부터 수집한다.
            page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=10_000)
            quote_locator = page.locator(QUOTE_SELECTOR)
            quote_locator.first.wait_for(state="visible", timeout=10_000)

            # 렌더링된 DOM과 정제 결과를 남겨 이후 파싱 테스트를 브라우저 없이 반복할 수 있게 한다.
            save_rendered_fixture(page.content())
            quotes = extract_quotes(quote_locator)
            valid_quotes, rejected_quotes = validate_quotes(quotes)
            export_jsonl(valid_quotes, JSONL_OUTPUT_PATH)
            export_jsonl(rejected_quotes, REJECTED_JSONL_OUTPUT_PATH)

            summary = {
                "tool": "playwright",
                "locator": QUOTE_SELECTOR,
                "status": "success",
                "fetched": len(quotes),
                "valid": len(valid_quotes),
                "rejected": len(rejected_quotes),
                "elapsed_ms": round((perf_counter() - started_at) * 1000),
            }
            save_run_summary(summary)
            print(json.dumps(summary, ensure_ascii=False))
        except Exception as error:
            # 실패 시 마지막 화면을 남겨 selector, 로딩, 차단 페이지 여부를 진단한다.
            FAILURE_SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(FAILURE_SCREENSHOT_PATH), full_page=True)

            summary = {
                "tool": "playwright",
                "locator": QUOTE_SELECTOR,
                "status": "failure",
                "error_type": type(error).__name__,
                "error": str(error),
                "elapsed_ms": round((perf_counter() - started_at) * 1000),
            }
            save_run_summary(summary)
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    main()
