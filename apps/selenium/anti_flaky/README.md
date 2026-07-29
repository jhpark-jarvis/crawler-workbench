# anti_flaky

Selenium 기반 수집의 불안정성을 재현하고 줄이는 검증 시나리오입니다.

## 목표 작업

- 작업 ID: `SEL-FLAKY-01`
- 타겟: `https://quotes.toscrape.com/js-delayed/?delay=2000`
- 지연 로딩 timeout을 재현한 뒤 조건 기반 대기와 제한된 재시도로 안정화한다.
- 완료 산출물: 실패 재현 기록, 안정화 코드, timeout·retry 로그

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
