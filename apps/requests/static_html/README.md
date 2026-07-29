# static_html

정적 페이지 수집 구현 시나리오입니다.

## 목표 작업

- 작업 ID: `REQ-STATIC-01`
- 타겟: `https://books.toscrape.com/`
- Books 1~3 페이지의 상품 목록을 수집하고, 상세 URL을 기준으로 정규화한다.
- 완료 산출물: HTML fixture, SQLite upsert 결과, 실행 로그

## 목표

- requests로 HTML을 가져온다.
- CSS selector 또는 XPath로 데이터를 파싱한다.
- 목록/상세 구조를 다뤄본다.
- 중복과 누락 필드를 점검한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- 정말 브라우저 자동화가 필요 없는 페이지인가?
- selector가 깨질 때 가장 먼저 어디를 볼 것인가?
- 상대경로 링크와 인코딩은 어떻게 처리할 것인가?
