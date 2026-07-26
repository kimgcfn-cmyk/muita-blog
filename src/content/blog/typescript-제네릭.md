---
title: "TypeScript 제네릭 완전 정복"
description: "제네릭의 기본 개념부터 실전 활용까지, 예제와 함께 알아보는 TypeScript 제네릭 가이드."
pubDate: 2025-02-05
tags: ["typescript", "튜토리얼", "프로그래밍"]
---

TypeScript의 제네릭(Generic)은 타입을 매개변수처럼 사용할 수 있게 해주는 강력한 기능입니다. 이 글에서는 제네릭의 핵심 개념을 실습과 함께 설명합니다.

## 제네릭이란?

제네릭은 **재사용 가능한 컴포넌트**를 만들 때 유용합니다. 하나의 함수나 클래스로 다양한 타입을 처리할 수 있습니다.

```typescript
// 일반 함수 — 특정 타입만 받음
function getFirstNumber(arr: number[]): number {
  return arr[0];
}

// 제네릭 함수 — 모든 타입을 받음
function getFirst<T>(arr: T[]): T {
  return arr[0];
}

getFirst([1, 2, 3]);       // number
getFirst(["a", "b", "c"]); // string
```

## 제네릭 제약 조건

`extends` 키워드로 제네릭이 받을 수 있는 타입을 제한할 수 있습니다.

```typescript
// length 속성을 가진 타입만 허용
function logLength<T extends { length: number }>(item: T): T {
  console.log(item.length);
  return item;
}

logLength("hello");     // OK
logLength([1, 2, 3]);   // OK
logLength({ length: 5, name: "test" }); // OK
// logLength(123);      // Error — number에는 length가 없음
```

## 실전 예시: API 응답 타입

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

interface User {
  id: number;
  name: string;
}

// 사용자 목록 응답
async function getUsers(): Promise<ApiResponse<User[]>> {
  const res = await fetch("/api/users");
  return res.json();
}

const response = await getUsers();
// response.data는 User[] 타입으로 자동 추론됨
response.data.forEach((user) => {
  console.log(user.name);
});
```

## 마무리

제네릭을 활용하면 타입 안전성을 유지하면서도 유연한 코드를 작성할 수 있습니다. 복잡해 보일 수 있지만, 하나씩 익혀가면 반드시 활용할 수 있는 핵심 기능입니다.
