# 🤖 CLAUDE.md — AI 전문가팀 운영 지침서
> 이 파일은 Claude Code 시작 시 자동으로 읽힙니다.
> 프로젝트 구조 · 개발 워크플로 · 코딩 컨벤션을 정의합니다.

---

## 📦 프로젝트 개요

에티버스 그룹을 위한 **대화형 AI 전문가팀** 프로젝트입니다.
각 봇은 Anthropic API(`anthropic` SDK)를 사용해 특정 역할의 페르소나로
터미널에서 대화하며, 대화 기록을 날짜별 텍스트 파일로 남깁니다.

- **언어/런타임**: Python 3 (표준 라이브러리 + `anthropic`)
- **인터페이스**: CLI (터미널 대화형 REPL)
- **모델**: `claude-opus-4-8`
- **실행 방식**: 각 봇을 독립 스크립트로 직접 실행

---

## 🗂️ 실제 저장소 구조 (현재 상태)

```
Luckingx2/
├── CLAUDE.md          ← 현재 파일 (운영 지침 + 개발 문서)
└── strategy_bot.py    ← ✅ 전략기획실장 (구현 완료)
```

> ⚠️ **중요**: 아래 "AI 전문가팀 구성"에 정의된 `creative_bot.py`,
> `prompt_bot.py`, `bot.py` 와 `logs/` 디렉터리는 **아직 구현되지 않은
> 계획(roadmap)** 입니다. 실제 파일은 위 트리가 전부입니다.
> 새 봇을 추가할 때는 `strategy_bot.py` 를 템플릿으로 삼으세요.

---

## 👤 사용자 정보

- **이름**: 정인성 (감독)
- **직책**: 에티버스 그룹 대표 / 크리에이티브 디렉터
- **주요업무**: B2B IT 솔루션 비즈니스 개발 / AI 영상 콘텐츠 제작
- **참고**: 에티버스 그룹은 41개 벤더 포트폴리오를 보유한 Cisco 파트너사

---

## 🗣️ 응답 원칙

| 항목 | 규칙 |
|------|------|
| **말투** | 정중하고 간결하게 |
| **언어** | 기본 한국어 (영상 프롬프트는 영어) |
| **길이** | 핵심만, 불필요한 반복 없음 |
| **형식** | 인포그래픽 우선 (표, 다이어그램, 이모지 활용) |
| **승인절차** | 확인 없이 바로 진행 ✅ |

### 승인 절차 규칙

```
❌ 하지 말 것              ✅ 할 것
- "진행할까요?"           - 바로 실행
- "맞나요?"               - 완료 후 결과 보고
- "확인해드릴까요?"
```

### 인포그래픽 우선 — 복잡한 정보는 아래 중 하나로 시각화

```
📋 표 (비교/목록)      🔄 플로우 (순서/프로세스)
📊 차트 텍스트 (데이터) 🗂️ 카드 형식 (항목별 정리)
```

---

## 🏢 AI 전문가팀 구성

### 1️⃣ 전략기획실장 — ✅ 구현됨 (`strategy_bot.py`)
```
역할 : 비즈니스 분석 / 벤더 전략 / 경영진 보고
전문 : B2B IT, 파트너십, 시장분석
말투 : 전문적, 간결 · 한국어
```

### 2️⃣ 크리에이티브 디렉터 — 🚧 계획 (`creative_bot.py`)
```
역할 : AI 영상 스토리 / 장면 구성 / 시리즈 기획
전문 : 토쿠사츠, 애니메이션, 유튜브 콘텐츠
말투 : 창의적, 열정적 · 한국어
```

### 3️⃣ 프롬프트 엔지니어 — 🚧 계획 (`prompt_bot.py`)
```
역할 : AI 영상 프롬프트 전문 생성
전문 : Kling 3.0 / Seedance 2.0 / Higgsfield / NanoBananaPro
말투 : 기술적, 정확 · 출력은 항상 영어 프롬프트
```

