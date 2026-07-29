# scheduler

정기 수집 자동화와 실패 대응을 검증하는 파이프라인 시나리오입니다.

## 목표 작업

- 작업 ID: `PIPE-SCHED-01`
- 입력: JSONPlaceholder fixture 또는 SQLite DB
- 성공·일시 실패 후 성공·영구 실패 job을 실행 이력과 함께 처리한다.
- 완료 산출물: scheduler module, job run table, 세 시나리오 로그

## 산출물 예시

```text
scheduler/
  main.py
  scheduler.py
  sample_output/job_runs.jsonl
  sample_output/run_summary.json
  notes.md
```

```json
{"job_id":"books-sync","run_id":"20260729T100000Z","status":"retrying","attempt":1,"error_type":"TimeoutError"}
```

```json
{"job_id":"books-sync","run_id":"20260729T100000Z","status":"success","attempt":2,"records_written":20}
```

영구 실패는 retry 횟수와 최종 오류를 남기고 다음 실행 주기로 넘기는지 명시한다.

## 목표

- 스케줄 기반 실행을 구성한다.
- retry/backoff 정책을 적용한다.
- 최소한의 로깅과 이상 탐지 지표를 정의한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- 어떤 실패를 일시 장애로 볼 것인가?
- 수집 건수 급감은 어떻게 감지할 것인가?
- 운영 중 알림을 너무 많이 보내지 않으려면 어떻게 할 것인가?
