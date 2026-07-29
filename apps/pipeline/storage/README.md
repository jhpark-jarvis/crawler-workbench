# storage

수집 데이터를 파일 또는 DB에 적재하는 파이프라인 시나리오입니다.

## 목표 작업

- 작업 ID: `PIPE-STORE-01`
- 입력: Books 수집 결과 fixture
- `source_id` unique key와 upsert로 재실행 안전한 SQLite 적재를 구현한다.
- 완료 산출물: schema, storage module, 두 번 실행한 검증 결과

## 목표

- SQLite 같은 관계형 저장소에 적재한다.
- upsert 또는 idempotent 적재 전략을 생각한다.
- 스키마 설계와 적재 흐름을 정리한다.

## 만들 것

- `main.py`
- `schema.sql`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- 재수집 시 중복 적재를 어떻게 막을 것인가?
- 어떤 컬럼에 인덱스가 필요한가?
- raw와 normalized 테이블을 분리할 것인가?
