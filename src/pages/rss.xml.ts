// RSS 피드 생성 엔드포인트 — RSS 2.0 형식으로 블로그 글을 제공합니다.
// @astrojs/rss 패키지를 사용하여 피드를 생성합니다.

import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

// RSS 피드 생성 핸들러
export async function GET(context: APIContext) {
  const posts = (await getCollection('blog'))
    .filter((post) => !post.data.draft)
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  return rss({
    title: 'Muita Blog',
    description: '개발과 기술에 대한 블로그',
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/blog/${post.slug}/`,
    })),
  });
}
