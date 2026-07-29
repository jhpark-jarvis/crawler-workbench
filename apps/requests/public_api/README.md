# public_api

공개 API 수집 구현 시나리오입니다.

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
