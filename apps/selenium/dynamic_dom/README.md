# dynamic_dom

Selenium으로 동적 렌더링 페이지를 수집하는 구현 시나리오입니다.

## 목표 작업

- 작업 ID: `SEL-DOM-01`
- 타겟: `https://quotes.toscrape.com/js/`
- JavaScript 렌더링 전후 차이를 확인하고 quote card가 나타난 뒤 데이터를 수집한다.
- 완료 산출물: requests 비교 메모, 정제 결과, 조건 기반 대기 코드

## 산출물 예시

```text
dynamic_dom/
  main.py
  fixtures/quotes_rendered.html
  sample_output/quotes.jsonl
  notes.md
```

```json
{"text":"The world as we have created it is a process of our thinking.","author":"Albert Einstein","tags":["change","deep-thoughts","thinking","world"]}
```

`notes.md`에는 requests 응답에 quote card가 없었던 이유와 기다린 locator를 비교해 기록한다.

## 목표

- JS 실행 이후 생성되는 DOM을 수집한다.
- 클릭, 스크롤, 페이지 이동 같은 상호작용을 처리한다.
- 수집 결과를 안정적으로 저장한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- `time.sleep` 말고 어떤 기다림 조건을 줄 것인가?
- headless와 headed 결과가 다르면 어디를 의심할 것인가?
- selector보다 URL 파라미터나 API 분석이 더 나은 상황은 언제인가?
