# policy_guard

수집 전 정책을 확인하고, 차단 신호가 오면 우회하지 않고 중단하는 HTTP 수집 시나리오입니다.

## 목표 작업

- 작업 ID: `REQ-POLICY-01`
- 타겟: `https://www.scrapethissite.com/robots.txt`
- `robots.txt` 규칙을 확인한 뒤 허용된 경로만 요청하고, 요청 간격과 차단 응답 처리 정책을 적용한다.
- 완료 산출물: 정책 확인 결과, 허용·차단 경로 판정 결과, 중단 또는 재시도 실행 로그

## 타겟 정책 확인

2026-08-04 기준 `robots.txt`는 아래 규칙을 반환한다.

```text
User-agent: *
Disallow: /lessons/
Disallow: /faq/
```

이 규칙은 구현 시작 전에 다시 요청해 확인한다. 정책이 바뀌어도 수집기가 허용 여부를 먼저
판정하도록 만들고, 문서의 예시 문자열만 신뢰하지 않는다.

## 구현 흐름

1. `robots.txt`를 요청하고 User-Agent별 규칙을 파싱한다.
2. 수집하려는 URL 경로가 허용되는지 판정한다.
3. 허용된 경우에만 고정된 요청 간격과 timeout을 적용해 요청한다.
4. `429`는 `Retry-After` 헤더가 있으면 그 시간을 기록하고, 정해진 재시도 횟수를 넘기면 중단한다.
5. `403` 또는 CAPTCHA·로그인 요구 화면은 재시도하거나 우회하지 않고 즉시 중단하고 원인을 기록한다.

## 산출물 예시

```text
policy_guard/
  main.py
  fixtures/robots_allow_disallow.txt
  fixtures/response_429.json
  fixtures/response_403.html
  sample_output/policy_check.json
  sample_output/run_stopped.json
  notes.md
```

```json
{"target_url":"https://www.scrapethissite.com/pages/ajax-javascript/","robots_url":"https://www.scrapethissite.com/robots.txt","user_agent":"crawler-workbench/1.0 (contact: example@example.com)","allowed":true,"matched_rule":null}
```

```json
{"target_url":"https://www.scrapethissite.com/lessons/","robots_url":"https://www.scrapethissite.com/robots.txt","allowed":false,"matched_rule":"Disallow: /lessons/","action":"skip"}
```

```json
{"status":429,"retry_after_seconds":60,"attempt":2,"max_attempts":2,"action":"stop","reason":"request limit reached"}
```

## 준수 원칙

- 로그인, CAPTCHA, 유료벽, 접근 제어, 안티봇 보호를 우회하지 않는다.
- 프록시 또는 User-Agent 로테이션으로 차단 정책을 회피하지 않는다.
- `robots.txt`는 경로 허용 여부를 판단하는 기준이며, 이용약관·개인정보·저작권 검토를 대체하지 않는다.
- `403`, CAPTCHA, 로그인 요구는 요청 속도를 높이거나 재시도하는 신호가 아니라 수집을 중단하고 검토할 신호다.

## 스스로 점검할 질문

- `User-agent: *`와 특정 User-Agent 규칙이 함께 있으면 어떤 규칙을 적용할 것인가?
- `Crawl-delay`가 있거나 없을 때 요청 간격을 어떻게 결정할 것인가?
- `429`의 `Retry-After`가 없을 때 재시도와 중단 기준을 어떻게 기록할 것인가?
- 허용되지 않은 경로를 네트워크 요청 전에 차단했는지 어떻게 테스트할 것인가?
