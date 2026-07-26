---
title: "Astro로 블로그 만들기 — 심화 가이드"
description: "Astro 콘텐츠 컬렉션, 동적 라우팅, RSS 피드 설정 방법을 단계별로 설명합니다."
pubDate: 2025-01-25
tags: ["astro", "튜토리얼", "웹개발"]
---

이 글에서는 Astro를 사용하여 블로그를 만드는 과정을 자세히 설명합니다.

## 프로젝트 구조

```
src/
├── content/blog/    # 마크다운 글 저장
├── layouts/         # 페이지 레이아웃
├── components/      # 재사용 컴포넌트
└── pages/           # 라우팅 페이지
```

## 콘텐츠 컬렉션

Astro의 콘텐츠 컬렉션을 사용하면 타입 안전하게 마크다운을 관리할 수 있습니다.

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    tags: z.array(z.string()),
  }),
});
```

## 동적 라우팅

`[slug].astro` 파일을 사용하여 각 글에 대한 페이지를 동적으로 생성합니다.

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}
---
```

## 마무리

Astro는 블로그를 만들기에 정말 좋은 도구입니다. 빠르고, 간단하고, 확장 가능합니다.
