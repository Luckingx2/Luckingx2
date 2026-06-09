#!/usr/bin/env python3
# 카드뉴스 index.html -> 인쇄용 print.html -> cards.pdf -> cards/card-NN.png
import re, os, pathlib
import weasyprint, fitz

HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / "fonts"
FONTS.mkdir(exist_ok=True)

# 한글 폰트 자동 다운로드(없을 때만)
FONT_URLS = {
    "BlackHanSans.ttf": "https://github.com/google/fonts/raw/main/ofl/blackhansans/BlackHanSans-Regular.ttf",
    "Jua.ttf": "https://github.com/google/fonts/raw/main/ofl/jua/Jua-Regular.ttf",
    "NotoSansKR.ttf": "https://github.com/notofonts/noto-cjk/raw/main/Sans/Variable/TTF/Subset/NotoSansKR-VF.ttf",
}
import urllib.request
for name, url in FONT_URLS.items():
    fp = FONTS / name
    if not fp.exists() or fp.stat().st_size < 1000:
        print("downloading font:", name)
        urllib.request.urlretrieve(url, fp)

src = (HERE / "index.html").read_text(encoding="utf-8")

# 1) Google Fonts <link>/<preconnect> 제거 (오프라인 렌더)
src = re.sub(r'<link[^>]*googleapis[^>]*>', '', src)
src = re.sub(r'<link[^>]*gstatic[^>]*>', '', src)
src = re.sub(r'<link rel="preconnect"[^>]*>', '', src)

# 2) 화면용 안내(intro)·하단 팁(print-tip) 제거
src = re.sub(r'<div class="intro">.*?</div>\s*', '', src, flags=re.S)
src = re.sub(r'<p class="print-tip">.*?</p>\s*', '', src, flags=re.S)

# 2-b) WeasyPrint는 컬러 이모지를 페이지 상단으로 튕기거나 클리핑하는 버그가 있음.
#      인쇄(PDF/PNG)본에서는 모든 컬러 이모지를 제거하고, 의미있는 아이콘은
#      SVG·번호·차트로 대체한다(화면용 index.html은 이모지 그대로 유지).
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF"      # 그림문자·기호·이모지
    "☀-➿"               # 기타기호+딩뱃(✂ 등)
    "⌀-⏿"               # ⏳ ⌛ ⏰
    "⬀-⯿"               # ⭐ 등
    "️⃣]")              # 변형선택자·키캡
src = EMOJI.sub('', src)
# 이모지 빠진 자리의 군더더기 공백 정리
src = re.sub(r' +<br>', '<br>', src)
src = re.sub(r'  +', ' ', src)

# 2-c) 원형 아이콘 통일: 카드별 일련번호로(컬러 이모지 클리핑 이슈 회피).
#      제목의 중복 동그라미 번호(①②③)는 제거.
src = src.replace('① ', '').replace('② ', '').replace('③ ', '')
_cnt = {'n': 0}
def _circ(m):
    if m.group('card') is not None:
        _cnt['n'] = 0
        return m.group(0)
    if m.group('inner').strip().isdigit():
        _cnt['n'] += 1
        return m.group(0)
    _cnt['n'] += 1
    return m.group('open') + str(_cnt['n']) + m.group('close')
src = re.compile(
    r'(?P<card><section class="card)'
    r'|(?P<open><div class="circ"[^>]*>)(?P<inner>[^<]*)(?P<close></div>)'
).sub(_circ, src)

# 3) 인쇄 오버라이드 + 로컬 한글/이모지 폰트 주입
override = f"""
<style id="print-override">
@font-face{{font-family:'Black Han Sans';src:url('file://{FONTS}/BlackHanSans.ttf');}}
@font-face{{font-family:'Jua';src:url('file://{FONTS}/Jua.ttf');}}
@font-face{{font-family:'Noto Sans KR';src:url('file://{FONTS}/NotoSansKR.ttf');}}
@page{{size:1080px 1080px;margin:0;}}
html,body{{background:#fff!important;padding:0!important;margin:0!important;}}
.deck{{display:block!important;gap:0!important;}}
.card{{width:1080px!important;height:1080px!important;max-width:none!important;
  aspect-ratio:auto!important;border-radius:0!important;box-shadow:none!important;
  margin:0!important;page-break-after:always;break-after:page;overflow:hidden;}}
.card:last-child{{page-break-after:auto;break-after:auto;}}
/* 원형 아이콘: flex 중앙정렬 대신 line-height 중앙정렬(이모지 튐 방지) */
.step .circ{{display:block!important;line-height:96px!important;text-align:center!important;padding:0!important;overflow:hidden;}}
/* 마지막 카드(로드맵): 스텝 풀폭 + 크기 축소로 넘침 방지 */
.deck .card:last-child .pad{{justify-content:flex-start!important;align-items:stretch!important;padding-top:66px!important;}}
.deck .card:last-child h2.big{{font-size:58px!important;margin-top:16px!important;}}
.deck .card:last-child .steps{{width:100%!important;gap:16px!important;margin-top:26px!important;}}
.deck .card:last-child .step{{padding:20px 30px!important;}}
.deck .card:last-child .step .circ{{width:80px!important;height:80px!important;flex-basis:80px!important;line-height:80px!important;font-size:38px!important;}}
.deck .card:last-child .step .txt b{{font-size:30px!important;margin-bottom:2px!important;}}
.deck .card:last-child .step .txt span{{font-size:22px!important;}}
.deck .card:last-child .pad > p{{font-size:26px!important;margin-top:24px!important;}}
</style>
</head>"""
src = src.replace("</head>", override, 1)

(HERE / "print.html").write_text(src, encoding="utf-8")

# 4) PDF 렌더
pdf_path = HERE / "재테크-카드뉴스.pdf"
weasyprint.HTML(string=src, base_url=str(HERE)).write_pdf(str(pdf_path))
print("PDF saved:", pdf_path, os.path.getsize(pdf_path), "bytes")

# 5) 페이지별 PNG (1080px)
out = HERE / "cards"; out.mkdir(exist_ok=True)
doc = fitz.open(str(pdf_path))
print("pages:", doc.page_count)
zoom = 1080 / 1080.0 * (1080 / (1080 * 72/96))  # 96dpi 기준 1080px
mat = fitz.Matrix(96/72, 96/72)  # 72pt page -> 96dpi px = 1080px
for i, page in enumerate(doc, 1):
    pix = page.get_pixmap(matrix=mat, alpha=False)
    fp = out / f"card-{i:02d}.png"
    pix.save(str(fp))
    print("saved", fp.name, pix.width, "x", pix.height)
print("DONE")