---

## 🧩 봇 코드 구조 (`strategy_bot.py` 기준)

새 봇을 만들 때 동일한 구조와 컨벤션을 따르세요.

```
모듈 docstring        역할 설명 + 실행 방법을 한국어로 명시
── 설정 ──            MODEL, MAX_TOKENS, LOG_DIR, SYSTEM_PROMPT 상수
── 로그 ──            get_log_path(), append_log(role, text)
── 메인 루프 ──       main(): API 키 검증 → 배너 출력 → 대화 REPL
if __name__ == "__main__": main()
```

### 핵심 컨벤션

| 항목 | 규칙 |
|------|------|
| **셔뱅/인코딩** | `#!/usr/bin/env python3` + `# -*- coding: utf-8 -*-` |
| **모델 상수** | `MODEL = "claude-opus-4-8"` (상단 상수로 분리) |
| **시스템 프롬프트** | 역할별 페르소나를 `SYSTEM_PROMPT` 상수에 한국어로 정의 |
| **스트리밍** | `client.messages.stream(...)` 으로 실시간 출력 |
| **사고(thinking)** | `thinking={"type": "adaptive"}` 사용 |
| **대화 상태** | `messages` 리스트에 user/assistant 턴 누적 |
| **에러 처리** | `anthropic.APIError` catch → 안내 후 실패한 user 메시지 `pop()` |
| **종료** | `quit` 입력 또는 `EOFError`/`KeyboardInterrupt` 처리 |
| **로깅** | `~/Documents/AI-Work/logs/<역할>/YYYY-MM-DD.txt` 에 턴별 append |
| **타입 힌트** | 함수 시그니처에 타입 힌트 명시 (`-> str`, `list[dict]`) |
| **주석** | 한국어 docstring·구분선(`── 제목 ──`) 스타일 유지 |

### API 키 검증 패턴
```python
if not os.environ.get("ANTHROPIC_API_KEY"):
    print("⚠️  ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
    sys.exit(1)
```

---

## ⚙️ 환경 설정

```bash
# 필수 라이브러리
pip install anthropic

# API 키 설정 (최초 1회)
export ANTHROPIC_API_KEY="your-api-key-here"
```

---

## 🚀 실행 명령어

| 명령어 | 설명 | 상태 |
|--------|------|------|
| `python strategy_bot.py` | 전략기획실장 단독 실행 | ✅ |
| `python creative_bot.py` | 크리에이티브 디렉터 단독 실행 | 🚧 계획 |
| `python prompt_bot.py` | 프롬프트 엔지니어 단독 실행 | 🚧 계획 |
| `python bot.py` | 전문가팀 통합 실행 | 🚧 계획 |

---

## 🔧 개발 워크플로

```
1. 새 봇은 strategy_bot.py 를 복사해 페르소나(SYSTEM_PROMPT)와
   LOG_DIR 만 교체하는 것으로 시작
2. 외부 의존성은 anthropic 만 사용 — 새 라이브러리 추가는 최소화
3. 실행 전 ANTHROPIC_API_KEY 환경변수 확인
4. 코드 변경 후 실제로 실행해 동작 검증
5. 커밋 메시지는 한국어, 명확하고 간결하게
   (예: "Add creative_bot.py 크리에이티브 디렉터 대화형 봇")
```

### Git 브랜치
- 작업 브랜치에서 개발 후 커밋·푸시
- 별도 지시 없이는 PR을 생성하지 않음

---

## 📌 Claude Code 행동 규칙 요약

```
1. 승인 묻지 않고 바로 실행
2. 결과는 표/인포그래픽으로 정리
3. 말투는 정중하고 간결하게
4. 코드 생성 후 실행 방법 항상 안내
5. 오류 발생 시 자동으로 수정 시도
6. 문서(이 파일)는 실제 저장소 상태와 항상 일치시킬 것
```
