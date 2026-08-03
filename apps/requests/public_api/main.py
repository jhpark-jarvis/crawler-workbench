import json
import sys
from pathlib import Path

import requests as r

# Allow this scenario to import shared helpers when run as a script.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sql import connect, execute, execute_many, transaction


API_URL = "https://jsonplaceholder.typicode.com/posts"
PAGE_SIZE = 10
DATABASE_PATH = PROJECT_ROOT / "workbench.db"
SCENARIO_DIR = Path(__file__).resolve().parent
FIXTURE_PATH = SCENARIO_DIR / "fixtures" / "posts_page_1.json"
JSONL_OUTPUT_PATH = SCENARIO_DIR / "sample_output" / "posts.jsonl"
REJECTED_JSONL_OUTPUT_PATH = SCENARIO_DIR / "sample_output" / "rejected_posts.jsonl"

CREATE_POSTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS posts (
    source_id TEXT PRIMARY KEY,
    remote_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL
)
"""

UPSERT_POSTS_SQL = """
INSERT INTO posts (source_id, remote_id, user_id, title, body)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(source_id) DO UPDATE SET
    remote_id = excluded.remote_id,
    user_id = excluded.user_id,
    title = excluded.title,
    body = excluded.body
"""


def fetch_posts(page):
    response = r.get(
        API_URL,
        params={"_page": page, "_limit": PAGE_SIZE},
        timeout=10,
    )
    response.raise_for_status()
    return response


def save_fixture(posts):
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_posts(api_posts):
    return [
        {
            "source_id": f"jsonplaceholder:posts:{post.get('id')}",
            "remote_id": post.get("id"),
            "user_id": post.get("userId"),
            "title": post.get("title"),
            "body": post.get("body"),
        }
        for post in api_posts
    ]


def validate_posts(json_data):
    valid_posts = []
    rejected_posts = []
    seen_source_ids = set()

    for row_index, post in enumerate(json_data):
        reason_codes = []
        missing_fields = [
            field
            for field in ("source_id", "remote_id", "user_id", "title", "body")
            if post.get(field) is None or post.get(field) == ""
        ]
        if missing_fields:
            reason_codes.append("missing_required_field")

        source_id = post.get("source_id", "")
        if not source_id.startswith("jsonplaceholder:posts:"):
            reason_codes.append("invalid_source_id")
        elif source_id in seen_source_ids:
            reason_codes.append("duplicate_source_id")

        if not isinstance(post.get("remote_id"), int) or post["remote_id"] <= 0:
            reason_codes.append("invalid_remote_id")
        if not isinstance(post.get("user_id"), int) or post["user_id"] <= 0:
            reason_codes.append("invalid_user_id")

        if reason_codes:
            rejected_posts.append(
                {
                    "row_index": row_index,
                    "reason_codes": reason_codes,
                    "record": post,
                }
            )
            continue

        seen_source_ids.add(source_id)
        valid_posts.append(post)

    return valid_posts, rejected_posts


def create_posts_table():
    connection = connect(DATABASE_PATH)
    try:
        with transaction(connection):
            execute(connection, CREATE_POSTS_TABLE_SQL)
    finally:
        connection.close()


def upsert_posts(json_data):
    rows = [
        (
            post["source_id"],
            post["remote_id"],
            post["user_id"],
            post["title"],
            post["body"],
        )
        for post in json_data
    ]

    connection = connect(DATABASE_PATH)
    try:
        with transaction(connection):
            execute_many(connection, UPSERT_POSTS_SQL, rows)
    finally:
        connection.close()


def export_jsonl(records, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        for record in records:
            output_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    create_posts_table()

    page = 1
    normalized_posts = []
    while True:
        response = fetch_posts(page)
        api_posts = response.json()

        if page == 1:
            save_fixture(api_posts)

        normalized_posts.extend(normalize_posts(api_posts))
        print(f"page={page}, records={len(api_posts)}, has_next={'next' in response.links}")

        if "next" not in response.links:
            break
        page += 1

    valid_posts, rejected_posts = validate_posts(normalized_posts)
    upsert_posts(valid_posts)
    export_jsonl(valid_posts, JSONL_OUTPUT_PATH)
    export_jsonl(rejected_posts, REJECTED_JSONL_OUTPUT_PATH)

    print(
        json.dumps(
            {
                "fetched": len(normalized_posts),
                "valid": len(valid_posts),
                "rejected": len(rejected_posts),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
