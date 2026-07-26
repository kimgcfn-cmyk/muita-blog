---
title: "Git 브랜치 전략: 나만의 워크플로우 찾기"
description: "개인 프로젝트와 팀 프로젝트에서 활용할 수 있는 Git 브랜치 전략과 커밋 컨벤션을 정리합니다."
pubDate: 2025-02-12
tags: ["git", "개발일지", "워크플로우"]
---

이번 글에서는 Git 브랜치 전략과 커밋 컨벤션에 대해 정리합니다. 프로젝트 규모와 팀 상황에 따라 적절한 전략을 선택하는 것이 중요합니다.

## 왜 브랜치 전략이 필요한가?

브랜치 전략이 없으면 충돌이 잦아지고, 배포가 불안정해지며, 이력 관리가 어려워집니다.

## 개인 프로젝트: 간단한 전략

혼자 작업할 때는 너무 복잡할 필요가 없습니다.

```
main          ← 항상 배포 가능한 상태
  └── feature/xxx   ← 기능 개발
```

작업이 끝나면 squash merge로 깔끔하게 합칩니다.

```bash
git checkout main
git merge --squash feature/xxx
git commit -m "feat: xxx 기능 추가"
git branch -d feature/xxx
```

## 팀 프로젝트: Git Flow

팀에서는 좀 더 구조화된 접근이 필요합니다.

- `main` — 프로덕션 코드
- `develop` — 개발 통합 브랜치
- `feature/*` — 기능 개발
- `hotfix/*` — 긴급 수정

## 커밋 컨벤션

[Conventional Commits](https://www.conventionalcommits.org/)를 따르면 이력이 깔끔해집니다.

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 변경
refactor: 코드 리팩토링
test: 테스트 추가
chore: 빌드, 설정 변경
```

## 나의 워크플로우

개인 프로젝트에서는 **trunk-based development**를 선호합니다. 기능 브랜치를 만들되, 빠르게 병합하는 것이 핵심입니다. 너무 오래 방치된 브랜치는 병합 충돌과 싸워야 하기 때문입니다.

작은 단위로 커밋하고, 빠르게 병합하고, 지속적으로 배포하는 것이 좋습니다.
