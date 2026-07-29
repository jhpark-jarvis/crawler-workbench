# selenium scenarios

`selenium` 기반 브라우저 자동화 수집 케이스를 다룹니다.

## 하위 케이스

- `dynamic_dom/`
  - JS 렌더링 이후 DOM 파싱
- `anti_flaky/`
  - wait, retry, timeout, screenshot 같은 안정화 포인트 점검

## 검증 포인트

- 동적 렌더링 페이지 수집 경험
- headless 브라우저 사용 경험
- DOM 구조 분석과 XPath/CSS selector 사용
- flaky automation 대응
