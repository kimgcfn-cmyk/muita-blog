---
title: "CSS Container Queries로 컴포넌트 주도 레이아웃 만들기"
description: "미디어쿼리 대신 컨테이너 크기에 반응하는 CSS Container Queries를 알아봅니다."
pubDate: 2025-02-20
tags: ["css", "웹개발", "튜토리얼"]
---

미디어쿼리는 **뷰포트** 크기에 반응하지만, 때로는 특정 **컴포넌트의 부모 요소** 크기에 반응하고 싶을 때가 있습니다. CSS Container Queries가 이 문제를 해결합니다.

## 미디어쿼리 vs 컨테이너 쿼리

```css
/* 미디어쿼리 — 브라우저 전체 크기에 반응 */
@media (min-width: 768px) {
  .card { flex-direction: row; }
}

/* 컨테이너 쿼리 — 부모 요소 크기에 반응 */
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card { flex-direction: row; }
}
```

## 왜 필요한가?

컴포넌트 기반 개발에서 각 컴포넌트는 다양한 위치에 배치될 수 있습니다. 미디어쿼리는 "화면이 넓으면 가로로"라고 말하지만, 컨테이너 쿼리는 "이 컴포넌트가 넓으면 가로로"라고 말할 수 있습니다.

## 실전 사용법

### 1. 컨테이너 정의

```css
.sidebar {
  container-type: inline-size;
  container-name: sidebar;
}
```

### 2. 쿼리 작성

```css
@container sidebar (min-width: 300px) {
  .sidebar-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
}
```

### 3. 컨테이너 이름 활용

여러 개의 컨테이너가 있을 때 이름으로 구분할 수 있습니다.

```css
@container sidebar (min-width: 300px) { /* ... */ }
@container main (min-width: 600px) { /* ... */ }
```

## 브라우저 지원

2025년 기준 주요 브라우저에서 지원합니다. IE는 지원하지 않지만, 크로스 브라우징이 필요한 경우 미디어쿼리로 대체할 수 있습니다.

## 마무리

컨테이너 쿼리는 컴포넌트를 진정으로 재사용 가능한 단위로 만드는 데 기여합니다. 반응형 디자인의 다음 단계라고 할 수 있습니다.
