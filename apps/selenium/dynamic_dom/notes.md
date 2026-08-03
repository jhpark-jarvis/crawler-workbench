### 초기 HTML에 DOM 요소는 없었지만 inline script에 원본 데이터가 포함돼 있었다. 브라우저로 렌더링 구조를 확인한 뒤, 운영 수집은 requests 기반 script JSON 파싱으로 선택할 수 있다.




### requests 응답에 quote card가 없었던 이유와 기다린 locator를 비교
- 데이터 원본 자체는 HTML Javascript 내에 담겨있었지만, 페이지 렌더링 완료 이후(document.ready 상태) 동적 js가 페이지에 `<script> var data=[...] </script>`에 포함되어있는 데이터를 렌더링 하는 구조로 구성되어있었다.
- 페이지 리스트 내 첫번째 구성요소를 `WebDriverWait`와 `EC`를 이용하여 렌더링이 완료될때까지 동적으로 대기한 뒤에 데이터 크롤링을 시작하는 방식으로 접근했다.