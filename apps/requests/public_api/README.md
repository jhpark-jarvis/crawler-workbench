# public_api

공개 API 수집 구현 시나리오입니다.

## 목표 작업

- 작업 ID: `REQ-API-01`
- 타겟: `GET https://jsonplaceholder.typicode.com/posts`
- 페이지네이션: query parameter `_page`, `_limit` 사용
- 페이지 크기: `_limit=10`
- 종료 조건: 응답 `Link` 헤더에 `rel="next"`가 없을 때
- 정규화: `source_id=jsonplaceholder:posts:{id}`, `userId`는 `user_id`로 변환
- 검증: `id`, `userId`, `title`, `body` 필수값과 `source_id` 중복 검사
- 완료 산출물: JSON fixture, validation report, SQLite upsert, `posts.jsonl`

## 산출물 예시

```text
public_api/
  main.py
  fixtures/posts_page_1.json
  sample_output/posts.jsonl
  sample_output/validation_report.json
  notes.md
```

```json
{"source_id":"jsonplaceholder:posts:1","user_id":1,"title":"sunt aut facere repellat provident occaecati excepturi optio reprehenderit","body":"..."}
```

```json
{"fetched":10,"valid":10,"invalid":0,"duplicate":0,"next_page":2}
```

## 목표

- REST API endpoint를 호출한다.
- JSON 응답을 정규화한다.
- page 또는 cursor 기반 pagination을 처리한다.
- 요청 제한과 재시도를 고려한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- 인증이 없는 공개 API인가?
- 응답 스키마가 바뀌면 어디서 깨지는가?
- DOM 파싱보다 API 호출이 왜 더 안정적인가?
