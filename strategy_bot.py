#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전략기획실장 (Strategy Bot)
================================

에티버스 그룹의 전략기획실장 역할을 수행하는 대화형 AI 봇입니다.
- B2B IT 솔루션 / 벤더 파트너십 / 시장 분석 / 경영진 보고서 작성 전문
- 한국어로 정중하고 간결하게 답변
- 대화 기록을 ~/Documents/AI-Work/logs/strategy/ 에 날짜별 txt로 저장
- 'quit' 입력 시 종료

실행 방법:
    pip install anthropic
    export ANTHROPIC_API_KEY="your-api-key-here"
    python strategy_bot.py
"""

import os
import sys
from datetime import datetime

import anthropic

# ── 설정 ─────────────────────────────────────────────────────────────
MODEL = "claude-opus-4-8"
MAX_TOKENS = 8000
LOG_DIR = os.path.expanduser("~/Documents/AI-Work/logs/strategy")

SYSTEM_PROMPT = (
    "당신은 에티버스 그룹의 전략기획실장입니다.\n"
    "B2B IT 솔루션, 벤더 파트너십, 시장 분석, 경영진 보고서 작성이 전문입니다.\n"
    "항상 정중하고 간결하게 답변하며, 복잡한 정보는 표나 목록으로 정리합니다.\n"
    "에티버스 그룹은 41개 벤더 포트폴리오를 보유한 Cisco 파트너사입니다."
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
    print("🏢  전략기획실장 (에티버스 그룹)")
    print("    B2B IT · 벤더 전략 · 경영진 보고서")
    print("    종료하려면 'quit' 을 입력하세요.")
    print("=" * 56)

    while True:
        try:
            user_input = input("\n감독님 ▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n전략기획실장: 업무를 종료합니다. 수고하셨습니다.")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("\n전략기획실장: 업무를 종료합니다. 수고하셨습니다.")
            break

        append_log("감독", user_input)
        messages.append({"role": "user", "content": user_input})

        # 스트리밍으로 응답 출력
        print("\n전략기획실장 ◀ ", end="", flush=True)
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
        append_log("전략기획실장", reply)


if __name__ == "__main__":
    main()
