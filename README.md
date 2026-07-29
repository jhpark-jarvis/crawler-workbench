# crawler-workbench

다양한 웹·API 소스에서 신뢰성 있게 데이터를 수집하고, 검증·적재·운영하는 방법을
실험하는 Python 프로젝트입니다.

## 목적

이 레포의 목표는 아래 두 가지입니다.

1. 소스 특성에 맞는 수집 방식을 선택하고 구현한다.
2. 수집 성공뿐 아니라 데이터 품질과 운영 안정성까지 검증한다.

즉, `크롤러를 만든다`에서 끝내지 않고 아래까지 함께 검증합니다.

- 수집 방식 선택
- 사이트 구조 분석
- API/XHR 추적
- 데이터 정제와 저장
- 재시도, 로깅, 스케줄링
- 장애/변경 대응 포인트 정리

## 기술 기준

모든 예제는 Python으로 구현합니다. Selenium과 Playwright 역시 각각의 Python
바인딩을 사용하며, JavaScript/TypeScript 구현은 이 저장소의 범위에 포함하지 않습니다.

## 구현 시나리오

아래 케이스를 단계적으로 다루는 것을 목표로 합니다.

- 정적 페이지 수집
- 동적 페이지 수집
- 공개 API 수집
- 브라우저 자동화 기반 수집
- 네트워크 응답 분석 후 API 직접 호출
- 데이터 검증, 중복 제거, 정제
- DB 적재
- 스케줄링과 실패 대응

## 구조

```text
apps/
  requests/
    static_html/
    public_api/
  selenium/
    dynamic_dom/
    anti_flaky/
  playwright/
    dynamic_dom/
    network_capture/
  pipeline/
    data_quality/
    storage/
    scheduler/
```

각 폴더는 하나의 구현 시나리오이며, 가능한 한 아래 파일들을 같이 남깁니다.

- `README.md`
- `main.py` 또는 실행 스크립트
- `sample_output/` 또는 결과 예시
- `notes.md` 또는 장애/학습 메모

## 진행 원칙

프로젝트 전체 작업 규칙과 완료 기준은 [AGENTS.md](AGENTS.md)에 정리합니다.
한국어 안내는 [AGENT_KO.md](AGENT_KO.md)에서 볼 수 있습니다. 시나리오를 시작하기
전에 읽고, 각 케이스의 `README.md`와 `notes.md`에 해당 결정을 남깁니다.
각 시나리오의 기본 타겟과 선택 이유는 [TARGETS_KO.md](TARGETS_KO.md)에 정리합니다.

각 케이스를 만들 때 아래 질문에 답할 수 있어야 합니다.

- 왜 이 방식으로 수집했는가?
- requests로 충분한가, 브라우저 자동화가 필요한가?
- DOM에서 파싱할지, API 응답을 직접 쓸지 어떻게 판단했는가?
- 어떤 지점이 구조 변경에 취약한가?
- 데이터 품질은 어떻게 검증할 것인가?
- 운영 시 어떤 로그와 지표를 남길 것인가?

## 추천 진행 순서

1. `apps/requests/static_html`
2. `apps/requests/public_api`
3. `apps/selenium/dynamic_dom`
4. `apps/playwright/dynamic_dom`
5. `apps/playwright/network_capture`
6. `apps/pipeline/data_quality`
7. `apps/pipeline/storage`
8. `apps/pipeline/scheduler`

## 기록 원칙

이 레포는 단순한 예제 모음이 아니라, 재현 가능한 수집·운영 결정을 남기는 저장소입니다.
각 시나리오가 끝나면 아래를 짧게라도 기록합니다.

- 대상 구조 요약
- 처음 시도한 방식
- 실패한 지점
- 개선한 방식
- 운영 시 깨질 가능성이 높은 부분
- 검증한 실패 시나리오와 결과
