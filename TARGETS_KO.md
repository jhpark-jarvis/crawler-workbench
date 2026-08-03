# 시나리오 타겟 목록

이 문서는 각 시나리오가 무엇을 수집·검증하는지 바로 시작할 수 있도록 정한 기본
타겟 목록입니다. 타겟을 직접 찾는 것은 이 프로젝트의 선행 과제가 아닙니다.
새 타겟이 필요하면 먼저 후보, 정책 확인 결과, 선택 이유를 이 문서에 추가합니다.

최종 확인일: 2026-07-29. 아래 URL은 모두 이 날짜에 `200 OK` 응답을 확인했습니다.

## 공통 원칙

- 초기 시나리오는 의도적으로 테스트 데이터를 제공하는 사이트를 사용합니다.
- 라이브 요청은 필요한 최소 횟수로 제한하고, 파싱·검증 테스트는 저장한 fixture로
  반복합니다.
- 타겟의 상태나 정책은 바뀔 수 있으므로 각 시나리오 시작 시 `robots.txt`와 이용 조건을
  다시 확인합니다.
- 모든 시나리오에서 `수집 -> 파싱 -> 품질 검증 -> 중복 처리 -> 적재 -> 로그`를 수행합니다.
  `pipeline/`은 이 공통 흐름을 더 깊게 다루는 전용 시나리오입니다.

## 기본 타겟

