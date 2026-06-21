#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
프롬프트 엔지니어 (Prompt Bot)
================================

에티버스 그룹의 AI 영상 프롬프트 엔지니어 역할을 수행하는 대화형 AI 봇입니다.
- Kling 3.0 / Seedance 2.0 / Higgsfield / NanoBananaPro 영상 프롬프트 전문 생성
- 항상 영어 프롬프트로 출력 (기술적·정확한 말투)
- 대화 기록을 ~/Documents/AI-Work/logs/prompt/ 에 날짜별 txt로 저장
- 'quit' 입력 시 종료

🎬 AI 영상 공식
    키워드 | Shot + Style + Lighting / Location + Action
    "좋은 프롬프트는 '무엇을 만들지'보다 '어떻게 보여줄지'를 설명합니다."

실행 방법:
    pip install anthropic
    export ANTHROPIC_API_KEY="your-api-key-here"
    python prompt_bot.py
"""

import os
import sys
from datetime import datetime

import anthropic

# ── 설정 ─────────────────────────────────────────────────────────────
MODEL = "claude-opus-4-8"
MAX_TOKENS = 8000
LOG_DIR = os.path.expanduser("~/Documents/AI-Work/logs/prompt")

# ── AI 영상 공식 ─────────────────────────────────────────────────────
# 키워드 | Shot + Style + Lighting / Location + Action
VIDEO_FORMULA = "Shot + Style + Lighting / Location + Action"

SYSTEM_PROMPT = (
    "당신은 에티버스 그룹의 AI 영상 프롬프트 엔지니어입니다.\n"
    "Kling 3.0, Seedance 2.0, Higgsfield, NanoBananaPro 등 최신 영상 생성 "
    "모델용 프롬프트 작성이 전문입니다.\n"
    "말투는 기술적이고 정확하며, 최종 영상 프롬프트는 항상 영어로 출력합니다.\n"
    "\n"
    "🎬 AI 영상 공식 (반드시 이 순서를 따릅니다):\n"
    f"    {VIDEO_FORMULA}\n"
    "    1) Shot      — 샷 종류·카메라 무빙 (e.g. wide shot, slow dolly-in, tracking shot)\n"
    "    2) Style     — 영상 톤·룩·장르 (e.g. cinematic, anime, tokusatsu, hyperrealistic)\n"
    "    3) Lighting  — 조명·시간대·분위기 (e.g. golden hour, soft rim light, neon glow)\n"
    "    4) Location  — 배경·공간·세계관 (e.g. rain-soaked Seoul street, futuristic lab)\n"
    "    5) Action    — 피사체의 동작·감정·변화 (e.g. turns slowly, eyes widen, dust rises)\n"
    "\n"
    "핵심 원칙: 좋은 프롬프트는 '무엇을 만들지'보다 '어떻게 보여줄지'를 설명합니다.\n"
    "(A good prompt describes HOW to show it, not just WHAT to make.)\n"
    "\n"
    "출력 형식:\n"
    "    1. 영어 영상 프롬프트 (공식 순서대로, 한 문단)\n"
    "    2. 공식 구성요소 분해 표 (Shot / Style / Lighting / Location / Action)\n"
    "    3. 권장 모델·설정 (해상도·길이·종횡비) 한 줄 코멘트\n"
)


# ── 로그 ─────────────────────────────────────────────────────────────
def get_log_path() -> str:
    """오늘 날짜 기준 로그 파일 경로를 반환합니다 (폴더 자동 생성)."""
    os.makedirs(LOG_DIR, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d") + ".txt"
    return os.path.join(LOG_DIR, filename)


def append_log(role: str, text: str) -> None:
    """대화 한 턴을 로그 파일에 추가합니다."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(get_log_path(), "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {role}: {text}\n")


# ── 메인 루프 ────────────────────────────────────────────────────────
def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        print('    export ANTHROPIC_API_KEY="your-api-key-here" 를 먼저 실행하세요.')
        sys.exit(1)

    client = anthropic.Anthropic()
    messages: list[dict] = []

    print("=" * 56)
    print("🎬  프롬프트 엔지니어 (에티버스 그룹)")
    print("    AI 영상 공식 | " + VIDEO_FORMULA)
    print("    Kling · Seedance · Higgsfield · NanoBananaPro")
    print("    종료하려면 'quit' 을 입력하세요.")
    print("=" * 56)

    while True:
        try:
            user_input = input("\n감독님 ▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n프롬프트 엔지니어: 작업을 종료합니다. 수고하셨습니다.")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("\n프롬프트 엔지니어: 작업을 종료합니다. 수고하셨습니다.")
            break

        append_log("감독", user_input)
        messages.append({"role": "user", "content": user_input})

        # 스트리밍으로 응답 출력
        print("\n프롬프트 엔지니어 ◀ ", end="", flush=True)
        reply_parts: list[str] = []
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                thinking={"type": "adaptive"},
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                    reply_parts.append(text)
            print()
        except anthropic.APIError as e:
            print(f"\n⚠️  API 오류가 발생했습니다: {e}")
            messages.pop()  # 실패한 user 메시지 제거
            continue

        reply = "".join(reply_parts)
        messages.append({"role": "assistant", "content": reply})
        append_log("프롬프트 엔지니어", reply)


if __name__ == "__main__":
    main()
