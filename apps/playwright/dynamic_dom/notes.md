# Selenium 비교 메모

- Selenium은 `WebDriverWait(...).until(EC.visibility_of_all_elements_located(...))`로 모든
  quote card가 visible 상태가 될 때까지 기다린다.
- Playwright는 `locator.first.wait_for(state="visible")`로 첫 quote card의 렌더링을 확인한
  뒤 같은 locator로 전체 항목을 읽는다. locator 동작 자체에 auto-wait가 적용된다.
- 두 구현 모두 렌더링된 HTML fixture, 정상 JSONL, 제외 JSONL을 남긴다. 따라서 도구 차이는
  대기와 브라우저 제어 방식에 두고, 데이터 계약은 동일하게 유지한다.
- Playwright 구현은 예외 발생 시 `failure_screenshot.png`와 실패 실행 요약을 저장한다.
