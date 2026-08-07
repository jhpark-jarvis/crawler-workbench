# dynamic_loading

클릭 이후 비동기로 나타나는 요소를 Selenium의 명시적 대기로 검증하는 시나리오입니다.
이 시나리오는 일반적인 데이터 수집보다 브라우저 상호작용과 조건 기반 대기 전략에
집중합니다.

## 목표 작업

- 작업 ID: `SEL-WAIT-01`
- 타겟: `https://the-internet.herokuapp.com/dynamic_loading/1`
- `Start` 버튼을 클릭하고, 숨겨진 loading 상태가 끝난 뒤 `#finish h4`가 보일 때까지 대기
- 고정 `time.sleep()` 없이 `WebDriverWait`와 expected condition 사용
- 완료 산출물: 실행 결과 JSON, 실패 시 timeout·현재 URL·screenshot 경로를 담은 로그

## 산출물 예시

```text
dynamic_loading/
  main.py
  sample_output/run_result.json
  sample_output/failure_screenshot.png
  notes.md
```

```json
{
  "target": "dynamic_loading/1",
  "status": "success",
  "result_text": "Hello World!",
  "wait_condition": "visibility_of_element_located(#finish h4)"
}
```

## 구현 조건

- `driver.get()` 후 `#start button`이 clickable 상태일 때만 클릭한다.
- 클릭 후 `#finish h4`의 visible 상태를 성공 조건으로 사용한다.
- timeout은 명시적으로 설정하고, `TimeoutException`은 실패 결과로 기록한다.
- headless와 headed 모드 모두에서 같은 결과가 나오는지 확인한다.

## 스스로 점검할 질문

- `presence_of_element_located`보다 `visibility_of_element_located`가 적절한 이유는 무엇인가?
- 버튼 클릭 직후 `sleep(2)`가 불안정한 이유는 무엇인가?
- timeout 실패 시 어떤 정보가 있어야 재현과 진단이 가능한가?
