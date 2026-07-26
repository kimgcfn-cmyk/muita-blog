// Astro 설정 파일 — 사이트 URL, 빌드 옵션 등을 정의합니다.
import { defineConfig } from 'astro/config';

export default defineConfig({
  // 배포 시 실제 사이트 URL로 변경하세요.
  site: 'https://muita.dev',
  markdown: {
    shikiConfig: {
      // 코드 블록 하이라이팅 테마 (라이트/다크 모드 지원)
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
    },
  },
});
