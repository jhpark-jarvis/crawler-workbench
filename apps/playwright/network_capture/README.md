# network_capture

Playwright로 페이지의 네트워크 요청을 분석하고, 가능하면 API 직접 호출로 전환하는 구현 시나리오입니다.

## 목표

- XHR, fetch 요청을 관찰한다.
- 필요한 endpoint, header, payload를 파악한다.
- 브라우저 DOM 파싱보다 API 직접 호출이 유리한지 판단한다.

## 만들 것

- `main.py`
- `README.md`
- `notes.md`

## 스스로 점검할 질문

- 이 페이지는 실제로 어떤 API로 데이터를 불러오는가?
- 브라우저 없이 재현 가능한 요청인가?
- 토큰, 쿠키, cursor는 어떻게 수집하고 갱신할 것인가?
