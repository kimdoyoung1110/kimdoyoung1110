<h1 align="center">👋 안녕하세요, 김도영입니다!</h1>

<p align="center">
  실서비스 커머스를 <b>초기 구축부터 1차 런칭까지 전담</b>해 본 <b>프론트엔드 개발자</b>입니다.<br/>
  결제·구독처럼 돈이 오가는 도메인의 엣지케이스를 설계로 풀고,<br/>
  CI · 테스트 · SEO · 보안까지 <b>런칭 품질</b>을 직접 책임집니다.
</p>

<p align="center">
  <a href="https://doyoungkim-portfolio.vercel.app/">
    <img src="https://img.shields.io/badge/🌐%20Portfolio-doyoungkim--portfolio.vercel.app-6366F1?style=for-the-badge&logoColor=white"/>
  </a>
</p>

---

## ✨ Highlights

- 🥗 **[Slunch Factory](https://slunch.co.kr/)** 에서 자사몰 커머스 **VeggieVerse**를 초기 구축부터 1차 런칭까지 프론트엔드 전담 — **5개 레포 500+ 커밋** (2026.05 ~ 현재)
- 💳 **토스페이먼츠 빌링 기반 결제·구독 시스템** 구축 — 결제 순서 재설계 · 품절 하드 가드 · 타임존 버그 등 엣지케이스를 설계로 해결
- 🛡️ CI가 전무하던 프로덕트에 **typecheck·build·test 게이트, 번들 보안 검증, SEO 구조화** 등 런칭 품질 기준을 0에서 수립
- 🧑‍💻 인천대 **[앱센터](https://github.com/inu-appcenter)** [memorIN](https://github.com/inu-appcenter/memorIN) **백엔드 시니어** (Spring Boot · PostgreSQL · WebSocket) · 인천대 **인공지능빅데이터센터**에서 RAG · LLM Agent 연구

---

## 💼 Experience

### 🏢 Slunch Factory — 프론트엔드 인턴 <sub>2026.05 ~ 현재</sub>

> AI 기반 비건 식단 구독 푸드테크 스타트업. 자사몰 **[VeggieVerse](https://slunch.co.kr/)** B2C 커머스를 초기 구축부터 1차 런칭까지 전담했습니다. <sub>(사내 레포는 비공개 — 라이브 서비스와 [포트폴리오](https://doyoungkim-portfolio.vercel.app/)에서 확인하실 수 있어요)</sub>
>
> `Next.js` `React` `TypeScript` `Tailwind CSS` `TanStack Query` `Supabase` `Toss Payments`

**결제 · 구독 시스템**
- 토스페이먼츠 빌링키 기반 정기결제·결제수단 관리 구축 — 복수 카드 등록 · 기본 카드 지정 · 등록 카드 바로결제
- 신규 카드 사용자의 첫 구독 결제가 전부 400으로 실패하는 문제를 발견, 결제 흐름을 **'카드 등록 → 주문 생성 → 결제'** 순서로 재설계해 해결
- 품절 상품이 결제까지 진행되던 경로에 **재고 재조회 하드 가드** 적용 (조회 실패 시 오차단을 막는 fail-open 설계)
- 구독 시작일이 UTC 변환으로 하루 밀리던 타임존 버그, 화면마다 다르던 구독 상태 판정을 유틸 단일화로 해결

**1차 런칭 품질 (CI · 보안 · SEO · 성능)**
- CI가 없던 레포에 typecheck·build·test 차단 게이트 신설, vitest 도입 후 순수함수 테스트 40케이스 작성
- 백엔드 오리진이 클라이언트 번들에 노출된 것을 빌드 산출물 분석으로 발견 → same-origin 프록시로 재구성, **노출 11건 → 0건** · 오픈 SSRF 라우트 제거
- canonical 15페이지 명시 · sitemap 276 URL · Product/Recipe JSON-LD 등 SEO 기반 신설
- 레포에 커밋돼 있던 **정적 에셋 290MB**를 Supabase Storage 서빙으로 이관, next/image 전환 · 한/영 i18n 구축

**커머스 운영 도구 · B2B · 백엔드**
- 운영 관리자 화면 초기 구축부터 전담 — 상품 CRUD, 상세페이지 편집기 + Figma export HTML 파이프라인, 재고·출고(fulfillment) 관리
- 수출 B2B 사이트 — FOB 자동견적(실시간 환율 · 인코텀즈), 컨테이너 적재 시뮬레이션, **12로케일 i18n · 아랍어 RTL**
- 공장 HACCP 관리자 — 완제품 재고 · LOT · 출고 관리, 현장용 모바일 UI 전면 개편
- Spring 백엔드 FOB API 작업 — 인증 필터체인 분기(공개/인증/403) 설계와 보안 슬라이스 테스트 작성

### 🔬 인천대학교 인공지능빅데이터센터 — 학생연구원 <sub>2026.05 ~ 2027.01(예정)</sub>

- INU-챗봇 자율운영을 위한 Agent 개발 — 학칙·규정 문서 기반 **RAG 파이프라인** 구축, LLM 환각 억제를 위한 답변 검증 시스템 개발 참여
- 교내 INTIP 플랫폼 프론트엔드 · 챗봇 UI/UX 구현

---

## 📌 Featured Projects

| 프로젝트 | 설명 | 기술 |
|---------|------|------|
| 🥗 **VeggieVerse** · [🔗 Live](https://slunch.co.kr/) | 비건 식단 구독 자사몰(B2C 커머스). 결제·구독·마이페이지부터 관리자·B2B·공장 HACCP 화면까지 **5개 레포 500+ 커밋** 전담, 1차 런칭 <sub>(사내 비공개 레포)</sub> | Next.js · TypeScript · TanStack Query · Toss Payments |
| 💬 **[memorIN](https://github.com/inu-appcenter/memorIN)** | 일상 아카이빙 + 통합 메신저 소셜 서비스. **백엔드 시니어**로 온프레미스 저사양 서버 대상 API 설계 · 코드리뷰 · 성능 튜닝 | Spring Boot 3.5 · PostgreSQL 18 · MinIO · STOMP |
| 🌌 **[GitGalaxy](https://github.com/kimdoyoung1110/gitgalaxy)** · [🔗 Live](https://frontend-three-delta-41.vercel.app) | GitHub 저장소 **약 1,900개 · 10만+ 데이터 포인트**를 3D 우주로 실시간 시각화. Web Worker · InstancedMesh로 **60fps** 달성 | React · Three.js · R3F |
| 🧭 **[DevRoad](https://github.com/kimdoyoung1110/DevRoad)** | 채용 트렌드 · 모의 면접 서비스. 번들 최적화로 **TBT 72%↓**, 초기 페이로드 **99%↓** | Next.js · TypeScript · Recharts |
| 🤖 **[AppCenter AI Server](https://github.com/inu-appcenter/AppCenter-AI-Server)** | 앱센터 통합 AI 서버 — **RAG 기반 LLM 챗봇** 백엔드 API | Spring Boot · Python · RAG |
| 🛒 **[CartrAIder](https://github.com/CartrAIder)** | 스마트 AI 카트 고객용 모바일 앱 — 상품 인식 · 결제 흐름 | React Native · Expo · TypeScript |

> 🔎 프로젝트별 상세 성과는 **[포트폴리오 사이트](https://doyoungkim-portfolio.vercel.app/)** 에서 확인하실 수 있어요.

---

## 🛠️ Tech Stack

### Frontend
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![TanStack Query](https://img.shields.io/badge/TanStack%20Query-FF4154?style=for-the-badge&logo=reactquery&logoColor=white)
![Zustand](https://img.shields.io/badge/Zustand-443E38?style=for-the-badge&logo=react&logoColor=white)
![React Native](https://img.shields.io/badge/React%20Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=threedotjs&logoColor=white)
![Vitest](https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white)

### Backend
![Java](https://img.shields.io/badge/Java-007396?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket%20%C2%B7%20STOMP-010101?style=for-the-badge&logo=socketdotio&logoColor=white)

### DB & Infra
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

---

## 🏢 Organizations

| 조직 | 소개 | 역할 |
|------|------|------|
| **[Slunch Factory](https://github.com/slunch-factory)** | AI 비건 식단 구독 푸드테크 스타트업 | 자사몰 VeggieVerse 커머스 전담 (프론트엔드 인턴, 5개 레포 500+ 커밋) |
| **[인천대 앱센터](https://github.com/inu-appcenter)** | 인천대학교 개발 동아리 | memorIN 백엔드 시니어 · 통합 AI 서버 백엔드 |
| **[CartrAIder](https://github.com/CartrAIder)** | 스마트 AI 카트 프로젝트 | 고객용 모바일 앱 (React Native) |
| **[Techeer](https://www.techeer.net/)** | 실리콘밸리 개발자 커리어 그룹 | 기술 스터디 · GitGalaxy 3D 시각화 |

---

## 📊 GitHub Stats

<p align="center">
  <img height="180em" src="https://github-readme-stats.vercel.app/api?username=kimdoyoung1110&show_icons=true&theme=tokyonight&include_all_commits=true&count_private=true"/>
  <img height="180em" src="https://github-readme-stats.vercel.app/api/top-langs/?username=kimdoyoung1110&layout=compact&theme=tokyonight&langs_count=8"/>
</p>

---

## 📫 Contact

<p align="center">
  <a href="https://doyoungkim-portfolio.vercel.app/"><img src="https://img.shields.io/badge/Portfolio-6366F1?style=for-the-badge&logo=vercel&logoColor=white"/></a>
  <a href="https://www.linkedin.com/in/do-young-kim-2823b53aa/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
  <a href="https://velog.io/@kdy9883/posts"><img src="https://img.shields.io/badge/Velog-20C997?style=for-the-badge&logo=velog&logoColor=white"/></a>
  <a href="https://blog.naver.com/ehdud9883"><img src="https://img.shields.io/badge/Naver%20Blog-03C75A?style=for-the-badge&logo=naver&logoColor=white"/></a>
  <a href="mailto:from.dozero@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white"/></a>
</p>

<p align="center">
  <i>"오늘보다 내일 더 나은 개발자가 되겠습니다." ✨</i>
</p>
