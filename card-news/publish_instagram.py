#!/usr/bin/env python3
"""
인스타그램 캐러셀 자동 발행 (Meta Graph API)
- 카드 10장(cards/card-01~10.png)을 하나의 캐러셀 게시물로 발행합니다.
- ⚠️ 액세스 토큰은 .env(로컬, git 제외) 또는 환경변수로만 읽습니다.
       토큰을 코드/깃/채팅에 절대 넣지 마세요.

필요 환경변수 (.env):
  IG_USER_ID       인스타 '비즈니스/크리에이터' 계정의 IG User ID
  IG_ACCESS_TOKEN  장기(Long-lived) 액세스 토큰
  IMAGE_BASE_URL   카드 이미지가 공개로 접근되는 베이스 URL (끝 슬래시 제외)
                   예) https://cdn.jsdelivr.net/gh/OWNER/REPO@COMMIT/card-news/cards
                   ※ 인스타 API는 '공개 https 이미지 URL'만 받습니다(비공개 저장소 불가).

사용:
  pip install requests python-dotenv
  cp .env.example .env          # 값 채우기
  python3 publish_instagram.py --dry-run   # URL 접근성만 점검(발행 X)
  python3 publish_instagram.py             # 실제 발행
"""
import os, sys, time, glob, pathlib, requests

HERE = pathlib.Path(__file__).resolve().parent
try:
    from dotenv import load_dotenv
    load_dotenv(HERE / ".env")
except Exception:
    pass

GRAPH = "https://graph.facebook.com/v21.0"


def need(key, dry=False):
    v = os.getenv(key)
    if not v and not dry:
        sys.exit(f"❌ 환경변수 {key} 가 필요합니다 (.env 확인)")
    return v or f"<{key}>"


def main():
    dry = "--dry-run" in sys.argv
    ig_id = need("IG_USER_ID", dry)
    token = need("IG_ACCESS_TOKEN", dry)
    base = need("IMAGE_BASE_URL", dry).rstrip("/")

    cap_file = HERE / os.getenv("CAPTION_FILE", "caption.txt")
    caption = cap_file.read_text(encoding="utf-8").strip() if cap_file.exists() else ""

    cards = sorted(glob.glob(str(HERE / "cards" / "card-*.png")))
    if not cards:
        sys.exit("❌ cards/card-*.png 이미지를 찾을 수 없습니다.")
    urls = [f"{base}/{pathlib.Path(c).name}" for c in cards]
    print(f"📇 카드 {len(urls)}장, 베이스: {base}\n")

    # 0) 이미지 공개 URL 접근성 점검
    all_ok = True
    for u in urls:
        try:
            r = requests.head(u, allow_redirects=True, timeout=30)
            ct = r.headers.get("content-type", "")
            ok = r.status_code == 200 and ct.startswith("image")
        except Exception as e:
            ok, ct = False, str(e)
            r = type("x", (), {"status_code": "ERR"})()
        all_ok &= ok
        print(("✅" if ok else "❌"), r.status_code, ct, u)

    if dry:
        print("\n[dry-run] 발행은 생략했습니다.")
        print("→ 위가 모두 ✅면 .env에 IG_USER_ID·IG_ACCESS_TOKEN 채우고 옵션 없이 실행하세요.")
        return
    if not all_ok:
        sys.exit("\n❌ 일부 이미지가 공개 image로 접근되지 않습니다. IMAGE_BASE_URL/호스팅을 확인하세요.")

    # 1) 각 이미지 → 캐러셀 아이템 컨테이너
    child_ids = []
    for u in urls:
        j = requests.post(f"{GRAPH}/{ig_id}/media", timeout=60, data={
            "image_url": u, "is_carousel_item": "true", "access_token": token,
        }).json()
        if "id" not in j:
            sys.exit(f"❌ 아이템 생성 실패: {j}")
        child_ids.append(j["id"])
        print("  item", j["id"])

    # 2) 캐러셀 컨테이너
    j = requests.post(f"{GRAPH}/{ig_id}/media", timeout=60, data={
        "media_type": "CAROUSEL", "children": ",".join(child_ids),
        "caption": caption, "access_token": token,
    }).json()
    if "id" not in j:
        sys.exit(f"❌ 캐러셀 생성 실패: {j}")
    container = j["id"]
    print("📦 carousel", container)

    # 3) 컨테이너 처리 대기
    for _ in range(24):
        st = requests.get(f"{GRAPH}/{container}", timeout=30, params={
            "fields": "status_code", "access_token": token,
        }).json()
        code = st.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            sys.exit(f"❌ 컨테이너 처리 오류: {st}")
        print("  대기중...", code)
        time.sleep(5)

    # 4) 발행
    j = requests.post(f"{GRAPH}/{ig_id}/media_publish", timeout=60, data={
        "creation_id": container, "access_token": token,
    }).json()
    if "id" not in j:
        sys.exit(f"❌ 발행 실패: {j}")
    print("\n🎉 발행 완료! media id:", j["id"])


if __name__ == "__main__":
    main()
