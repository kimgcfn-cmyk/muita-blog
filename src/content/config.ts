// 콘텐츠 컬렉션 스키마 — 블로그 글의 필드 타입을 정의합니다.
import { defineCollection, z } from 'astro:content';

// 블로그 글 컬렉션 스키마
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    // 글 제목
    title: z.string(),
    // 글 요약 (목록에서 표시)
    description: z.string(),
    // 발행일
    pubDate: z.coerce.date(),
    // 태그 목록 (배열)
    tags: z.array(z.string()).default([]),
    // 대표 이미지 경로 (선택)
    heroImage: z.string().optional(),
    // 초안 여부 (true면 목록에서 숨김)
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
