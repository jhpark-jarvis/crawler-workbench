# requests scenarios

`requests`, `BeautifulSoup`, `lxml` 같은 HTTP/HTML 기반 수집 케이스를 다룹니다.

## 하위 케이스

- `static_html/`
  - 정적 HTML 페이지 수집
  - pagination, detail page, selector 파싱
- `public_api/`
  - 공개 API 수집
  - JSON parsing, pagination, rate limit 대응

## 검증 포인트

- HTTP 요청/응답 구조 이해
- 정적 페이지와 동적 페이지 구분
- HTML selector/XPath 설계
- API 호출과 JSON 처리
