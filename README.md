# AI Content Studio

AI 영상 프롬프트, 콘텐츠 리서치, 카드뉴스 제작·발행을 한곳에서 관리하는 작업 공간입니다.

## 안전 원칙

- 분석, 초안, 로컬 렌더링은 바로 실행할 수 있습니다.
- Git 커밋·푸시·PR, 파일 삭제, 외부 게시·발행은 감독님의 명시적 승인 후에만 수행합니다.
- API 키와 액세스 토큰은 `.env` 또는 환경변수로만 관리합니다.
- Instagram 발행기는 기본적으로 dry-run이며 `--confirm-publish` 없이는 발행하지 않습니다.

## 설치와 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
ai-content prompt --model kling_3 --subject "A swordsman runs through a burning forest"
pytest
```

## 구조

- `src/ai_content_studio/`: 공통 설정, 에이전트, 외부 발행 코드
- `templates/`: Kling 3.0, Seedance, Higgsfield, NanoBananaPro 템플릿
- `projects/`: 실제 콘텐츠 프로젝트
- `research/`: 기업·산업 리서치
- `tests/`: 승인 게이트와 템플릿 검증

## GitHub 반영 정책

이 디렉터리는 로컬 정리본입니다. 기존 저장소 또는 원격 브랜치에는 자동으로 반영되지 않습니다.

