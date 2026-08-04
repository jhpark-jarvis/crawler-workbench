# dynamic_dom

Playwright로 동적 렌더링 페이지를 수집하는 구현 시나리오입니다.

## 목표 작업

- 작업 ID: `PW-DOM-01`
- 타겟: `https://quotes.toscrape.com/js-delayed/?delay=2000`
- Selenium과 같은 데이터 contract를 Playwright locator와 auto-wait로 구현한다.
- 완료 산출물: 렌더링 fixture, 정상·제외 JSONL, 실행 요약, 실패 screenshot

## 산출물 예시

```text
dynamic_dom/
  main.py
  fixtures/quotes_rendered.html
  sample_output/quotes.jsonl
  sample_output/rejected_quotes.jsonl
  sample_output/run_summary.json
  sample_output/failure_screenshot.png
  notes.md
```

```json
{"tool":"playwright","locator":"div.quote","status":"success","fetched":10,"valid":10,"rejected":0,"elapsed_ms":2417}
```

`quotes.jsonl`과 `rejected_quotes.jsonl`의 구조는 Selenium 구현과 동일하다. `notes.md`에는
Selenium 구현과 비교한 locator, 대기 방식, 실패 진단 방식의 차이를 기록한다.

## 목표

- locator 기반으로 DOM 요소를 안정적으로 찾는다.
- click, scroll, wait 전략을 비교한다.
- 수집 실패 시 trace 또는 screenshot을 남길 수 있게 설계한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- Selenium보다 어떤 점이 편하거나 안정적인가?
- `networkidle`이 항상 정답이 아닌 이유는 무엇인가?
- locator 전략을 어떻게 잡을 것인가?
