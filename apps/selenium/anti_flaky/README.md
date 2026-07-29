# anti_flaky

Selenium 기반 수집의 불안정성을 재현하고 줄이는 검증 시나리오입니다.

## 목표

- explicit wait를 사용한다.
- timeout, retry, screenshot, logging을 붙인다.
- 수집 실패를 재현하고 대응 포인트를 기록한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- 어떤 에러는 재시도 대상이고 어떤 에러는 즉시 실패인가?
- wait 조건을 DOM 기준으로 둘지 네트워크 기준으로 둘지 어떻게 정할 것인가?
- 운영 중 실패율이 올라가면 어떤 로그부터 볼 것인가?
