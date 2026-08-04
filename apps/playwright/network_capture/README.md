# network_capture

Playwright로 페이지의 네트워크 요청을 분석하고, 가능하면 API 직접 호출로 전환하는 구현 시나리오입니다.

## 목표 작업

- 작업 ID: `PW-NET-01`
- 타겟: `https://www.scrapethissite.com/pages/ajax-javascript/`
- 타겟 페이지에서 `2015`를 클릭해 발생하는 XHR 응답을 관찰하고, 확인된 JSON endpoint를 직접 HTTP 호출로 전환한다.
- 현재 구현 산출물: 네트워크 관찰 기록
- 완료 시 산출물: browser/direct JSONL, 결과 비교 리포트

## 관찰 흐름

1. Playwright로 타겟 페이지에 접속한다.
2. `2015` 링크를 클릭한다.
3. `?ajax=true&year=2015` GET 응답을 캡처한다.
4. 같은 URL을 `requests`로 호출한 결과와 비교한다.

연도 링크의 HTML `id`는 `2015`처럼 숫자로 시작한다. 따라서 CSS 선택자 `#2015`는 유효하지 않고,
`[id="2015"]` 또는 텍스트 locator를 사용한다. 단순 응답 관찰에는 요청을 가로채는 `route()`가
필요하지 않으며, 클릭과 응답을 연결하는 `expect_response()`를 사용한다.

## 현재 구현 산출물

```text
network_capture/
  main.py
  sample_output/network_observation.json
```

```json
{"request_url":"https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2015","method":"GET","status":200,"content_type":"application/json"}
```

`main.py`는 Playwright로 `2015` 클릭 후 발생한 응답을 캡처하고,
`sample_output/network_observation.json`에 요청 메타데이터를 저장한다.

## 완료 시 확장 산출물

```text
network_capture/
  sample_output/browser_result.jsonl
  sample_output/direct_result.jsonl
  sample_output/comparison_report.json
  notes.md
```

`browser_result.jsonl`과 `direct_result.jsonl`은 **같은 정규화 구조**를 사용한다.
두 파일의 수집 방식만 다르고 `source_id`와 데이터 값은 같아야 한다.

```json
{"source_id":"scrapethissite:ajax-javascript:2015:spotlight","title":"Spotlight","year":2015,"awards":2,"nominations":6,"best_picture":true}
```

`browser_result.jsonl`은 Playwright로 렌더링된 DOM 또는 관찰한 response에서 만든 결과다.

```json
{"source_id":"scrapethissite:ajax-javascript:2015:spotlight","title":"Spotlight","year":2015,"awards":2,"nominations":6,"best_picture":true}
```

`direct_result.jsonl`은 확인한 endpoint를 `requests`로 직접 호출해 만든 결과다.

```json
{"browser_records":16,"direct_records":16,"matching_source_ids":16,"value_mismatches":0,"result":"match"}
```

`comparison_report.json`은 단순 건수뿐 아니라 `source_id` 집합과 같은 ID의 필드 값까지
비교한 결과를 기록한다. `notes.md`에는 browser/direct 결과가 일치했는지와 직접 호출로
전환해도 되는 근거를 기록한다.

## 목표

- XHR, fetch 요청을 관찰한다.
- 필요한 endpoint, header, payload를 파악한다.
- 브라우저 DOM 파싱보다 API 직접 호출이 유리한지 판단한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- 이 페이지는 실제로 어떤 API로 데이터를 불러오는가?
- 브라우저 없이 재현 가능한 요청인가?
- 토큰, 쿠키, cursor는 어떻게 수집하고 갱신할 것인가?
