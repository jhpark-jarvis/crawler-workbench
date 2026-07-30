import requests as r
import bs4
import os
import json
import sys
from pathlib import Path

# Allow this scenario to import shared helpers when run as a script.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sql import connect, execute, execute_many, transaction

DATABASE_PATH = PROJECT_ROOT / "workbench.db"
JSONL_OUTPUT_PATH = Path(__file__).resolve().parent / "sample_output" / "books.jsonl"

CREATE_BOOKS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS books (
    source_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    price_gbp TEXT NOT NULL,
    availability TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 0 AND 5)
)
"""

UPSERT_BOOKS_SQL = """
INSERT INTO books (source_id, title, price_gbp, availability, rating)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(source_id) DO UPDATE SET
    title = excluded.title,
    price_gbp = excluded.price_gbp,
    availability = excluded.availability,
    rating = excluded.rating
"""

# 조회는 아니지만.. O(n) 방지를 위해 O(1)으로 쓰는게 낫지 않을까
star_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

def fetch_html(url):
    try:
        response = r.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except r.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_html(html_content):
    return bs4.BeautifulSoup(html_content, 'html.parser')

def save_fixture(soup, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

def convert_rating(star):
    return star_mapping.get(star, 0)  # Return 0 if the rating is not found


def create_books_table():
    connection = connect(DATABASE_PATH)
    try:
        with transaction(connection):
            execute(connection, CREATE_BOOKS_TABLE_SQL)
    finally:
        connection.close()


def upsert_books(json_data):
    rows = [
        (
            book["source_id"],
            book["title"],
            book["price_gbp"],
            book["availability"],
            book["rating"],
        )
        for book in json_data
    ]

    connection = connect(DATABASE_PATH)
    try:
        with transaction(connection):
            execute_many(connection, UPSERT_BOOKS_SQL, rows)
    finally:
        connection.close()


def export_books_jsonl(json_data):
    JSONL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JSONL_OUTPUT_PATH.open("w", encoding="utf-8") as output_file:
        for book in json_data:
            output_file.write(json.dumps(book, ensure_ascii=False) + "\n")



if __name__ == "__main__":
    create_books_table()

    #region html_fixtures 산출물
    os.makedirs("./fixtures", exist_ok=True)
    html_fixture = parse_html(fetch_html("https://books.toscrape.com/catalogue/page-1.html"))
    save_fixture(html_fixture, "./fixtures/books_page_1.html")
    #endregion
    
    data_list = []
    
    for i in range(1, 4): # 4
        html = fetch_html(f"https://books.toscrape.com/catalogue/page-{i}.html")
        if html:
            soup = parse_html(html)
            target = soup.select('#default > div > div > div > div > section > div:nth-child(2) > ol')
            for idx, li in enumerate(target[0].find_all('li')):
                a_tag = li.select_one('article > h3 > a')
                source_id = a_tag['href']
                static_path = "https://books.toscrape.com/catalogue/"
                title = a_tag['title']
                price_gbp = li.select_one('article > div.product_price > p.price_color').text.replace('Â', '').replace('£', '').strip()
                availability = li.select_one('article > div.product_price > p.instock.availability').text.strip()
                rating = convert_rating(li.select_one('article > p').get('class')[1])
                
                data_list.append({
                    "source_id": static_path + source_id,
                    "title": title,
                    "price_gbp": price_gbp,
                    "availability": availability,
                    "rating": rating
                })
    
    upsert_books(data_list)
    export_books_jsonl(data_list)

    print(json.dumps(data_list, indent=4))
    print(len(data_list))
                
            
