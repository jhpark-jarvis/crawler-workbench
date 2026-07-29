# pipeline scenarios

수집 이후의 데이터 품질, 저장, 자동화 운영 케이스를 다룹니다.

## 하위 케이스

- `data_quality/`
  - 결측, 중복, 타입 정규화
- `storage/`
  - SQLite 또는 다른 DB 적재
- `scheduler/`
  - 주기 실행, 로깅, 재시도

## 검증 포인트

- 데이터 품질 관리
- SQL 및 관계형 DB 이해
- 자동화 운영과 실패 대응
