# data_quality

수집 결과를 정제하고 검증하는 파이프라인 시나리오입니다.

## 목표 작업

- 작업 ID: `PIPE-QUALITY-01`
- 입력: Books 또는 JSONPlaceholder 결과에 오류를 섞은 fixture
- 정상·결측·중복·잘못된 타입 행을 검사하고 제외 사유를 분리한다.
- 완료 산출물: fixture, validation module, 유효/제외 행 결과

## 산출물 예시

```text
data_quality/
  main.py
  fixtures/books_mixed.jsonl
  sample_output/valid_rows.jsonl
  sample_output/rejected_rows.jsonl
  sample_output/validation_report.json
```

```json
{"input":5,"valid":2,"rejected":3,"reasons":{"missing_title":1,"invalid_price":1,"duplicate_source_id":1}}
```

제외 결과에는 원본 행과 기계가 읽을 수 있는 `reason_code`를 함께 남긴다.

## 목표

- 중복 기준을 설계한다.
- 결측값과 이상값 처리 기준을 세운다.
- raw 데이터와 clean 데이터를 구분한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- unique key는 무엇으로 잡을 것인가?
- 결측값은 폐기할지 보존할지 어떻게 정할 것인가?
- 데이터 품질과 크롤링 성공률은 왜 다른가?