| 디렉토리 | 기본 타겟 | 핵심 검증 | 수집할 데이터 예시 |
| --- | --- | --- | --- |
| `apps/requests/static_html` | [Books to Scrape](https://books.toscrape.com/) | 정적 HTML, CSS selector, 페이지네이션 | 제목, 가격, 재고 상태, 평점, 상세 URL |
| `apps/requests/public_api` | [JSONPlaceholder posts](https://jsonplaceholder.typicode.com/posts) | REST API, query parameter, JSON 검증 | `id`, `userId`, `title`, `body` |
| `apps/selenium/dynamic_dom` | [Quotes to Scrape JavaScript](https://quotes.toscrape.com/js/) | JavaScript 렌더링 후 DOM 대기·파싱 | 인용문, 작가, 태그 |
| `apps/selenium/dynamic_loading` | [The Internet - Dynamic Loading](https://the-internet.herokuapp.com/dynamic_loading/1) | 클릭, 명시적 대기, timeout 처리 | 실행 상태, 결과 텍스트, 대기 조건 |
| `apps/selenium/anti_flaky` | [Quotes to Scrape delayed](https://quotes.toscrape.com/js-delayed/?delay=2000) | 명시적 대기, timeout, 빈 결과와 지연 로딩 대응 | 인용문, 작가, 태그 |
| `apps/playwright/dynamic_dom` | [Quotes to Scrape delayed](https://quotes.toscrape.com/js-delayed/?delay=2000) | Playwright locator와 auto-wait, Selenium 구현 비교 | 인용문, 작가, 태그 |
| `apps/playwright/network_capture` | [Scrape This Site AJAX](https://www.scrapethissite.com/pages/ajax-javascript/) | XHR 식별, 응답 가로채기, API 직접 호출로 전환 | 연도별 팀명, 승/패, 득점 |
| `apps/pipeline/data_quality` | Books 또는 JSONPlaceholder에서 저장한 fixture | 스키마·결측·형식·범위·중복 검사 | 의도적으로 섞은 정상/중복/결측/잘못된 타입 행 |
| `apps/pipeline/storage` | Books 수집 결과 fixture | SQLite 스키마, upsert, idempotency | `source`, `source_id`, 수집 시각, 정규화 필드 |
| `apps/pipeline/scheduler` | JSONPlaceholder fixture 또는 위 SQLite DB | job 실행 이력, 재시도, 실패 알림 기준 | job ID, 시작·종료 시각, 상태, 레코드 수, 오류 |

## 타겟별 설계 메모

### `requests/static_html`: Books to Scrape

- 이 사이트는 스크래핑 테스트용 fictional bookstore이며, 1,000개 항목과
  페이지네이션을 제공합니다.
- 첫 목표는 1~3 페이지를 수집해 `title + detail URL`을 중복 키로 정하고 SQLite에
  저장하는 것입니다.
- 가격은 문자열 그대로 저장하지 말고 `Decimal` 또는 정수 단위로 정규화합니다.
- 대체 타겟: [Quotes to Scrape](https://quotes.toscrape.com/). 텍스트와 태그 중심의
  더 작은 정적 HTML 검증이 필요할 때 사용합니다.

### `requests/public_api`: JSONPlaceholder

- 테스트와 프로토타입을 목적으로 제공되는 fake REST API입니다.
- `posts`와 `comments`의 관계를 이용해 목록 수집, 상세/연관 데이터 수집, pagination
  parameter, JSON schema 검증을 수행합니다.
- 데이터가 가짜이고 비교적 고정적이므로, 변경 감지보다는 API 오류·timeout·재시도와
  idempotent 저장에 집중합니다.
- 대체 타겟: 실제 공개 API는 인증 키, 이용 조건, 호출 한도를 별도로 확인한 뒤 추가합니다.

### `selenium/dynamic_dom`: Quotes to Scrape JavaScript

- 초기 HTML과 렌더링 후 DOM의 차이를 확인하기 좋습니다.
- 고정 `sleep` 대신 quote card 또는 author element가 나타날 때까지 명시적으로 기다립니다.
- 수집 전 `requests`로 동일 URL을 받아 보고, 왜 브라우저가 필요한지 `notes.md`에
  비교 기록합니다.

### `selenium/dynamic_loading`: The Internet

- `Start` 버튼을 누른 뒤 숨겨진 요소가 나타나는 시점을 명시적 대기로 다룹니다.
- 데이터 수집 타겟이 아니라 click, wait condition, timeout 처리의 재현 가능한 브라우저
  검증 타겟입니다.
- 성공 조건은 `#finish h4`가 visible 상태가 되고 `Hello World!` 텍스트가 나오는 것입니다.

### `selenium/anti_flaky`: 지연 로딩 Quotes

- `?delay=2000`으로 의도적인 지연을 만들 수 있어 timeout과 대기 조건을 재현하기
  좋습니다.
- 첫 구현은 짧은 timeout으로 실패를 재현하고, 이후 조건 기반 대기와 충분한 timeout으로
  안정화합니다.
### `playwright/dynamic_dom`: 지연 로딩 Quotes

- Selenium과 같은 문제를 Playwright로 구현해 locator, auto-wait, timeout 관리의 차이를
  비교합니다.
- 두 구현의 저장 결과와 실패 로그 형식을 동일하게 맞추면 도구 선택 근거를 명확하게
  비교할 수 있습니다.

### `playwright/network_capture`: Scrape This Site AJAX

- 페이지에서 연도를 고르면 XHR로 JSON을 받는 구조입니다.
- Playwright로 요청 URL과 응답을 관찰한 뒤, 허용된 같은 엔드포인트를 `requests`로 직접
  호출하는 두 구현을 만듭니다.
- 확인용 예시 엔드포인트:
  `https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2015`
- 핵심 결론은 “브라우저로 API를 발견할 수 있지만, 데이터 수집 자체는 직접 HTTP 호출이
  더 단순하고 안정적일 수 있다”입니다.

### `pipeline/data_quality`: 혼합 fixture

- 외부 타겟을 새로 잡지 않습니다. 앞선 시나리오의 정제된 결과에 의도적으로 오류를 섞은
  JSON fixture를 만듭니다.
- 반드시 포함할 오류: 필수값 결측, 잘못된 타입, 허용 범위 밖 값, 중복 키, 예상하지 않은
  필드 또는 스키마 버전 변경.
- 결과는 유효 행, 제외 행, 제외 사유를 분리해 저장합니다.

### `pipeline/storage`: Books 결과

- Books의 상세 URL 또는 canonical URL을 `source_id`로 사용해 SQLite upsert를 구현합니다.
- 동일 입력을 두 번 적재해 row 수가 불필요하게 늘지 않는지 검증합니다.
- 수집 시각, 원본 URL, 정규화 결과, schema version을 남겨 재처리와 변경 추적을 검증합니다.

### `pipeline/scheduler`: fixture 기반 job

- 외부 사이트를 주기적으로 호출하지 않습니다. JSONPlaceholder fixture 또는 앞 단계의
  SQLite를 입력으로 사용하는 job을 만듭니다.
- 성공, 일시 실패 후 재시도 성공, 영구 실패의 세 경우를 테스트합니다.
- 실행 이력에는 job ID, 시작·종료 시각, 상태, 입력·출력 행 수, 오류 종류를 기록합니다.

## 첫 구현 순서

1. `apps/requests/static_html`: Books 1~3 페이지를 수집하고 SQLite에 upsert
2. `apps/requests/public_api`: posts를 수집하고 JSON schema·중복 검증
3. `apps/selenium/dynamic_dom`: JavaScript Quotes를 수집하고 requests와 차이 기록
4. `apps/selenium/anti_flaky`: 지연 로딩 실패와 안정화 구현
5. `apps/playwright/dynamic_dom`: 같은 지연 로딩을 Playwright로 재구현
6. `apps/playwright/network_capture`: XHR 관찰 후 direct API 호출로 전환
7. `apps/pipeline/` 세 시나리오: 앞에서 만든 fixture와 결과를 재사용

## 타겟 변경 절차

타겟이 응답하지 않거나 정책이 바뀌면 다음 순서로 교체합니다.

1. 기존 fixture로 파싱·검증 테스트가 계속 가능한지 확인합니다.
2. 같은 기술 포인트를 가진 테스트용 타겟을 후보로 찾습니다.
3. URL, 정책 확인 결과, 선택 이유, 변경 날짜를 이 문서에 기록합니다.
4. 타겟의 DOM/API 차이와 코드 변경 내용을 해당 시나리오의 `notes.md`에 기록합니다.
