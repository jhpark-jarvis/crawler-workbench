import selenium
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
from pathlib import Path
import json

# Allow this scenario to import shared helpers when run as a script.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


JSONL_OUTPUT_PATH = Path(__file__).resolve().parent / "sample_output" / "books.jsonl"
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "quotes_rendered.html"


def initialize_driver():
    driver = selenium.webdriver.Chrome()
    driver.get("https://quotes.toscrape.com/js/")
    return driver

def export_books_jsonl(json_data):
    JSONL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JSONL_OUTPUT_PATH.open("w", encoding="utf-8") as output_file:
        for book in json_data:
            output_file.write(json.dumps(book, ensure_ascii=False) + "\n")


def save_rendered_fixture(html):
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(html, encoding="utf-8")


def main():
    driver = initialize_driver()

    # DOM에 첫번째 요소가 생성될 때 까지 대기
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]'))
    )
    save_rendered_fixture(driver.page_source)

    data_list = []

    elements = driver.find_elements(By.XPATH, '/html/body/div/div')
    for element in elements:
        if element.get_attribute("class") == "quote":
            title = element.find_element(By.XPATH, './span[1]').text.replace("“", "").replace("”", "")
            author = element.find_element(By.XPATH, './span[2]/small').text
            # print(f"Title: {title}, Author: {author}")
            tags_elements = element.find_element(By.XPATH, './div')
            tags_list = []
            for tag_element in tags_elements.find_elements(By.XPATH, './a'):
                tag = tag_element.text
                tags_list.append(tag)
            # print(f"Tags: {', '.join(tags_list)}")
            # data_list.append(element.text)
            data_list.append({
                "title": title,
                "author": author,
                "tags": tags_list
            })

    export_books_jsonl(data_list)


if __name__ == "__main__":
    main()
