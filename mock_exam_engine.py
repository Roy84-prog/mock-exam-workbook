import json
import re
import os
import random
from playwright.sync_api import sync_playwright

# ========================================================
# [설정 영역: 교재 기본 정보]
# ========================================================
# 0. 출력 모드 설정 (True로 설정된 파일만 렌더링 및 저장됩니다)
CONFIG_MAKE_STUDENT = False
CONFIG_MAKE_TEACHER = False
CONFIG_MAKE_PRESENTATION = True

# 1. 헤더 및 타이틀 변경 내용을 맨 앞에서 수정할 수 있도록 변수화
CONFIG_ACADEMY_NAME = "With ROY"
CONFIG_SERIES_TAG = "2026 Curriculum"
CONFIG_SUB_TITLE = "빈순삽합 실전편 1-8회"
CONFIG_COPYRIGHT = "© CEDU 빈순삽합 실전편 구매한 학생들에게만 배부되는 수업용 자료입니다."
CONFIG_WATERMARK_TEXT = "Super"
CONFIG_TARGET_FOLDER = "3"

CONFIG_HEADER_TITLE = "빈순삽합 실전"
CONFIG_COVER_TITLE_HTML = '특목고 대비 <span class="highlight">READING - Part 1</span>'
CONFIG_ENG_TITLE_MAIN = "SG"
CONFIG_ENG_TITLE_SUB = "어학원"

# 2. 학생용/교사용 줄간격(Line Height) 설정
CONFIG_LH_TYPE_1 = "2.4"
CONFIG_LH_TYPE_2 = "2.4"
CONFIG_LH_TYPE_3 = "2.4"
CONFIG_LH_TYPE_4 = "2.4"
CONFIG_LH_TYPE_5 = "2.2"
CONFIG_LH_TYPE_6 = "2.4"
CONFIG_LH_TYPE_7 = "2.4"
CONFIG_LH_TYPE_8 = "2.4"
CONFIG_LH_TYPE_9 = "2.0"

CONFIG_LH_BOX = "1.9"
CONFIG_LH_CHUNK = "2.2"

# 3. 프리젠테이션(수업용 화면) 전용 지문 폰트 및 줄간격 설정
CONFIG_FONT_SIZE_PRESENTATION = "15.5px"
CONFIG_LH_PRESENTATION = "2.4"

# 장문 독해(9번 유형) 전용 수업용 폰트 및 줄간격 분리
CONFIG_FONT_SIZE_PRES_TYPE_9 = "14.5px"
CONFIG_LH_PRES_TYPE_9 = "2.0"

CONFIG_LH_PRES_BLANK_BOX = "2.0"
CONFIG_LH_PRES_CHUNK = "2.2"

# 4. 프리젠테이션(수업용 화면) 전용 단어표 크기 및 폰트 설정
CONFIG_PRES_VOCAB_WIDTH = "220mm"
CONFIG_PRES_VOCAB_ROW_HEIGHT = "68px"
CONFIG_PRES_VOCAB_WORD_SIZE = "19px"
CONFIG_PRES_VOCAB_MEAN_SIZE = "14px"
CONFIG_PRES_VOCAB_CHUNK_EN_SIZE = "13.5px"
CONFIG_PRES_VOCAB_CHUNK_KO_SIZE = "12px"

# 5. 프리젠테이션(수업용 화면) 여백 설정
CONFIG_PRES_PADDING_TOP = "3.5mm"
CONFIG_PRES_MARGIN_LEFT = "15mm"


# ========================================================

# ========================================================
# [새 기능 추가] HTML을 PDF로 저장하는 함수
# ========================================================
def save_html_to_pdf(html_content, output_pdf_path):
    """
    HTML 문자열을 입력받아 지정된 경로에 PDF 파일로 저장하는 함수입니다.

    :param html_content: PDF로 변환할 원본 HTML 문자열
    :param output_pdf_path: 저장될 PDF 파일의 경로 및 이름 (예: 'output.pdf')
    """
    with sync_playwright() as p:
        # 백그라운드(Headless) 모드로 크롬 브라우저 실행
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 브라우저 페이지에 HTML 내용 삽입
        page.set_content(html_content)

        # ⚠️ 중요: 웹 폰트(구글 폰트 등)가 완전히 로드될 때까지 대기하여 폰트 깨짐 방지
        page.evaluate("document.fonts.ready")

        # 수업용 화면의 JS(문장 자르기/가리기)가 모두 실행될 수 있도록 약간 대기
        page.wait_for_timeout(300)

        # A4 사이즈(가로 방향), 배경색 포함, 여백 없이 PDF 저장
        page.pdf(
            path=output_pdf_path,
            format="A4",
            landscape=True,  # 교재 방향이 가로(landscape)이므로 추가
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )

        # 브라우저 종료
        browser.close()


# ========================================================
# [1. HTML/CSS 템플릿: Premium Workbook V80]
# ========================================================
WORKBOOK_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>Premium Workbook V80 (Secret Note Update)</title>
<style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Noto+Sans+KR:wght@300;400;500;700;900&family=Noto+Serif+KR:wght@400;600;700&display=swap');
    @import url('https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@1.0/nanumsquareround.css');
    @import url('https://cdn.jsdelivr.net/npm/font-kopub@1.0/kopubbatang.min.css');

    @media print {
        body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .page-break { page-break-after: always; }
        .page-container { margin: 0 !important; border: none !important; box-shadow: none !important; width: 297mm !important; height: 210mm !important; }
        @page { size: A4 landscape; margin: 0; }
    }

    :root {
        --c-brand: #003b6f; --c-accent: #00897b; --c-text: #263238; --c-gray-line: #cfd8dc;
        --lf-blue-bg: #e3f2fd; --lf-blue-text: #1565c0;
        --lf-org-bg: #fff8e1; --lf-org-text: #ef6c00;
        --lf-grn-bg: #e8f5e9; --lf-grn-text: #2e7d32;
        --lp-logic-bg: #7e57c2; --lp-gram-bg: #26a69a;

        /* Vocab용 변수 */
        --font-eng: 'Montserrat', sans-serif;
        --c-synonym: #795548;
        --c-chunk-text: #263238; 
        --c-chunk-hl: #d84315;
    }

    body { margin: 0; padding: 0; background-color: #e0e0e0; font-family: 'Noto Sans KR', sans-serif; color: var(--c-text); }

    .page-container {
        width: 297mm; height: 210mm; background-color: white;
        margin: 20px auto; padding: 0; box-sizing: border-box; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); position: relative;
        display: flex; flex-direction: column; overflow: hidden;
    }

    /* Header & Footer */
    .page-header { height: 10mm; min-height: 10mm; max-height: 10mm; border-top: 5px solid var(--c-brand); border-bottom: 2px solid #b0bec5; display: flex; justify-content: space-between; align-items: center; padding: 0 15mm; box-sizing: border-box; overflow: hidden; }
    .ph-left { display: flex; align-items: center; font-family: 'Montserrat', 'Noto Sans KR', sans-serif; }
    .ph-title-main { font-weight: 800; color: var(--c-text); font-size: 14px; letter-spacing: -0.5px; }
    .ph-title-num { font-weight: 900; color: var(--c-brand); font-size: 14px; margin-left: 4px; }
    .unit-badge-group { display: flex; align-items: center; margin-left: 12px; font-family: 'Montserrat', sans-serif; }
    .ub-label { background-color: var(--c-brand); color: white; font-size: 9px; font-weight: 700; padding: 3px 6px; border-top-left-radius: 4px; border-bottom-left-radius: 4px; }
    .ub-num { background-color: var(--c-accent); color: white; font-size: 9px; font-weight: 800; padding: 3px 8px; border-top-right-radius: 4px; border-bottom-right-radius: 4px; }

    .ph-right { display: flex; align-items: center; gap: 6px; font-family: 'Montserrat', sans-serif; font-size: 14px; color: #5d4037; font-weight: 800; letter-spacing: -0.2px; }
    .yt-icon { width: 20px; height: 14px; display: block; }

    .page-footer { margin-top: auto; height: 8mm; min-height: 8mm; display: flex; justify-content: center; align-items: flex-start; padding-top: 1mm; font-family: 'Montserrat', sans-serif; font-size: 11px; color: #78909c; font-weight: 800; box-sizing: border-box; letter-spacing: 1px; }

    /* Cover Page */
    .cover-layout { flex: 1; padding: 20mm; background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 60%, #e3f2fd 100%); display: flex; flex-direction: column; justify-content: center; position: relative; overflow: hidden; }
    .geo-shape { position: absolute; z-index: 0; }
    .shape-1 { top: -15%; right: -10%; width: 600px; height: 600px; background: var(--c-brand); opacity: 0.05; clip-path: polygon(25% 0%, 100% 0%, 75% 100%, 0% 100%); transform: rotate(30deg); }
    .shape-2 { bottom: 5%; left: -5%; width: 400px; height: 400px; background: var(--c-accent); opacity: 0.04; clip-path: polygon(0% 0%, 100% 100%, 0% 100%); }
    .bg-text-overlay { position: absolute; z-index: 0; opacity: 0.06; font-family: 'Montserrat'; font-weight: 900; font-size: 180px; color: var(--c-brand); top: -30px; right: -10px; letter-spacing: -10px; }
    .brand-logo { font-family: 'Montserrat', 'NanumSquareRound', sans-serif; font-weight: 900; font-size: 28px; color: var(--c-brand); margin-bottom: 50px; display: flex; align-items: center; gap: 10px; position: relative; z-index: 1; }
    .brand-svg { width: 40px; height: 40px; color: var(--c-accent); }
    .title-section { position: relative; z-index: 1; margin-bottom: 60px; }
    .series-tag { background: var(--c-brand); color: white; padding: 6px 16px; font-size: 11px; font-weight: 700; border-radius: 20px; display: inline-block; margin-bottom: 20px; font-family: 'Montserrat', sans-serif; letter-spacing: 2px; text-transform: uppercase; box-shadow: none; }
    .main-tit { font-size: 64px; font-weight: 900; color: var(--c-text); letter-spacing: -2px; line-height: 1.05; margin-bottom: 15px; font-family: 'Montserrat', 'Noto Sans KR', sans-serif; }
    .main-tit .highlight { color: var(--c-accent); } 
    .sub-tit { font-size: 22px; font-weight: 500; color: #546e7a; border-left: 4px solid var(--c-accent); padding-left: 18px; font-family: 'Noto Sans KR', sans-serif; letter-spacing: -0.3px; }

    .bottom-info { display: flex; justify-content: flex-end; align-items: flex-end; border-top: 2px solid rgba(0,59,111,0.1); padding-top: 30px; position: relative; z-index: 1; }
    .input-area { display: flex; gap: 25px; }
    .input-group { display: flex; flex-direction: column; }
    .input-label { font-size: 11px; color: #b0bec5; font-weight: 700; margin-bottom: 6px; font-family: 'Montserrat'; text-transform: uppercase; }
    .input-box { border-bottom: 2px solid #cfd8dc; width: 140px; height: 24px; }

    /* Page 2: Main Study */
    .p2-body { flex: 1; display: flex; flex-direction: column; padding: 2mm 5mm 0mm 10mm; box-sizing: border-box; min-height: 0; }
    .p2-top-wrap { display: flex; flex: 1; gap: 35mm; min-height: 0; }
    .left-col { flex: 1.4; display: flex; flex-direction: column; overflow: hidden; }

    .q-stem-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; margin-top: 2px; }
    .question-stem { font-family: 'Noto Serif KR', serif; font-weight: 700; font-size: 15px; color: #263238; border-left: 4px solid var(--c-brand); padding-left: 10px; line-height: 1.4; margin: 0; flex: 1; }
    .q-diff-badge { background: #eceff1; color: #455a64; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 4px; font-family: 'Montserrat', 'Noto Sans KR', sans-serif; margin-left: 15px; white-space: nowrap; }

    /* 유형별 본문 줄간격 클래스 동적 할당 */
    .passage-content { flex: 1; font-family: 'KoPub Batang', 'KoPubBatang', serif; font-size: 15.5px; text-align: justify; color: #212121; padding-left: 5px; }
    .passage-content.type-1 { line-height: ___CONFIG_LH_TYPE_1___; }
    .passage-content.type-2 { line-height: ___CONFIG_LH_TYPE_2___; }
    .passage-content.type-3 { line-height: ___CONFIG_LH_TYPE_3___; }
    .passage-content.type-4 { line-height: ___CONFIG_LH_TYPE_4___; }
    .passage-content.type-5 { line-height: ___CONFIG_LH_TYPE_5___; }
    .passage-content.type-6 { line-height: ___CONFIG_LH_TYPE_6___; }
    .passage-content.type-7 { line-height: ___CONFIG_LH_TYPE_7___; }
    .passage-content.type-8 { line-height: ___CONFIG_LH_TYPE_8___; }
    .passage-content.type-9 { line-height: ___CONFIG_LH_TYPE_9___; font-size: 14.5px; } 

    .passage-footnotes { margin-top: 8px; border-top: 1px dashed #cfd8dc; padding-top: 6px; font-family: 'KoPub Batang', serif; font-size: 12px; font-weight: 700; color: #546e7a; line-height: 1.4; }
    .passage-box { border: 2px solid #b0bec5; border-radius: 8px; padding: 8px 12px; background-color: #fafafa; margin-bottom: 8px; font-family: 'KoPub Batang', serif; font-size: 15.5px; line-height: ___CONFIG_LH_BOX___; }
    .box-container { border: 2px solid #b0bec5; border-radius: 8px; padding: 8px 12px; background-color: #fafafa; margin-bottom: 10px; font-family: 'KoPub Batang', serif; font-size: 15.5px; line-height: ___CONFIG_LH_BOX___; }

    .order-chunk { margin-bottom: 10px; padding-left: 5px; line-height: ___CONFIG_LH_CHUNK___; }
    .summary-sentence-box { border: 2px solid var(--c-accent); border-radius: 8px; padding: 10px; background-color: #e0f2f1; margin-top: 10px; font-weight: 600; color: #004d40; }
    .para-mark { color: var(--c-brand); font-weight: 900; margin-right: 4px; font-family: 'Montserrat'; font-size: 1.1em; }

    .right-col { flex: 0.75; display: flex; flex-direction: column; height: 100%; gap: 8px; }
    .secret-note { flex: 1; border: 1px solid var(--c-gray-line); border-radius: 8px; display: flex; flex-direction: column; overflow: hidden; min-height: 0; }
    .sn-header { background: var(--c-brand); color: white; padding: 6px 12px; font-size: 12px; font-weight: 700; letter-spacing: 1px; }
    .sn-body { flex: 1; background: white; padding: 20px; background-image: linear-gradient(#eeeeee 1px, transparent 1px); background-size: 100% 25px; }
    .sn-item { margin-bottom: 12px; font-family: 'NanumSquareRound', sans-serif; font-size: 12px; line-height: 1.5; }
    .sn-label { font-weight: 800; color: var(--c-accent); margin-right: 4px; }
    .sn-text { color: #37474f; font-weight: 600; }

    .lp-wrapper { flex: 0 0 auto; display: flex; flex-direction: column; overflow: hidden; }
    .lp-title-outside { font-family: 'NanumSquareRound', sans-serif; font-size: 13px; font-weight: 800; color: #37474f; margin-bottom: 2px; display: flex; align-items: center; gap: 5px; padding-left: 2px; }
    .lp-box { border: 1px solid #cfd8dc; border-radius: 8px; background: #fff; padding: 6px 8px; display: flex; flex-direction: column; overflow: hidden; font-family: 'NanumSquareRound', sans-serif; }
    .lp-content-area { display: flex; flex-direction: column; gap: 4px; }
    .lp-section { margin-bottom: 2px; }
    .lp-badge { display: inline-block; padding: 1px 6px; border-radius: 8px; font-size: 10px; font-weight: 800; color: white; margin-bottom: 2px; font-family: 'NanumSquareRound', sans-serif; }
    .badge-logic { background-color: var(--lp-logic-bg); }
    .badge-grammar { background-color: var(--lp-gram-bg); }
    .lp-list { list-style-type: none; margin: 0; padding-left: 5px; }
    .lp-item { font-size: 10px; color: #37474f; line-height: 1.35; margin-bottom: 2px; text-align: justify; font-family: 'NanumSquareRound', sans-serif; position: relative; padding-left: 8px; letter-spacing: -0.2px; }
    .lp-item::before { content: "-"; position: absolute; left: 0; color: #b0bec5; font-size: 10px; }
    .lp-item b { color: #d32f2f; font-weight: 800; }

    .p2-bottom-wrap { flex: 0 0 auto; margin-top: 8px; display: flex; flex-direction: column; gap: 6px; }
    .options-box { background: white; border: 2px dashed #b0bec5; border-radius: 8px; padding: 10px 14px; display: flex; flex-direction: column; justify-content: center; margin-bottom: 0px; }
    .opt-title { font-size: 11px; font-weight: 800; color: #78909c; margin-bottom: 8px; display: block; }
    .opt-sub-question { font-size: 12.5px; font-weight: 800; color: #263238; margin-bottom: 6px; display: block; font-family: 'Noto Serif KR', serif; }

    .opt-item-wrapper { margin-bottom: 4px; display: flex; flex-direction: column; gap: 3px; }
    .opt-item-wrapper:last-child { margin-bottom: 0; }
    .opt-row { display: block; font-size: 12.5px; color: #000000; line-height: 1.4; font-family: 'KoPub Batang', 'KoPubBatang', serif; }
    .opt-row:hover { color: var(--c-brand); font-weight: 700; cursor: pointer; }

    .why-card { background-color: #f8f9fa; border: 1px solid #eceff1; border-left: 4px solid #cfd8dc; border-radius: 6px; padding: 3px 8px; display: flex; align-items: center; gap: 8px; margin-left: 2px; min-height: 20px;}
    .why-badge { background-color: #f1f8e9; border: 1px solid #a5d6a7; color: #388e3c; font-weight: 800; font-size: 9px; padding: 1px 5px; border-radius: 4px; font-family: 'NanumSquareRound', sans-serif; letter-spacing: 0.5px; }

    /* Page 3: Worksheet */
    .p3-body { flex: 1; padding: 5mm 5mm 0mm 10mm; display: flex; flex-direction: column; gap: 12px; box-sizing: border-box; min-height: 0; }
    .p3-top { flex: 1.35; display: flex; gap: 15px; min-height: 0; } 

    .summary-card { flex: 0.75; border: 1px solid #e6ee9c; background: #fffde7; border-radius: 8px; padding: 15px; display: flex; flex-direction: column; }
    .sum-header-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 10px; }
    .card-label { font-size: 14px; font-weight: 800; color: #37474f; margin-bottom: 0; display: flex; align-items: center; gap:6px; font-family: 'Montserrat', 'Noto Sans KR', sans-serif; }
    .sum-sub-guide { font-size: 11px; color: #90a4ae; font-weight: 700; font-family: 'NanumSquareRound', sans-serif; letter-spacing: -0.5px; }
    .icon-s { width:16px; height:16px; background:#546e7a; color:white; font-size:10px; display:flex; justify-content:center; align-items:center; border-radius:4px; font-family: 'Montserrat'; font-weight: 900; }

    .sum-content-wrapper { flex: 1; display: flex; flex-direction: column; }
    .sum-box-eng { font-family: 'KoPub Batang', 'KoPubBatang', serif; font-size: 13.5px; line-height: 1.65; color: #263238; margin-bottom: 12px; text-align: justify; font-weight: 500; }
    .sum-write-area { flex: 1; margin-bottom: 10px; }
    .inter-head { font-size: 11px; color: #f9a825; font-weight: 800; margin-bottom: 4px; font-family: 'Montserrat'; }
    .write-line { border-bottom: 1px solid #cfd8dc; height: 22px; margin-bottom: 4px; }

    .sec-vocab { flex: 1.25; display: flex; flex-direction: column; margin-top: 0px; border: 1px solid #cfd8dc; border-radius: 8px; overflow: hidden; }
    .v-header { display: flex; background: #37474f; color: white; font-family: var(--font-eng); font-size: 11px; font-weight: 700; padding: 6px 0; border-bottom: 1px solid #cfd8dc; }
    .v-list { flex: 1; display: flex; flex-direction: column; overflow-y: hidden; background: white; }
    .v-row { display: flex; align-items: stretch; border-bottom: 1px solid #eceff1; padding: 0; min-height: 32px; flex: 1; }
    .v-row:nth-child(even) { background-color: #fafafa; } 

    .cell { display: flex; align-items: center; padding: 1px 8px; border-right: 1px solid rgba(0,0,0,0.05); box-sizing: border-box; overflow: hidden; }
    .cell:last-child { border-right: none; }
    .v-header .cell { border-right: 1px solid rgba(255,255,255,0.2); justify-content: center; padding: 3px 8px; text-align: center; }
    .v-header .cell:last-child { border-right: none; }

    .col-chk { width: 30px; justify-content: center; flex-shrink: 0; }
    .col-word { width: 24%; flex-shrink: 0; }
    .col-mean { width: 30%; flex-shrink: 0; flex-direction: column; justify-content: center; align-items: flex-start; }
    .col-chunk { flex: 1; flex-direction: column; justify-content: center; align-items: flex-start; overflow: hidden; }

    .v-row .col-chk { align-items: flex-start; padding-top: 6px; }
    .v-row .col-word { align-items: flex-start; padding-top: 5px; }
    .v-row .col-mean { justify-content: flex-start; padding-top: 5px; }
    .v-row .col-chunk { justify-content: flex-start; padding-top: 5px; }

    .cell.col-word { border-right: 1px solid rgba(0,0,0,0.05); } 
    .v-header .cell.col-word { border-right: 1px solid rgba(255,255,255,0.2); position: relative; align-items: center; padding-top: 3px; }

    .chk-box { width: 10px; height: 10px; border: 1px solid var(--c-brand); border-radius: 2px; background: white; }
    .word-txt { font-family: var(--font-eng); font-weight: 800; color: var(--c-brand); font-size: 12.5px; word-break: break-word; line-height: 1.1; } 
    .vm-kor { font-weight: 800; color: #212121; font-size: 12px; line-height: 1.3; font-family: 'NanumSquareRound', sans-serif; display: block; width: 100%;}
    .vm-syn { font-family: var(--font-eng); line-height: 1.1; margin-top: 2px; color: var(--c-synonym); font-weight: 400; background: rgba(78, 52, 46, 0.08); padding: 2px 4px; border-radius: 4px; display: inline-block; width: 100%; box-sizing: border-box;}
    .vm-syn::before { content: "≒ "; font-weight: 800; opacity: 0.7; }

    .vch-en { font-family: var(--font-eng); font-weight: 600; color: var(--c-chunk-text); font-size: 11px; line-height: 1.3; margin-bottom: 2px; display: block; width: 100%; }
    .vch-ko { font-size: 10px; color: #78909c; line-height: 1.1; font-family: 'NanumSquareRound', sans-serif; display: block; width: 100%; }
    .c-hl { color: var(--c-chunk-hl); font-weight: 800; } 

    .p3-bottom { flex: 0.85; display: flex; flex-direction: column; padding-top: 10px; }
    .flow-header-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 10px; border-bottom: 2px solid #eceff1; padding-bottom: 6px; }
    .flow-label { font-size: 15px; font-weight: 800; color: #37474f; margin-bottom: 0; display: flex; align-items: center; gap:8px; font-family: 'Montserrat', 'Noto Sans KR', sans-serif; }
    .icon-f { width:18px; height:18px; background:#ef5350; color:white; font-size:12px; display:flex; justify-content:center; align-items:center; border-radius:4px; font-family: 'Montserrat'; font-weight: 900; }
    .flow-sub-guide { font-size: 11px; color: #90a4ae; font-weight: 700; font-family: 'NanumSquareRound', sans-serif; letter-spacing: -0.5px; }

    .flow-container { display: flex; gap: 10px; height: 100%; align-items: stretch; }
    .flow-box { flex: 1; border-radius: 8px; display: flex; flex-direction: column; border: 1px solid #cfd8dc; overflow: hidden; background: white; }
    .fb-header { padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; }
    .flow-box.theme-blue .fb-header { background-color: #e3f2fd; border-bottom: 1px solid rgba(0,0,0,0.05); } 
    .flow-box.theme-yel .fb-header { background-color: #fff8e1; border-bottom: 1px solid rgba(0,0,0,0.05); } 
    .flow-box.theme-grn .fb-header { background-color: #e8f5e9; border-bottom: 1px solid rgba(0,0,0,0.05); } 
    .fb-title-label { font-family: 'Montserrat', sans-serif; font-size: 15px; font-weight: 900; color: #000; }
    .fb-range-pill { background-color: white; color: #546e7a; font-size: 11px; font-weight: 800; padding: 4px 12px; border-radius: 20px; font-family: 'Montserrat', sans-serif; box-shadow: none; }
    .fb-body { flex: 1; padding: 12px; display: flex; flex-direction: column; gap: 6px; }
    .fb-body.student-empty { min-height: 80px; } 
    .fb-line { border-bottom: 1px dashed #cfd8dc; height: 24px; width: 100%; }
    .fb-body-text { font-family: 'KoPub Batang', serif; font-size: 12px; line-height: 1.6; color: #455a64; text-align: justify; }
    .fb-body-text b { color: #d32f2f; font-weight: 800; }
    .fb-body-text.teacher-ans { font-family: 'Noto Sans KR', 'NanumSquareRound', sans-serif; font-size: 11.5px; color: #1565c0; font-weight: 500; }
    .arrow-wrap { display: flex; align-items: center; justify-content: center; color: #90a4ae; font-size: 18px; font-weight: 400; padding: 0 4px; }

    /* ================= 속지(Unit Divider) ================= */
    .divider-layout { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%); position: relative; overflow: hidden; }
    .div-unit-box { text-align: center; z-index: 1; background: white; padding: 60px 100px; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,59,111,0.08); border-top: 6px solid var(--c-brand); border-bottom: 6px solid var(--c-accent); position: relative; }
    .div-unit-box::before { content: "___CONFIG_ENG_TITLE_MAIN___"; position: absolute; top: -14px; left: 50%; transform: translateX(-50%); background: var(--c-brand); color: white; font-size: 11px; font-weight: 800; padding: 4px 16px; border-radius: 12px; font-family: 'Montserrat', sans-serif; letter-spacing: 1.5px; white-space: nowrap; }
    .div-label { font-size: 20px; color: #90a4ae; font-weight: 800; font-family: 'Montserrat', sans-serif; letter-spacing: 6px; margin-bottom: 5px; }
    .div-num { font-size: 120px; font-weight: 900; color: var(--c-brand); font-family: 'Montserrat', sans-serif; line-height: 1; margin-bottom: 25px; letter-spacing: -4px; }
    .div-line { width: 60px; height: 5px; background: var(--c-accent); margin: 0 auto 20px auto; border-radius: 2.5px; }
    .div-desc { font-size: 18px; color: #455a64; font-weight: 700; font-family: 'Noto Sans KR', sans-serif; letter-spacing: -0.5px; }

    /* ================= 누적 Review Test Layout ================= */
    .p2-voca-body { flex: 1; padding: 5mm 5mm 0mm 10mm; display: flex; flex-direction: column; gap: 0; background: #fff; box-sizing: border-box; min-height: 0;}
    .review-split { display: flex; gap: 5mm; height: 100%; box-sizing: border-box; align-items: stretch; }

    .rev-col-left { flex: 6; display: flex; flex-direction: column; gap: 15px; }
    .rev-col-right { flex: 4; display: flex; flex-direction: column; height: 100%; }

    .test-section-card { background: #fff; border-radius: 8px; border: 1px solid #cfd8dc; overflow: hidden; display: flex; flex-direction: column; }
    .test-sec-title { background: #f8fafd; padding: 8px 12px; border-bottom: 1px solid #eceff1; font-size: 13px; font-weight: 800; color: #37474f; font-family: 'NanumSquareRound', sans-serif; display: flex; align-items: center; gap: 8px; }
    .icon-v { background: #5c6bc0; width:18px; height:18px; color:white; font-size:12px; display:flex; justify-content:center; align-items:center; border-radius:4px; font-family: 'Montserrat', sans-serif; font-weight: 900;} 

    .td-flex-wrap { display: flex; align-items: flex-start; gap: 4px; width: 100%; }
    .q-num { flex-shrink: 0; width: 20px; color: #90a4ae; font-size: 10.5px; font-weight: 800; font-family: 'Montserrat', sans-serif; text-align: left; padding-top: 1px; }
    .word-text-wrap { flex: 1; word-break: break-word; }

    .step1-container { display: flex; gap: 0; }
    .step1-table { width: 50%; border-collapse: collapse; font-family: 'Noto Sans KR', sans-serif; table-layout: fixed; }
    .step1-table:first-child { border-right: 1px solid #eceff1; }
    .step1-table th { background: #ffffff; color: #78909c; padding: 6px; font-size: 10px; border-bottom: 1px solid #eceff1; font-family: 'Montserrat', sans-serif; text-transform: uppercase; }
    .step1-table td { padding: 4px 8px; border-bottom: 1px solid #b0bec5; vertical-align: middle; height: 26px; overflow: hidden; }
    .step1-table th:first-child, .step1-table td:first-child { border-right: 1px solid #eceff1; }

    .step2-container { display: flex; flex-direction: column; gap: 10px; padding: 10px 15px; background: #fafafa;}
    .step2-box { background: #fff; border: 1px solid #eceff1; border-radius: 6px; padding: 6px 10px; margin-bottom: 10px; }
    .step2-box:last-child { margin-bottom: 0; }
    .step2-subtable { width: 100%; border-collapse: collapse; font-family: 'Noto Sans KR', sans-serif; table-layout: fixed; }
    .step2-subtable td { border-bottom: 1px dashed #b0bec5; vertical-align: middle; overflow: hidden; padding: 0; }
    .step2-subtable tr:last-child td { border-bottom: none; }

    .step3-card { flex: 1; display: flex; flex-direction: column; background: #fff; border-radius: 8px; border: 1px solid #cfd8dc; overflow: hidden; height: 100%; }
    .step3-table-container { flex: 1; display: flex; }
    .step3-table { width: 100%; height: 100%; border-collapse: collapse; font-family: 'Noto Sans KR', sans-serif; table-layout: fixed; }
    .step3-table th { background: #ffffff; color: #78909c; padding: 6px; font-size: 10px; border-bottom: 1px solid #eceff1; font-family: 'Montserrat', sans-serif; text-transform: uppercase; height: 26px; }
    .step3-table td { padding: 5px 10px; vertical-align: middle; border-bottom: 1px solid #b0bec5; }
    .step3-table tbody tr:last-child td { border-bottom: none; }

    .tt-word { font-family: 'Montserrat', sans-serif; font-weight: 800; color: var(--c-brand); font-size: 12px; }
    .tt-mean-p1 { font-weight: 800; color: #212121; line-height: 1.2; word-break: keep-all; font-family: 'NanumSquareRound', sans-serif; }

    .step3-chunk-text { color:#37474f; line-height:1.6; font-size: 11.5px; font-family: 'Montserrat', 'KoPub Batang', serif; letter-spacing: -0.2px; }
    .step3-ko-text { color:#1565c0; font-weight: 800; font-size: 11.5px; font-family: 'NanumSquareRound', sans-serif; letter-spacing: -0.3px; }

    .tt-empty-box { height: 18px; } 
    .chunk-hl { font-weight: 800; color: #d32f2f; text-decoration: underline; } 

    /* ====================================================================== */
    /* [기능 추가] Interlinear Vocab & Highlights CSS */
    /* ====================================================================== */
    .vocab-container { display: inline; position: relative; text-indent: 0; line-height: 1.0; }
    .vocab-text { color: inherit; border-bottom: 1px dotted #bbb; font-weight: inherit; }
    .vocab-sub { position: absolute; top: 100%; left: 50%; transform: translateX(-50%); width: max-content; margin-top: 1px; font-size: 9px; color: #4e342e; background-color: transparent; text-shadow: 1px 1px 0 #eeeeee, -1px -1px 0 #eeeeee, 1px -1px 0 #eeeeee, -1px 1px 0 #eeeeee; padding: 0 1px; font-weight: bold; font-family: 'NanumSquareRound', sans-serif; z-index: 10; line-height: 1.1; pointer-events: none; }

    span[class^="highlight-"] { 
        border-radius: 4px; padding: 2px 4px; margin: 0 1px; 
        -webkit-box-decoration-break: clone; box-decoration-break: clone; 
        position: relative; z-index: 1; 
    }
    span[class^="highlight-"]::before { content: none; display: none; }

    /* 노란색 형광펜 -> 검정색 네모칸 (#000000) */
    .highlight-subject { background-color: transparent; border: 2px solid #000000; } 
    .highlight-feature { background-color: transparent; border: 2px solid #000000; }

    /* 파란색 형광펜 -> 연한 파스텔톤 (#e1f5fe) */
    .highlight-clue { background-color: #e1f5fe; border-bottom: 2px solid #b3e5fc; } 

    /* [수정] 끊어진 문장 회색 연결 (Continuity Fade) - 약간 더 또렷한 은회색 설정 */
    .fade-text { color: #b0bec5 !important; opacity: 0.35; pointer-events: none; transition: opacity 0.3s; }
    /* ====================================================================== */
</style>
</head>
<body>
"""


def highlight_chunk_word(target_word, full_sentence):
    if not target_word or not full_sentence: return full_sentence
    clean_word = re.sub(r'\(.*?\)', '', target_word.lower().strip()).strip()
    base = clean_word
    if len(base) > 3:
        if base.endswith('y'):
            base = base[:-1]
        elif base.endswith('e'):
            base = base[:-1]
        elif base.endswith('s'):
            base = base[:-1]
    pattern = r'\b' + re.escape(base) + r'[a-z]*'
    try:
        return re.sub(pattern, lambda m: f'<span class="c-hl">{m.group()}</span>', full_sentence, flags=re.IGNORECASE)
    except:
        return full_sentence


def get_shrink_style(text, max_len=20, base_size=11.5):
    t_len = sum(1.8 if ord('가') <= ord(c) <= ord('힣') else 1.0 for c in text)

    style = "white-space: nowrap; overflow: visible; "
    diff = t_len - max_len

    if diff >= 20:
        style += f"font-size: {max(7.0, base_size - 3.0)}px; letter-spacing: -0.6px;"
    elif diff >= 14:
        style += f"font-size: {max(8.0, base_size - 2.0)}px; letter-spacing: -0.4px;"
    elif diff >= 8:
        style += f"font-size: {max(9.0, base_size - 1.5)}px; letter-spacing: -0.3px;"
    elif diff >= 4:
        style += f"font-size: {max(10.0, base_size - 1.0)}px; letter-spacing: -0.2px;"
    elif diff > 0:
        style += f"font-size: {max(10.5, base_size - 0.5)}px; letter-spacing: -0.1px;"
    else:
        style += f"font-size: {base_size}px;"
    return style


def is_valid_synonym(syn):
    if not syn: return False
    clean = syn.strip().upper()
    if clean in ['', '-', 'N', 'A', 'N/A', 'NONE', 'X']: return False
    return True


# ==============================================================================
# [기능 추가] 파이썬 함수 모음 (단어 파싱, 루비 문자 적용, 형광펜 처리)
# ==============================================================================
def parse_local_vocab(word_str):
    if not word_str: return []
    result = []
    items = word_str.split(',')
    for item in items:
        if ':' in item:
            parts = item.split(':', 1)
            w = parts[0].strip()
            m = parts[1].strip()
            result.append({'word': w, 'meaning': m})
    return result


def apply_vocab_style(text, vocab_list_dicts):
    if not vocab_list_dicts: return text
    sorted_vocab = sorted(vocab_list_dicts, key=lambda x: len(x.get('word', '').split('[')[0].split('(')[0].strip()),
                          reverse=True)

    # HTML 태그를 건드리지 않기 위해 태그를 기준으로 텍스트를 나눔
    parts = re.split(r'(<[^>]+>)', text)

    for v in sorted_vocab:
        raw_word = v.get('word', '').split('[')[0].split('(')[0].strip()
        meaning = v.get('meaning', '').replace('①', '').replace('②', ',').strip()
        meaning = re.sub(r'\(.*?\)', '', meaning).strip()
        if not raw_word or len(raw_word) < 2: continue

        try:
            # 정규식 \b를 통해 독립된 단어만 정확히 매칭 (대소문자 구분 안 함)
            pattern = re.compile(rf'\b({re.escape(raw_word)})\b', re.IGNORECASE)
            replacement = rf'<span class="vocab-container"><span class="vocab-sub">{meaning}</span><span class="vocab-text">\g<1></span></span>'
            # 짝수 인덱스(일반 텍스트)에만 치환 적용
            for i in range(0, len(parts), 2):
                parts[i] = pattern.sub(replacement, parts[i])
        except:
            pass
    return "".join(parts)


def preprocess_multiline_tags(text):
    highlight_tags = ['subject', 'keyword', 'feature', 'clue', 'clue1', 'clue2']

    for tag in highlight_tags:
        clean_tag = tag.strip()
        pattern = re.compile(rf'(《{tag}》)(.*?)(《\/{clean_tag}》)', re.DOTALL)

        def replacer(match):
            open_t = match.group(1)
            content = match.group(2)
            close_t = match.group(3)

            if '\n' in content:
                parts = content.split('\n')
                wrapped = [f"{open_t}{p}{close_t}" for p in parts]
                return '\n'.join(wrapped)
            return match.group(0)

        text = pattern.sub(replacer, text)
    return text


def convert_common_tags(text):
    text = re.sub(r'《subject》(.*?)《/subject》', r'<span class="highlight-subject">\1</span>', text, flags=re.DOTALL)
    text = re.sub(r'《keyword》(.*?)《/keyword》', r'<span class="highlight-subject">\1</span>', text, flags=re.DOTALL)
    text = re.sub(r'《feature》(.*?)《/feature》', r'<span class="highlight-feature">\1</span>', text, flags=re.DOTALL)
    text = re.sub(r'《clue》(.*?)《/clue》', r'<span class="highlight-clue">\1</span>', text, flags=re.DOTALL)
    text = re.sub(r'《clue1》(.*?)《/clue1》', r'<span class="highlight-clue">\1</span>', text, flags=re.DOTALL)
    text = re.sub(r'《clue2》(.*?)《/clue2》', r'<span class="highlight-clue">\1</span>', text, flags=re.DOTALL)
    return text


# ==============================================================================


def create_cover_page(meta_data):
    cover_title_html = CONFIG_COVER_TITLE_HTML

    return f"""
    <div class="page-container page-break">
        <div class="page-header">
            <div class="ph-left"><span class="ph-title-main">{CONFIG_ENG_TITLE_MAIN}</span><span class="ph-title-num">{CONFIG_ENG_TITLE_SUB}</span></div>
            <div class="ph-right"></div>
        </div>
        <div class="cover-layout">
            <div class="geo-shape shape-1"></div><div class="geo-shape shape-2"></div>
            <div class="bg-text-overlay">{CONFIG_WATERMARK_TEXT}</div>
            <div class="brand-logo">
                <svg class="brand-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 3L1 9L12 15L21 10.09V17H23V9M5 13.18V17.18L12 21L19 17.18V13.18L12 17L5 13.18Z" fill="currentColor"/>
                    <path d="M18.5 3.5L20.5 5.5L22.5 3.5L20.5 1.5L18.5 3.5Z" fill="currentColor"/>
                </svg>
                {CONFIG_ACADEMY_NAME}
            </div>
            <div class="title-section">
                <span class="series-tag">{CONFIG_SERIES_TAG}</span>
                <div class="main-tit">{cover_title_html}</div>
                <div class="sub-tit">{CONFIG_SUB_TITLE}</div>
            </div>
            <div class="bottom-info">
                <div class="input-area">
                    <div class="input-group"><span class="input-label">Class</span><div class="input-box"></div></div>
                    <div class="input-group"><span class="input-label">Name</span><div class="input-box"></div></div>
                </div>
            </div>
        </div>
        <div class="page-footer" style="justify-content: center;">{CONFIG_COPYRIGHT}</div>
    </div>
    """


def create_back_cover_page():
    return f"""
    <div class="page-container page-break">
        <div class="page-header">
            <div class="ph-left"><span class="ph-title-main">{CONFIG_ENG_TITLE_MAIN}</span><span class="ph-title-num">{CONFIG_ENG_TITLE_SUB}</span></div>
            <div class="ph-right"></div>
        </div>
        <div class="cover-layout">
            <div class="geo-shape shape-1"></div><div class="geo-shape shape-2"></div>
            <div class="bg-text-overlay">{CONFIG_WATERMARK_TEXT}</div>
        </div>
        <div class="page-footer" style="justify-content: center;"></div>
    </div>
    """


def create_unit_divider(unit_num):
    return f"""
    <div class="page-container page-break">
        <div class="divider-layout">
            <div class="geo-shape shape-1" style="opacity: 0.03;"></div>
            <div class="geo-shape shape-2" style="opacity: 0.02;"></div>
            <div class="div-unit-box">
                <div class="div-label">UNIT</div>
                <div class="div-num">{unit_num}</div>
                <div class="div-line"></div>
                <div class="div-desc">{CONFIG_SUB_TITLE}</div>
            </div>
        </div>
        <div class="page-footer">- __PAGE_NUM__ -</div>
    </div>
    """


def generate_unit_pages(json_data_str, is_teacher):
    data = json.loads(json_data_str)
    meta = data.get('meta_info', {})
    visual = data.get('visual_data', {})

    try:
        difficulty = int(meta.get('difficulty_level', 3))
    except:
        difficulty = 3
    stars_html = "★" * difficulty + "☆" * (5 - difficulty)
    time_limit_str = "2 min 30 sec" if difficulty == 4 else ("3 min" if difficulty == 5 else "2 min")

    source_origin = meta.get('source_origin', '')
    unit_match = re.search(r'(\d+)', source_origin)
    unit_num = unit_match.group(1).zfill(2) if unit_match else "00"

    question_header = meta.get('question_header', '')
    range_match = re.search(r'(\d+)[\-~](\d+)', question_header)
    if range_match:
        q_num = f"{range_match.group(1)},{range_match.group(2)}"
        is_long_passage = True
    else:
        q_num_match = re.search(r'(\d+)', question_header)
        q_num = q_num_match.group(1).zfill(2) if q_num_match else "00"
        is_long_passage = False

    badge_text = f"{unit_num} - {q_num}"
    badge_text_p3 = f"Unit {badge_text}"
    cover_title_plain = CONFIG_HEADER_TITLE

    # =======================================================
    # [기능 적용] 원문 처리 (형광펜 및 뜻 적용)
    # =======================================================
    raw_text = visual.get('question_text_visual', '')
    raw_text = re.sub(r'《BLANK》.*?《/BLANK》', ' ____________ ', raw_text)

    if is_teacher:
        # 1. 형광펜 강조 처리 (Teacher 전용)
        raw_text = preprocess_multiline_tags(raw_text)
        raw_text = convert_common_tags(raw_text)

    # 2. 불필요한 태그 제거 및 줄바꿈 보정
    clean_text = re.sub(r'《[^》]+》', '', raw_text)
    clean_text = clean_text.replace('\n', ' ')

    if is_teacher:
        # 3. 단어 루비 문자 처리 (Teacher 전용)
        vocab_list_dicts = []
        for sent in data.get('sentence_analysis', []):
            ctx = sent.get('context_meaning', '')
            if ctx:
                vocab_list_dicts.extend(parse_local_vocab(ctx))
        if not vocab_list_dicts:
            vocab_list_dicts = data.get('vocab_list', [])

        clean_text = apply_vocab_style(clean_text, vocab_list_dicts)

    final_passage_html = re.sub(r'([❶-❿⓫-⓴①-⑳])', r'<span class="para-mark">\1</span>', clean_text)
    # =======================================================

    try:
        q_type = int(meta.get('question_type', 0))
    except:
        q_type = 0

    if q_type == 4:
        parts = re.split(r'(\([ABC]\))', final_passage_html)
        if len(parts) > 1:
            box_content = parts[0]
            new_html = f'<div class="box-container">{box_content}</div>'
            for i in range(1, len(parts), 2):
                label = parts[i]
                content = parts[i + 1] if i + 1 < len(parts) else ""
                new_html += f'<div class="order-chunk"><span class="para-mark">{label}</span>{content}</div>'
            final_passage_html = new_html
    elif q_type == 5:
        match = re.search(r'(<span class="para-mark">❶</span>.*?)(?=<span class="para-mark">❷</span>)',
                          final_passage_html)
        if match:
            box_content = match.group(1)
            rest_content = final_passage_html[match.end():]
            final_passage_html = f'<div class="box-container">{box_content}</div>{rest_content}'
    elif q_type == 6:
        summary_keyword_match = re.search(r'(Summary|요약문)', final_passage_html, re.IGNORECASE)
        if summary_keyword_match:
            split_idx = summary_keyword_match.start()
            main_text = final_passage_html[:split_idx]
            summary_text = final_passage_html[split_idx:]
            final_passage_html = f'{main_text}<div class="summary-sentence-box">{summary_text}</div>'
        else:
            last_mark_match = list(re.finditer(r'<span class="para-mark">[❶-❿⓫-⓴①-⑳]</span>', final_passage_html))
            if last_mark_match:
                last_idx = last_mark_match[-1].start()
                main_text = final_passage_html[:last_idx]
                summary_text = final_passage_html[last_idx:]
                final_passage_html = f'{main_text}<div class="summary-sentence-box">{summary_text}</div>'

    footnotes = visual.get('footnotes', [])
    if not footnotes: footnotes = data.get('footnotes', [])
    if footnotes:
        note_text = "  ".join(footnotes)
        final_passage_html += f'<div class="passage-footnotes">{note_text}</div>'

    is_insertion_prob = (q_type == 5) or ("들어갈 곳" in question_header) or ("삽입" in question_header)

    effective_q_type = q_type
    if is_long_passage or q_type == 9:
        effective_q_type = 9
    elif is_insertion_prob:
        effective_q_type = 5
    elif effective_q_type not in range(1, 10):
        effective_q_type = 1

    passage_div_class = f"passage-content type-{effective_q_type}"

    raw_options_visual = visual.get('options_visual', [])
    options_html = ""

    ans_data = data.get('answer_data', {})
    raw_main_answer = str(ans_data.get('correct_choice', meta.get('answer', data.get('answer', ''))))

    circle_map = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
    main_correct_ans_num = -1
    found_circle = False
    for c_char, c_num in circle_map.items():
        if c_char in raw_main_answer:
            main_correct_ans_num = c_num
            found_circle = True
            break

    if not found_circle:
        ans_m = re.search(r'([1-5])', raw_main_answer)
        if ans_m:
            main_correct_ans_num = int(ans_m.group(1))

    if raw_options_visual and isinstance(raw_options_visual[0], dict):
        for prob_idx, prob_obj in enumerate(raw_options_visual):
            sub_q = prob_obj.get("sub_question", "")
            opts = prob_obj.get("options", ["① ", "② ", "③ ", "④ ", "⑤ "])

            if sub_q and (effective_q_type == 9 or is_long_passage):
                options_html += f'<span class="opt-sub-question">{sub_q}</span>'

            for idx, opt in enumerate(opts):
                if is_insertion_prob:
                    opt = re.sub(r'^\s*\(\s*([①-⑤])\s*\)', r'\1', opt)
                    opt = re.sub(r'^\s*([①-⑤])', r'( \1 )', opt)

                is_correct = False
                if len(raw_options_visual) == 1:
                    is_correct = (is_teacher and (idx + 1) == main_correct_ans_num)
                opt_style = ' style="color:#d32f2f; font-weight:900;"' if is_correct else ''

                if effective_q_type == 9 or is_long_passage:
                    options_html += f"""
                    <div class="opt-item-wrapper">
                        <span class="opt-row"{opt_style}>{opt}</span>
                    </div>
                    """
                else:
                    options_html += f"""
                    <div class="opt-item-wrapper">
                        <span class="opt-row"{opt_style}>{opt}</span>
                        <div class="why-card">
                            <span class="why-badge">why?</span>
                            <div style="flex:1;"></div>
                        </div>
                    </div>
                    """
            if prob_idx < len(raw_options_visual) - 1:
                options_html += '<div style="height: 15px;"></div>'
    else:
        options = raw_options_visual if raw_options_visual else ["① ", "② ", "③ ", "④ ", "⑤ "]
        for idx, opt in enumerate(options):
            if is_insertion_prob:
                opt = re.sub(r'^\s*\(\s*([①-⑤])\s*\)', r'\1', opt)
                opt = re.sub(r'^\s*([①-⑤])', r'( \1 )', opt)

            is_correct = (is_teacher and (idx + 1) == main_correct_ans_num)
            opt_style = ' style="color:#d32f2f; font-weight:900;"' if is_correct else ''

            if effective_q_type == 9 or is_long_passage:
                options_html += f"""
                <div class="opt-item-wrapper">
                    <span class="opt-row"{opt_style}>{opt}</span>
                </div>
                """
            else:
                options_html += f"""
                <div class="opt-item-wrapper">
                    <span class="opt-row"{opt_style}>{opt}</span>
                    <div class="why-card">
                        <span class="why-badge">why?</span>
                        <div style="flex:1;"></div>
                    </div>
                </div>
                """

    final_options_div = f'<div class="options-box"><span class="opt-title">▼ CHOICES</span>{options_html}</div>'

    topic_data = data.get('topic_data', {})

    if is_teacher:
        korean_topic = topic_data.get('korean_topic', topic_data.get('keywords', ''))
        easy_summary = topic_data.get('easy_summary', topic_data.get('summary', ''))
        secret_note_body = f"""
        <div class="sn-body" style="overflow: visible;">
            <div style="background: white; padding-bottom: 5px; position: relative; z-index: 100; min-height: 100%;">
                <div class="sn-item"><span class="sn-label">소재:</span> <span class="sn-text">{korean_topic}</span></div>
                <div class="sn-item"><span class="sn-label">요약:</span> <span class="sn-text">{easy_summary}</span></div>
            </div>
        </div>"""
        secret_note_div = f'<div class="secret-note" style="overflow: visible; z-index: 100;"><div class="sn-header">SECRET NOTE</div>{secret_note_body}</div>'
    else:
        secret_note_body = """<div class="sn-body"><div style="color:#ccc; font-size:12px; text-align:center; margin-top:20px;">Analysis Space<br>(Structure / Grammar / Logic)</div></div>"""
        secret_note_div = f'<div class="secret-note"><div class="sn-header">SECRET NOTE</div>{secret_note_body}</div>'

    lp_data = data.get('learning_point', {})
    logic_points = lp_data.get('logic', [])
    grammar_points = lp_data.get('grammar', [])

    def format_lp_item(text):
        return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    lp_logic_html = "".join([f"<li class='lp-item'>{format_lp_item(item)}</li>" for item in logic_points])
    lp_grammar_html = "".join([f"<li class='lp-item'>{format_lp_item(item)}</li>" for item in grammar_points])

    vocab_rows = ""
    vocab_subset = data.get('vocab_list', [])[:10]

    for idx, v in enumerate(vocab_subset):
        chunk_raw = v.get('chunk_example', '')
        chunk_en_hl = highlight_chunk_word(v.get('word', ''), chunk_raw)
        chunk_ko = v.get('chunk_translation', '')

        synonyms = v.get('synonym', '')
        if is_valid_synonym(synonyms):
            syn_parts = [s.strip() for s in synonyms.replace('/', ',').split(',') if s.strip()]
            clean_syn = ", ".join(syn_parts)
            syn_style = get_shrink_style(clean_syn, 25, 10.5)
            syn_html = f'<div class="vm-syn" style="{syn_style}">{clean_syn}</div>'
        else:
            clean_syn = ""
            syn_html = ""

        raw_mean = v.get('meaning', '')
        clean_mean = re.sub(r'[①-⑳]', '|', raw_mean)
        clean_mean = re.sub(r'\(.*?\)', '', clean_mean).strip()
        parts = [p.strip() for p in clean_mean.split('|') if p.strip()]
        final_mean = ", ".join(parts)

        mean_style = get_shrink_style(final_mean, 22, 12.0)

        c_en_style = get_shrink_style(chunk_raw, max_len=30, base_size=11.0)
        c_ko_style = get_shrink_style(chunk_ko, max_len=20, base_size=10.0)

        vocab_rows += f"""
        <div class="v-row">
            <div class="cell col-chk"><div class="chk-box"></div></div>
            <div class="cell col-word"><span class="word-txt">{v.get("word", "")}</span></div>
            <div class="cell col-mean"><span class="vm-kor" style="{mean_style}">{final_mean}</span>{syn_html}</div>
            <div class="cell col-chunk">
                <span class="vch-en" style="{c_en_style}">{chunk_en_hl}</span>
                <span class="vch-ko" style="{c_ko_style}">{chunk_ko}</span>
            </div>
        </div>
        """

    vocab_block = f"""
    <div class="sec-vocab">
        <div class="v-header">
            <div class="cell col-chk">Chk</div>
            <div class="cell col-word">Word</div>
            <div class="cell col-mean">Mean & Syn</div>
            <div class="cell col-chunk">Chunk Example</div>
        </div>
        <div class="v-list">{vocab_rows}</div>
    </div>
    """

    logic_data = data.get('three_stage_flow', [])
    if not logic_data: logic_data = data.get('logic_map', [])
    steps = [{"theme": "theme-blue"}, {"theme": "theme-yel"}, {"theme": "theme-grn"}]

    flow_chart_html = ""
    for i, step in enumerate(steps):
        range_text, title_text, content_text = "", "", ""
        if i < len(logic_data) and isinstance(logic_data[i], dict):
            range_text = logic_data[i].get("range", "")
            title_text = logic_data[i].get("title", "")
            content_raw = logic_data[i].get("content", "")

            if is_teacher:
                content_text = re.sub(r'《fill》(.*?)《/fill》', r'<b>\1</b>', content_raw)
                content_text = re.sub(r'《[^》]+》', '', content_text)
                content_text = re.sub(r'([^\n>])\s+([①-⑳]|\d+\.)', r'\1<br>\2', content_text)

        if is_teacher:
            title_display = f"Title : {title_text}" if title_text else "Title :"
            flow_chart_html += f"""
            <div class="flow-box {step['theme']}">
                <div class="fb-header">
                    <span class="fb-title-label">{title_display}</span>
                    <span class="fb-range-pill">{range_text}</span>
                </div>
                <div class="fb-body"><div class="fb-body-text teacher-ans">{content_text}</div></div>
            </div>"""
        else:
            flow_chart_html += f"""
            <div class="flow-box {step['theme']}">
                <div class="fb-header">
                    <span class="fb-title-label">Title :</span>
                    <span class="fb-range-pill">{range_text}</span>
                </div>
                <div class="fb-body student-empty">
                    <div class="fb-line"></div>
                    <div class="fb-line"></div>
                    <div class="fb-line"></div>
                    <div class="fb-line"></div>
                </div>
            </div>"""

        if i < 2:
            flow_chart_html += '<div class="arrow-wrap">→</div>'

    csat_prob = topic_data.get('csat_summary_problem', {})
    summary_eng_raw = csat_prob.get('summary_text', "요약문 데이터가 없습니다.")
    summary_ans = csat_prob.get('correct_answer', csat_prob.get('answer', "-"))
    summary_kor = csat_prob.get('translation', "-")

    ans_A = ""
    ans_B = ""
    m = re.search(r'\([Aa]\)\s*(.*?)\s*\([Bb]\)\s*(.*)', summary_ans)
    if m:
        ans_A = m.group(1).strip(" ,/")
        ans_B = m.group(2).strip(" ,/")
    else:
        ans_parts = [a.strip() for a in re.split(r'[,/]', summary_ans) if a.strip()]
        if len(ans_parts) >= 1: ans_A = ans_parts[0]
        if len(ans_parts) >= 2: ans_B = ans_parts[1]

    ans_A = re.sub(r'^\([Aa]\)\s*', '', ans_A)
    ans_B = re.sub(r'^\([Bb]\)\s*', '', ans_B)

    if not ans_A or ans_A == '-':
        m_a = re.search(r'\([Aa]\)[^a-zA-Z]*([a-zA-Z\s]+)', summary_kor)
        if m_a: ans_A = m_a.group(1).strip()
    if not ans_B or ans_B == '-':
        m_b = re.search(r'\([Bb]\)[^a-zA-Z]*([a-zA-Z\s]+)', summary_kor)
        if m_b: ans_B = m_b.group(1).strip()

    if ans_A == '-': ans_A = ""
    if ans_B == '-': ans_B = ""

    if is_teacher:
        processed_eng = summary_eng_raw
        if ans_A:
            processed_eng = re.sub(r'\(\s*[Aa]\s*\)\s*(?:_+|-+)?\s*',
                                   f'(A) <span style="color:#d32f2f; font-weight:800; border-bottom:1px solid #d32f2f; padding:0 4px;">{ans_A}</span> ',
                                   processed_eng)
        if ans_B:
            processed_eng = re.sub(r'\(\s*[Bb]\s*\)\s*(?:_+|-+)?\s*',
                                   f'(B) <span style="color:#d32f2f; font-weight:800; border-bottom:1px solid #d32f2f; padding:0 4px;">{ans_B}</span> ',
                                   processed_eng)

        summary_block = f"""
        <div class="summary-card">
            <div class="sum-header-row">
                <div class="card-label"><div class="icon-s">S</div>요약문 빈칸 완성 &amp; 해석</div>
                <div class="sum-sub-guide">* 정답이 채워진 요약문과 해석입니다.</div>
            </div>
            <div class="sum-content-wrapper">
                <div class="sum-box-eng" style="line-height:1.8;">{processed_eng}</div>
                <div class="sum-write-area">
                    <div class="inter-head" style="color:#d84315; margin-top: 10px;">▼ 해석 및 구문 분석 (Interpretation)</div>
                    <div style="line-height: 28px; background: repeating-linear-gradient(to bottom, transparent, transparent 27px, #cfd8dc 27px, #cfd8dc 28px); font-family: 'NanumSquareRound', sans-serif; font-size: 12.5px; color: #455a64; padding-top: 4px; border-bottom: 1px solid #cfd8dc;">
                        {summary_kor}
                    </div>
                </div>
            </div>
        </div>"""
    else:
        hint_A = ans_A[0] + "___________" if ans_A else "____________"
        hint_B = ans_B[0] + "___________" if ans_B else "____________"

        summary_eng_blank = summary_eng_raw
        summary_eng_blank = re.sub(r'\(\s*[Aa]\s*\)\s*(?:_+|-+)?\s*', f'(A) {hint_A} ', summary_eng_blank)
        summary_eng_blank = re.sub(r'\(\s*[Bb]\s*\)\s*(?:_+|-+)?\s*', f'(B) {hint_B} ', summary_eng_blank)

        summary_block = f"""
        <div class="summary-card">
            <div class="sum-header-row">
                <div class="card-label"><div class="icon-s">S</div>요약문 빈칸 완성 &amp; 해석</div>
                <div class="sum-sub-guide">* 빈칸을 채우고 해석을 쓰세요.</div>
            </div>
            <div class="sum-content-wrapper"><div class="sum-box-eng">{summary_eng_blank}</div><div class="sum-write-area"><div class="inter-head">▼ 해석 및 구문 분석 (Interpretation)</div><div class="write-line"></div><div class="write-line"></div><div class="write-line"></div><div class="write-line"></div></div></div>
        </div>"""

    return f"""
    <div class="page-container page-break">
        <div class="page-header">
            <div class="ph-left"><span class="ph-title-main">{cover_title_plain}</span><span class="ph-title-num">{CONFIG_WATERMARK_TEXT}</span><div class="unit-badge-group"><span class="ub-label">UNIT</span><span class="ub-num">{badge_text}</span></div></div>
            <div class="ph-right"><svg class="yt-icon" viewBox="0 0 24 17" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="17" rx="4" fill="#D32F2F"/><path d="M10 11.5V5.5L15 8.5L10 11.5Z" fill="white"/></svg><span>ROY'S ENGLISH</span></div>
        </div>
        <div class="p2-body">
            <div class="p2-top-wrap">
                <div class="left-col">
                    <div class="q-stem-row">
                        <div class="question-stem">{meta.get('question_header', '')}</div>
                        <div class="q-diff-badge">난이도 {stars_html} | 제한 시간: {time_limit_str}</div>
                    </div>
                    <div class="{passage_div_class}">{final_passage_html}</div>
                </div>
                <div class="right-col">
                    {secret_note_div}
                    <div class="lp-wrapper"><div class="lp-title-outside"><span class="lp-icon">🎯</span> Learning Points (핵심 콕콕)</div><div class="lp-box"><div class="lp-content-area"><div class="lp-section"><span class="lp-badge badge-logic">논리</span><ul class="lp-list">{lp_logic_html}</ul></div><div class="lp-section"><span class="lp-badge badge-grammar">구문</span><ul class="lp-list">{lp_grammar_html}</ul></div></div></div></div>
                    {final_options_div}
                </div>
            </div>
        </div>
        <div class="page-footer">- __PAGE_NUM__ -</div>
    </div>

    <div class="page-container page-break">
        <div class="page-header">
            <div class="ph-left"><span class="ph-title-main">REVIEW & WORKSHEET</span><span style="font-size:11px; color:#90a4ae; font-weight:700; margin-left:8px; font-family:'Montserrat';">[{badge_text_p3}{' (ANS)' if is_teacher else ''}]</span></div>
            <div class="ph-right"><svg class="yt-icon" viewBox="0 0 24 17" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="17" rx="4" fill="#D32F2F"/><path d="M10 11.5V5.5L15 8.5L10 11.5Z" fill="white"/></svg><span>ROY'S ENGLISH</span></div>
        </div>
        <div class="p3-body">
            <div class="p3-top">
                {summary_block}
                {vocab_block}
            </div>
            <div class="p3-bottom">
                <div class="flow-header-row">
                    <div class="flow-label"><div class="icon-f">F</div>Logic Flow (글의 흐름 구조화)</div>
                    <div class="flow-sub-guide">* 복습 후 제목과 문장 단락별 구조화 요약하세요.</div>
                </div>
                <div class="flow-container">{flow_chart_html}</div>
            </div>
        </div>
        <div class="page-footer">- __PAGE_NUM__ -</div>
    </div>
    """


def generate_review_test_page(unit_num, cumulative_vocab, is_teacher):
    if not cumulative_vocab: return ""

    unique_vocab = []
    seen = set()
    for v in cumulative_vocab:
        word = v.get('word', '').strip()
        if word and word not in seen:
            seen.add(word)
            unique_vocab.append(v)

    pool_size = len(unique_vocab)
    if pool_size == 0: return ""

    random.seed(f"review_unit_{unit_num}")

    s1_count = min(10, pool_size)
    step1_pool = random.sample(unique_vocab, s1_count)

    valid_s2_pool = [v for v in unique_vocab if is_valid_synonym(v.get('synonym', ''))]
    s2_count = min(10, len(valid_s2_pool))
    step2_pool = random.sample(valid_s2_pool, s2_count)

    s3_count = 10
    s3_candidates = [v for v in unique_vocab if v not in step1_pool]
    if len(s3_candidates) < s3_count:
        shortage = s3_count - len(s3_candidates)
        extra = [v for v in step1_pool]
        random.shuffle(extra)
        s3_candidates.extend(extra[:shortage])
    step3_pool = random.sample(s3_candidates, min(s3_count, len(s3_candidates)))

    # [STEP 1 구성]
    list_for_left = step1_pool[:len(step1_pool) // 2]
    list_for_right = step1_pool[len(step1_pool) // 2:]

    step1_left = ""
    step1_right = ""

    for i, v in enumerate(list_for_left):
        ans_word = v.get("word", "")
        raw_mean = v.get('meaning', '')
        clean_mean = re.sub(r'[①-⑳]', '|', raw_mean)
        clean_mean = re.sub(r'\(.*?\)', '', clean_mean).strip()
        final_mean = ", ".join([p.strip() for p in clean_mean.split('|') if p.strip()])
        m_style = get_shrink_style(final_mean, 22, 11)

        if is_teacher:
            step1_left += f"""<tr>
                <td class="tt-word" style="text-align:left; padding-left:10px;"><div class="td-flex-wrap"><span class="q-num">{i + 1}.</span><span class="word-text-wrap">{ans_word}</span></div></td>
                <td style="text-align:center;"><div class="tt-mean-p1" style="color:#d32f2f; {m_style}">{final_mean}</div></td>
            </tr>"""
        else:
            step1_left += f"""<tr>
                <td class="tt-word" style="text-align:left; padding-left:10px;"><div class="td-flex-wrap"><span class="q-num">{i + 1}.</span><span class="word-text-wrap">{ans_word}</span></div></td>
                <td><div class="tt-empty-box"></div></td>
            </tr>"""

    for i, v in enumerate(list_for_right):
        ans_word = v.get("word", "")
        raw_mean = v.get('meaning', '')
        clean_mean = re.sub(r'[①-⑳]', '|', raw_mean)
        clean_mean = re.sub(r'\(.*?\)', '', clean_mean).strip()
        final_mean = ", ".join([p.strip() for p in clean_mean.split('|') if p.strip()])
        m_style = get_shrink_style(final_mean, 22, 11)

        if is_teacher:
            step1_right += f"""<tr>
                <td class="tt-word" style="text-align:left; padding-left:10px;"><div class="td-flex-wrap"><span class="q-num">{i + 6}.</span><span class="word-text-wrap">{ans_word}</span></div></td>
                <td style="text-align:center;"><div class="tt-mean-p1" style="color:#d32f2f; {m_style}">{final_mean}</div></td>
            </tr>"""
        else:
            step1_right += f"""<tr>
                <td class="tt-word" style="text-align:left; padding-left:10px;"><div class="td-flex-wrap"><span class="q-num">{i + 6}.</span><span class="word-text-wrap">{ans_word}</span></div></td>
                <td><div class="tt-empty-box"></div></td>
            </tr>"""

    # [STEP 2 구성]
    group_a = step2_pool[:len(step2_pool) // 2]
    group_b = step2_pool[len(step2_pool) // 2:]

    def generate_matching_rows(group, is_teacher, num_offset):
        rows_html = ""
        svg_lines = ""
        syn_pool = []

        for i, v in enumerate(group):
            syn = v.get('synonym', '')
            clean_syn = syn.replace('/', ',').replace('(', '').replace(')', '')
            final_syn = ", ".join([s.strip() for s in clean_syn.split(',')])
            syn_pool.append({'syn': final_syn, 'id': i})

        random.shuffle(syn_pool)

        if is_teacher:
            for row_idx_left, v in enumerate(group):
                row_idx_right = next(idx for idx, s in enumerate(syn_pool) if s['id'] == row_idx_left)
                y1 = row_idx_left * 28 + 14
                y2 = row_idx_right * 28 + 14
                svg_lines += f'<line x1="5" y1="{y1}" x2="95" y2="{y2}" stroke="#e65100" stroke-width="1.5" opacity="0.6" />'

        for i, v in enumerate(group):
            shuffled_syn = syn_pool[i]['syn'] if i < len(syn_pool) else ""
            s_style = get_shrink_style(shuffled_syn, 22, 12)

            rows_html += f"""
            <tr style="height: 28px;">
                <td class="tt-word" style="text-align:left; padding-left:5px; width:38%;">
                    <div class="td-flex-wrap"><span class="q-num">{num_offset + i}.</span><span class="word-text-wrap">{v.get("word", "")}</span></div>
                </td>
                <td style="text-align:center; width:24%; position:relative;">
                    <div style="display:flex; justify-content:space-between; align-items:center; width:100%; color:#b0bec5; font-size:10px; padding:0 2px; box-sizing:border-box;">
                        <span>●</span><span>●</span>
                    </div>
                </td>
                <td class="tt-mean-p1" style="text-align:right; padding-right:5px; width:38%; {s_style}">{shuffled_syn}</td>
            </tr>"""

        box_html = f"""
        <div class="step2-box">
            <div style="position:relative; width:100%;">
                <svg style="position:absolute; left:38%; top:0; width:24%; height:100%; overflow:visible; z-index:5;" viewBox="0 0 100 {len(group) * 28}" preserveAspectRatio="none">
                    {svg_lines}
                </svg>
                <table class="step2-subtable" style="width:100%; position:relative; z-index:10;">
                    <colgroup><col width="38%"><col width="24%"><col width="38%"></colgroup>
                    <tbody>{rows_html}</tbody>
                </table>
            </div>
        </div>
        """
        return box_html

    step2_left = generate_matching_rows(group_a, is_teacher, 11)
    step2_right = generate_matching_rows(group_b, is_teacher, 11 + len(group_a))

    # [STEP 3 구성]
    step3_rows = ""
    for i, v in enumerate(step3_pool):
        chunk_raw = v.get('chunk_example', '')
        chunk_ko = v.get('chunk_translation', '')
        word_raw = v.get('word', '').split('(')[0].strip()

        clean_word = re.sub(r'\(.*?\)', '', word_raw.lower().strip()).strip()
        base = clean_word
        if len(base) > 3:
            if base.endswith('y'):
                base = base[:-1]
            elif base.endswith('e'):
                base = base[:-1]
            elif base.endswith('s'):
                base = base[:-1]

        pattern = r'\b' + re.escape(base) + r'[a-z]*'

        if is_teacher:
            try:
                chunk_step3 = re.sub(pattern, lambda m: f'<span class="chunk-hl">{m.group()}</span>', chunk_raw,
                                     flags=re.IGNORECASE)
            except:
                chunk_step3 = chunk_raw
        else:
            try:
                chunk_step3 = re.sub(pattern, '____________________', chunk_raw, flags=re.IGNORECASE)
            except:
                chunk_step3 = chunk_raw

        step3_rows += f"""<tr>
            <td class="step3-ko-text"><div class="td-flex-wrap"><span class="q-num">{21 + i}.</span><span class="word-text-wrap">{chunk_ko}</span></div></td>
            <td class="step3-chunk-text">{chunk_step3}</td>
        </tr>"""

    random.seed()

    return f"""
    <div class="page-container page-break">
        <div class="page-header">
            <div class="ph-left"><span class="ph-title-main">REVIEW TEST</span><span style="font-size:11px; color:#90a4ae; font-weight:700; margin-left:8px; font-family:'Montserrat';">[Unit {unit_num} Cumulative{' (ANS)' if is_teacher else ''}]</span></div>
            <div class="ph-right" style="font-family:'Noto Sans KR', sans-serif; font-size:13px; font-weight:700; color:#455a64; letter-spacing: 0.5px;">이름 : ____________________ &nbsp;&nbsp;&nbsp; 점수 : &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; / 30</div>
        </div>
        <div class="p2-voca-body">
            <div class="review-split">
                <div class="rev-col-left">
                    <div class="test-section-card">
                        <div class="test-sec-title"><div class="icon-v">V</div>STEP 1. Speed Check (단어 뜻 적기 - Random)</div>
                        <div class="step1-container">
                            <table class="step1-table">
                                <colgroup><col width="48%"><col width="52%"></colgroup>
                                <thead><tr><th>Word</th><th>Meaning</th></tr></thead>
                                <tbody>{step1_left}</tbody>
                            </table>
                            <table class="step1-table">
                                <colgroup><col width="48%"><col width="52%"></colgroup>
                                <thead><tr><th>Word</th><th>Meaning</th></tr></thead>
                                <tbody>{step1_right}</tbody>
                            </table>
                        </div>
                    </div>

                    <div class="test-section-card">
                        <div class="test-sec-title"><div class="icon-v">V</div>STEP 2. Match Synonyms (유의어 연결)</div>
                        <div class="step2-container">
                            {step2_left}
                            {step2_right}
                        </div>
                    </div>
                </div>

                <div class="rev-col-right">
                    <div class="test-section-card step3-card">
                        <div class="test-sec-title"><div class="icon-v">V</div>STEP 3. Chunk Context (뜻을 보고 빈칸을 채우시오)</div>
                        <div class="step3-table-container">
                            <table class="step3-table">
                                <colgroup><col width="45%"><col width="55%"></colgroup>
                                <thead><tr><th>Korean Translation</th><th>English Chunk (Fill in the blank)</th></tr></thead>
                                <tbody>{step3_rows}</tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="page-footer">- __PAGE_NUM__ -</div>
    </div>
    """


# ==============================================================================
# 수업용 화면 띄우기 (Presentation) 페이지 생성 함수
# ==============================================================================
def generate_presentation_pages(json_data_str, unit_num, badge_text, cover_title_plain):
    data = json.loads(json_data_str)
    meta = data.get('meta_info', {})
    visual = data.get('visual_data', {})

    try:
        difficulty = int(meta.get('difficulty_level', 3))
    except:
        difficulty = 3
    stars_html = "★" * difficulty + "☆" * (5 - difficulty)
    question_header = meta.get('question_header', '')

    # 발문 우측에 페이지 배지를 동적으로 생성하는 함수
    def build_q_stem(page_str=""):
        page_badge = f'<span style="background: white; color: #1976d2; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 4px; font-family: \'Montserrat\', \'NanumSquareRound\', sans-serif; border: 1px solid #bbdefb; margin-left: 4px;">{page_str}</span>' if page_str else ""
        return f'''
        <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 5px; margin-top: 0px; background: #e3f2fd; padding: 4px 10px; border-radius: 6px; border-left: 4px solid #1976d2; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <span style="font-family: 'NanumSquareRound', sans-serif; font-size: 12px; font-weight: 800; color: #0d47a1; letter-spacing: -0.3px;">{question_header}</span>
            <span style="background: white; color: #1976d2; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 4px; font-family: 'NanumSquareRound', sans-serif; border: 1px solid #bbdefb;">난이도 {stars_html}</span>__PAGE_BADGE__
        </div>
        <div style="height: 2px;"></div>
        '''

    q_stem_html_vis = build_q_stem()
    q_stem_html_vis_p1 = build_q_stem("페이지 1")
    q_stem_html_vis_p2 = build_q_stem("페이지 2")

    try:
        q_type = int(meta.get('question_type', 0))
    except:
        q_type = 0

    range_match = re.search(r'(\d+)[\-~](\d+)', question_header)
    is_long_passage = True if range_match else False

    is_insertion_prob = (q_type == 5) or ("들어갈 곳" in question_header) or ("삽입" in question_header)
    effective_q_type = q_type
    if is_long_passage or q_type == 9:
        effective_q_type = 9
    elif is_insertion_prob:
        effective_q_type = 5
    elif effective_q_type not in range(1, 10):
        effective_q_type = 1

    passage_div_class = f"passage-content type-{effective_q_type}"

    # =======================================================
    # [기능 적용] 수업용 화면 지문 형광펜 및 뜻 적용
    # =======================================================
    raw_text = visual.get('question_text_visual', '')
    raw_text = re.sub(r'《BLANK》.*?《/BLANK》', ' ____________ ', raw_text)

    # 1. 형광펜 강조 처리
    raw_text = preprocess_multiline_tags(raw_text)
    raw_text = convert_common_tags(raw_text)

    # 2. 불필요한 태그 제거 및 줄바꿈 보정
    clean_text = re.sub(r'《[^》]+》', '', raw_text)
    clean_text = clean_text.replace('\n', ' ')

    # 3. 단어 루비 문자 처리
    vocab_list_dicts = []
    for sent in data.get('sentence_analysis', []):
        ctx = sent.get('context_meaning', '')
        if ctx:
            vocab_list_dicts.extend(parse_local_vocab(ctx))
    if not vocab_list_dicts:
        vocab_list_dicts = data.get('vocab_list', [])
    clean_text = apply_vocab_style(clean_text, vocab_list_dicts)

    final_passage_html = re.sub(r'([❶-❿⓫-⓴①-⑳])', r'<span class="para-mark">\1</span>', clean_text)
    # =======================================================

    # 1. Slide 1, 2: 단어장 추출
    vocab_subset = data.get('vocab_list', [])[:10]
    vocab_part1 = vocab_subset[:5]
    vocab_part2 = vocab_subset[5:]

    def get_vocab_slide_html(v_part):
        if not v_part: return ""
        v_rows = ""
        mean_base = float(CONFIG_PRES_VOCAB_MEAN_SIZE.replace('px', ''))
        en_base = float(CONFIG_PRES_VOCAB_CHUNK_EN_SIZE.replace('px', ''))
        ko_base = float(CONFIG_PRES_VOCAB_CHUNK_KO_SIZE.replace('px', ''))

        for idx, v in enumerate(v_part):
            chunk_raw = v.get('chunk_example', '')
            chunk_en_hl = highlight_chunk_word(v.get('word', ''), chunk_raw)
            chunk_ko = v.get('chunk_translation', '')
            synonyms = v.get('synonym', '')
            if is_valid_synonym(synonyms):
                syn_parts = [s.strip() for s in synonyms.replace('/', ',').split(',') if s.strip()]
                clean_syn = ", ".join(syn_parts)
                syn_style = get_shrink_style(clean_syn, 25, 10.5)
                syn_html = f'<div class="vm-syn" style="{syn_style}">{clean_syn}</div>'
            else:
                clean_syn = ""
                syn_html = ""
            raw_mean = v.get('meaning', '')
            clean_mean = re.sub(r'[①-⑳]', '|', raw_mean)
            clean_mean = re.sub(r'\(.*?\)', '', clean_mean).strip()
            parts = [p.strip() for p in clean_mean.split('|') if p.strip()]
            final_mean = ", ".join(parts)

            mean_style = get_shrink_style(final_mean, 22, mean_base)
            c_en_style = get_shrink_style(chunk_raw, 30, en_base)
            c_ko_style = get_shrink_style(chunk_ko, 20, ko_base)

            v_rows += f"""
            <div class="v-row" style="min-height: {CONFIG_PRES_VOCAB_ROW_HEIGHT}; padding: 5px 0;">
                <div class="cell col-chk"><div class="chk-box"></div></div>
                <div class="cell col-word"><span class="word-txt" style="font-size: {CONFIG_PRES_VOCAB_WORD_SIZE};">{v.get("word", "")}</span></div>
                <div class="cell col-mean"><span class="vm-kor" style="{mean_style} margin-top: 2px;">{final_mean}</span>{syn_html}</div>
                <div class="cell col-chunk">
                    <span class="vch-en" style="{c_en_style} margin-top: 2px;">{chunk_en_hl}</span>
                    <span class="vch-ko" style="{c_ko_style} margin-top: 1px;">{chunk_ko}</span>
                </div>
            </div>
            """

        v_block = f"""
        <div class="sec-vocab">
            <div class="v-header">
                <div class="cell col-chk">Chk</div>
                <div class="cell col-word">Word</div>
                <div class="cell col-mean">Mean & Syn</div>
                <div class="cell col-chunk">Chunk Example</div>
            </div>
            <div class="v-list">{v_rows}</div>
        </div>
        """
        # 단어장 슬라이드는 배지(page str)를 포함시키지 않음
        v_stem = f'''
        <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 5px; margin-top: 0px; background: #e3f2fd; padding: 4px 10px; border-radius: 6px; border-left: 4px solid #1976d2; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <span style="font-family: 'NanumSquareRound', sans-serif; font-size: 12px; font-weight: 800; color: #0d47a1; letter-spacing: -0.3px;">{question_header}</span>
            <span style="background: white; color: #1976d2; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 4px; font-family: 'NanumSquareRound', sans-serif; border: 1px solid #bbdefb;">난이도 {stars_html}</span>
        </div>
        <div style="height: 2px;"></div>
        '''
        return f"""
        <div class="page-container page-break">
            <div class="page-header">
                <div class="ph-left"><span class="ph-title-main">{cover_title_plain}</span><span class="ph-title-num">{CONFIG_WATERMARK_TEXT}</span><div class="unit-badge-group"><span class="ub-label">UNIT</span><span class="ub-num">{badge_text}</span></div></div>
                <div class="ph-right"><svg class="yt-icon" viewBox="0 0 24 17" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="17" rx="4" fill="#D32F2F"/><path d="M10 11.5V5.5L15 8.5L10 11.5Z" fill="white"/></svg><span>ROY'S ENGLISH</span></div>
            </div>
            <div style="flex: 1; padding: {CONFIG_PRES_PADDING_TOP} 20mm 20mm 20mm; display: flex; justify-content: center; align-items: flex-start; background: #fafafa;">
                <div style="width: {CONFIG_PRES_VOCAB_WIDTH}; transform: scale(1.3); transform-origin: top center; display: flex; flex-direction: column;">
                    <div style="align-self: flex-start; margin-bottom: 5px;">
                        {v_stem}
                    </div>
                    <div style="background: white; box-shadow: 0 10px 20px rgba(0,0,0,0.05); border-radius: 8px;">
                        {v_block}
                    </div>
                </div>
            </div>
            <div class="page-footer">- __PAGE_NUM__ -</div>
        </div>
        """

    slides = []
    slide_vocab1 = get_vocab_slide_html(vocab_part1)
    if slide_vocab1: slides.append(slide_vocab1)
    slide_vocab2 = get_vocab_slide_html(vocab_part2)
    if slide_vocab2: slides.append(slide_vocab2)

    # 내용 슬라이드들을 담을 배열
    content_slides = []

    # 2. 본문 및 특수 요소 분리 추출
    text_to_split = final_passage_html
    footnotes_html = ""
    m_fn = re.search(r'(<div class="passage-footnotes">.*?</div>)', text_to_split, re.DOTALL)
    if m_fn:
        footnotes_html = m_fn.group(1)
        text_to_split = text_to_split.replace(footnotes_html, '')

    box_content_html = ""
    summary_content_html = ""
    blank_sentence_html = ""
    order_chunks = []

    if effective_q_type == 4:
        parts = re.split(r'(\([ABC]\))', text_to_split)
        if len(parts) > 1:
            box_content_html = f'<div class="box-container" style="line-height: {CONFIG_LH_PRES_BLANK_BOX};">{parts[0]}</div>'
            for i in range(1, len(parts), 2):
                order_chunks.append(
                    f'<div class="order-chunk" style="line-height: {CONFIG_LH_PRES_CHUNK};"><span class="para-mark">{parts[i]}</span>{parts[i + 1]}</div>')
            text_to_split = box_content_html + "".join(order_chunks)

    elif effective_q_type == 5:
        match = re.search(r'(<span class="para-mark">❶</span>.*?)(?=<span class="para-mark">❷</span>)', text_to_split)
        if match:
            box_content_html = f'<div class="box-container" style="line-height: {CONFIG_LH_PRES_BLANK_BOX};">{match.group(1)}</div>'
            text_to_split = text_to_split[match.end():]

    elif effective_q_type == 6:
        summary_keyword_match = re.search(r'(Summary|요약문)', text_to_split, re.IGNORECASE)
        if summary_keyword_match:
            split_idx = summary_keyword_match.start()
            main_text = text_to_split[:split_idx]
            summary_content_html = f'<div class="summary-sentence-box">{text_to_split[split_idx:]}</div>'
            text_to_split = main_text
        else:
            last_mark_match = list(re.finditer(r'<span class="para-mark">[❶-❿⓫-⓴①-⑳]</span>', text_to_split))
            if last_mark_match:
                last_idx = last_mark_match[-1].start()
                main_text = text_to_split[:last_idx]
                summary_content_html = f'<div class="summary-sentence-box">{text_to_split[last_idx:]}</div>'
                text_to_split = main_text

    elif effective_q_type == 3:
        tokens = re.split(r'(<span class="para-mark">[❶-❿⓫-⓴①-⑳]</span>)', text_to_split)
        if len(tokens) > 1:
            for i in range(1, len(tokens), 2):
                mark = tokens[i]
                txt = tokens[i + 1] if i + 1 < len(tokens) else ""
                sentence = mark + txt
                if '_' in txt or '<u>' in txt or '빈칸' in txt:
                    blank_sentence_html = sentence
                    break
        else:
            if '_' in text_to_split: blank_sentence_html = text_to_split

    unique_id = f"{unit_num}_{random.randint(10000, 99999)}"

    # 지문 분할 트릭
    markers = list(re.finditer(r'<span class="para-mark">[❶-❿⓫-⓴①-⑳]</span>', text_to_split))
    if len(markers) > 1:
        mid_idx = len(markers) // 2
        split_pos = markers[mid_idx].start()
        part1 = text_to_split[:split_pos]
        part2 = text_to_split[split_pos:]

        dangling_match = re.search(r'\(\s*$', part1)
        if dangling_match:
            move_len = len(dangling_match.group(0))
            part1 = part1[:-move_len]
            part2 = dangling_match.group(0) + part2
    else:
        part1 = text_to_split
        part2 = ""

    if footnotes_html:
        if part2:
            part2 += footnotes_html
        else:
            part1 += footnotes_html

    if part2:
        # [Slide 1 text] part1 정상 표시 + 마커(1.4em 높이) + part2 전체 회색
        slide_p1_text = f'<span style="color: inherit;">{part1}</span><span id="pres-marker-p1-{unique_id}" style="display: inline-block; width: 0; height: 1.4em; vertical-align: text-bottom;"></span><span class="fade-text">{part2}</span>'

        # [Slide 2 text] part1 전체 회색 + 마커 + part2 정상 표시
        slide_p2_text = f'<span class="fade-text">{part1}</span><span id="pres-marker-p2-{unique_id}"></span><span style="color: inherit;">{part2}</span>'
    else:
        slide_p1_text = f'<span style="color: inherit;">{part1}</span>'
        slide_p2_text = ""

    # 슬라이드 생성 공통 함수 (유동적 필기 노트 영역 포함)
    def make_pres_slide(stem_html, content_html, scale=1.5, use_student_lh=False, align_center=False, slide_idx=0,
                        show_memo=False):
        if not use_student_lh:
            if effective_q_type == 9:
                lh_style = f"font-size: {CONFIG_FONT_SIZE_PRES_TYPE_9} !important; line-height: {CONFIG_LH_PRES_TYPE_9} !important;"
            else:
                lh_style = f"font-size: {CONFIG_FONT_SIZE_PRESENTATION} !important; line-height: {CONFIG_LH_PRESENTATION} !important;"
        else:
            lh_style = ""

        align_style = f"margin-left: {CONFIG_PRES_MARGIN_LEFT}; transform-origin: top left;" if not align_center else "margin: 0 auto; transform-origin: top center;"
        justify_style = "justify-content: flex-start;" if not align_center else "justify-content: center;"

        container_id_attr = f'id="pres-container-p{slide_idx}-{unique_id}"' if slide_idx in [1, 2] else ""
        pos_style = ' position: relative;' if slide_idx in [1, 2] else ""

        script_html = ""
        if slide_idx == 1:
            script_html = f"""
            <script>
                window.addEventListener('load', function() {{
                    setTimeout(function() {{
                        var container = document.getElementById('pres-container-p1-{unique_id}');
                        var marker = document.getElementById('pres-marker-p1-{unique_id}');
                        if (marker && container) {{
                            // 마커의 Y좌표(offsetTop)와 마커의 글자 렌더링 높이(offsetHeight)를 합산하여
                            // 정확히 현재 줄(글자 아랫단)까지만 컨테이너를 한정. 다음 줄(Ascender)은 완벽히 숨김.
                            var exactBottomY = marker.offsetTop + marker.offsetHeight;
                            container.style.maxHeight = exactBottomY + 'px';
                            container.style.overflow = 'hidden';
                        }}
                    }}, 50);
                }});
            </script>
            """
        elif slide_idx == 2:
            script_html = f"""
            <script>
                window.addEventListener('load', function() {{
                    setTimeout(function() {{
                        var container = document.getElementById('pres-container-p2-{unique_id}');
                        var marker = document.getElementById('pres-marker-p2-{unique_id}');
                        if (marker && container) {{
                            var shift = marker.offsetTop;
                            container.style.marginTop = '-' + shift + 'px';
                        }}
                    }}, 50);
                }});
            </script>
            """

        # [수정] 빈 공간 필기용 노트 영역 (아이보리 배경색 적용 및 도트 패턴 제거)
        memo_html = ""
        if slide_idx in [1, 2] or show_memo:
            memo_html = f"""
            <div style="margin-top: 15px; flex: 1; display: flex; flex-direction: column; padding-bottom: 10px; min-height: 80px;">
                <div style="font-family: 'Montserrat', sans-serif; font-size: 11px; font-weight: 800; color: #90a4ae; margin-bottom: 6px; letter-spacing: 1px;"><span style="color: #cfd8dc;">+</span> ANALYSIS &amp; NOTES</div>
                <div style="flex: 1; width: 100%; border: 1.5px solid #f5eedc; border-radius: 8px; background-color: #fffdf4; box-sizing: border-box; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);"></div>
            </div>
            """

        scaled_height = round(188.5 / float(scale), 2)

        return f"""
        <div class="page-container page-break">
            <div class="page-header">
                <div class="ph-left"><span class="ph-title-main">{cover_title_plain}</span><span class="ph-title-num">{CONFIG_WATERMARK_TEXT}</span><div class="unit-badge-group"><span class="ub-label">UNIT</span><span class="ub-num">{badge_text}</span></div></div>
                <div class="ph-right"><svg class="yt-icon" viewBox="0 0 24 17" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="17" rx="4" fill="#D32F2F"/><path d="M10 11.5V5.5L15 8.5L10 11.5Z" fill="white"/></svg><span>ROY'S ENGLISH</span></div>
            </div>
            <div style="flex: 1; padding: {CONFIG_PRES_PADDING_TOP} 5mm 0mm 5mm; display: flex; {justify_style} align-items: flex-start; overflow: hidden;">
                <div style="width: 160.84mm; height: {scaled_height}mm; transform: scale({scale}); {align_style} display: flex; flex-direction: column;">
                    <div class="left-col" style="width: 100%; flex: 1; display: flex; flex-direction: column;">
                        {stem_html}
                        <div style="overflow: hidden; width: 100%; flex: 0 0 auto;">
                            <div class="{passage_div_class}" style="{lh_style}{pos_style}" {container_id_attr}>
                                {content_html}
                            </div>
                        </div>
                        {memo_html}
                    </div>
                </div>
            </div>
            <div class="page-footer">- __PAGE_NUM__ -</div>
            {script_html}
        </div>
        """

    # 유형별 슬라이드 전개 (모두 content_slides 배열에 추가)
    if effective_q_type == 3:
        if blank_sentence_html:
            blank_box_html = f'<div class="box-container" style="margin-bottom: 5px; padding: 12px 15px; font-weight: bold; line-height: {CONFIG_LH_PRES_BLANK_BOX}; font-family: \'KoPub Batang\', serif; font-size: 15.5px;">{blank_sentence_html}</div>'
            content_slides.append(make_pres_slide(q_stem_html_vis, blank_box_html, show_memo=True))

        if part2:
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p1_text, slide_idx=1))
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p2_text, slide_idx=2))
        else:
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p1_text, slide_idx=1))

    elif effective_q_type == 4:
        if box_content_html:
            content_slides.append(make_pres_slide(q_stem_html_vis, box_content_html, show_memo=True))

        for i, chunk in enumerate(order_chunks):
            content_slides.append(make_pres_slide(q_stem_html_vis, chunk, show_memo=True))

        content_slides.append(
            make_pres_slide(q_stem_html_vis, text_to_split, scale=1.0, use_student_lh=True, align_center=True))

    elif effective_q_type == 5:
        if box_content_html:
            content_slides.append(make_pres_slide(q_stem_html_vis, box_content_html, show_memo=True))

        if part2:
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p1_text, slide_idx=1))
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p2_text, slide_idx=2))
        else:
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p1_text, slide_idx=1))

    elif effective_q_type == 6:
        if summary_content_html:
            content_slides.append(make_pres_slide(q_stem_html_vis, summary_content_html, show_memo=True))

        if part2:
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p1_text, slide_idx=1))
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p2_text, slide_idx=2))
        else:
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p1_text, slide_idx=1))

    else:
        if part2:
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p1_text, slide_idx=1))
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p2_text, slide_idx=2))
        else:
            content_slides.append(make_pres_slide(q_stem_html_vis, slide_p1_text, slide_idx=1))

    # 선택지 슬라이드
    raw_options_visual = visual.get('options_visual', [])
    ans_data = data.get('answer_data', {})
    raw_main_answer = str(ans_data.get('correct_choice', meta.get('answer', data.get('answer', ''))))

    circle_map = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
    main_correct_ans_num = -1
    for c_char, c_num in circle_map.items():
        if c_char in raw_main_answer:
            main_correct_ans_num = c_num
            break
    if main_correct_ans_num == -1:
        ans_m = re.search(r'([1-5])', raw_main_answer)
        if ans_m: main_correct_ans_num = int(ans_m.group(1))

    pres_options_html = ""
    if raw_options_visual and isinstance(raw_options_visual[0], dict):
        for prob_idx, prob_obj in enumerate(raw_options_visual):
            opts = prob_obj.get("options", ["① ", "② ", "③ ", "④ ", "⑤ "])
            for idx, opt in enumerate(opts):
                if is_insertion_prob:
                    opt = re.sub(r'^\s*\(\s*([①-⑤])\s*\)', r'\1', opt)
                    opt = re.sub(r'^\s*([①-⑤])', r'( \1 )', opt)
                is_correct = ((idx + 1) == main_correct_ans_num)
                opt_style = ' style="font-size: 15px; line-height: 2.8; color: #000000;'
                if is_correct: opt_style += ' color:#d32f2f; font-weight:900;'
                opt_style += '"'
                pres_options_html += f'<div class="opt-item-wrapper" style="margin-bottom: 8px;"><span class="opt-row"{opt_style}>{opt}</span></div>'
            if prob_idx < len(raw_options_visual) - 1:
                pres_options_html += '<div style="height: 15px;"></div>'
    else:
        options = raw_options_visual if raw_options_visual else ["① ", "② ", "③ ", "④ ", "⑤ "]
        for idx, opt in enumerate(options):
            if is_insertion_prob:
                opt = re.sub(r'^\s*\(\s*([①-⑤])\s*\)', r'\1', opt)
                opt = re.sub(r'^\s*([①-⑤])', r'( \1 )', opt)
            is_correct = ((idx + 1) == main_correct_ans_num)
            opt_style = ' style="font-size: 15px; line-height: 2.8; color: #000000;'
            if is_correct: opt_style += ' color:#d32f2f; font-weight:900;'
            opt_style += '"'
            pres_options_html += f'<div class="opt-item-wrapper" style="margin-bottom: 8px;"><span class="opt-row"{opt_style}>{opt}</span></div>'

    opt_box = f'<div class="options-box" style="padding: 10px 25px;"><span class="opt-title">▼ CHOICES</span>{pres_options_html}</div>'

    opt_slide_content = ""
    if effective_q_type == 3 and blank_sentence_html:
        opt_slide_content += f'<div class="box-container" style="margin-bottom: 8px; padding: 12px 15px; font-weight: bold; line-height: {CONFIG_LH_PRES_BLANK_BOX}; font-family: \'KoPub Batang\', serif; font-size: 15.5px;">{blank_sentence_html}</div>'
    elif effective_q_type == 6 and summary_content_html:
        opt_slide_content += f'<div style="margin-bottom: 8px; font-family: \'KoPub Batang\', serif;">{summary_content_html}</div>'

    opt_slide_content += opt_box
    content_slides.append(
        make_pres_slide(q_stem_html_vis, opt_slide_content, scale=1.5, align_center=False, show_memo=True))

    # ==============================================================================
    # 마지막 슬라이드: 핵심 콕콕 단독 배치 (발문 포함하여 통일감 및 페이지 배지 생성 대응)
    # ==============================================================================
    lp_data = data.get('learning_point', {})
    logic_points = lp_data.get('logic', [])
    grammar_points = lp_data.get('grammar', [])

    def format_lp_item_slide(text):
        return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    lp_logic_html_pres = "".join([
        f"<li class='lp-item' style='font-size: 12px; line-height: 2.4; margin-bottom: 12px;'>{format_lp_item_slide(item)}</li>"
        for item in logic_points])
    lp_grammar_html_pres = "".join([
        f"<li class='lp-item' style='font-size: 12px; line-height: 2.4; margin-bottom: 12px;'>{format_lp_item_slide(item)}</li>"
        for item in grammar_points])

    slide_last = f"""
    <div class="page-container page-break">
        <div class="page-header">
            <div class="ph-left"><span class="ph-title-main">{cover_title_plain}</span><span class="ph-title-num">{CONFIG_WATERMARK_TEXT}</span><div class="unit-badge-group"><span class="ub-label">UNIT</span><span class="ub-num">{badge_text}</span></div></div>
            <div class="ph-right"><svg class="yt-icon" viewBox="0 0 24 17" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="24" height="17" rx="4" fill="#D32F2F"/><path d="M10 11.5V5.5L15 8.5L10 11.5Z" fill="white"/></svg><span>ROY'S ENGLISH</span></div>
        </div>
        <div style="flex: 1; padding: {CONFIG_PRES_PADDING_TOP} 20mm 10mm 20mm; display: flex; justify-content: flex-start; align-items: flex-start; overflow: hidden; background: linear-gradient(135deg, #ffffff 0%, #f0f4f8 100%);">
            <div style="width: 160.84mm; transform: scale(1.5); margin-left: {CONFIG_PRES_MARGIN_LEFT}; transform-origin: top left; display: flex; flex-direction: column;">

                <div class="left-col" style="width: 100%; display: flex; flex-direction: column;">
                    {q_stem_html_vis}
                    <div class="lp-wrapper" style="background: white; border-radius: 8px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); width: 100%;">
                        <div class="lp-title-outside" style="padding: 15px 15px 10px 15px; font-size: 16px;"><span class="lp-icon">🎯</span> Learning Points (핵심 콕콕)</div>
                        <div class="lp-box" style="border: none; padding: 0 15px 15px 15px;">
                            <div class="lp-content-area">
                                <div class="lp-section"><span class="lp-badge badge-logic" style="font-size: 13px; padding: 4px 10px;">논리</span><ul class="lp-list" style="padding-left: 15px; margin-top: 8px;">{lp_logic_html_pres}</ul></div>
                                <div class="lp-section" style="margin-top: 15px;"><span class="lp-badge badge-grammar" style="font-size: 13px; padding: 4px 10px;">구문</span><ul class="lp-list" style="padding-left: 15px; margin-top: 8px;">{lp_grammar_html_pres}</ul></div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
        <div class="page-footer">- __PAGE_NUM__ -</div>
    </div>
    """
    content_slides.append(slide_last)

    # [수정] 단어장 슬라이드를 제외한 나머지 전체 슬라이드 개수를 카운팅하여 배지 치환
    total_content_slides = len(content_slides)
    for i, slide_html in enumerate(content_slides):
        page_str = f"Page {i + 1}/{total_content_slides}"
        badge_html = f'<span style="background: white; color: #1976d2; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 4px; font-family: \'Montserrat\', \'NanumSquareRound\', sans-serif; border: 1px solid #bbdefb; margin-left: 4px;">{page_str}</span>'
        final_slide_html = slide_html.replace('__PAGE_BADGE__', badge_html)
        slides.append(final_slide_html)

    return "".join(slides)


def insert_page_numbers(html_str):
    parts = html_str.split('__PAGE_NUM__')
    if len(parts) <= 1:
        return html_str
    res = parts[0]
    for i, p in enumerate(parts[1:], 1):
        res += str(i) + p
    return res


if __name__ == "__main__":
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_folder = os.path.join(desktop_path, CONFIG_TARGET_FOLDER)

    final_template = WORKBOOK_TEMPLATE.replace("___CONFIG_ENG_TITLE_MAIN___", CONFIG_ENG_TITLE_MAIN)
    final_template = final_template.replace("___CONFIG_LH_TYPE_1___", CONFIG_LH_TYPE_1)
    final_template = final_template.replace("___CONFIG_LH_TYPE_2___", CONFIG_LH_TYPE_2)
    final_template = final_template.replace("___CONFIG_LH_TYPE_3___", CONFIG_LH_TYPE_3)
    final_template = final_template.replace("___CONFIG_LH_TYPE_4___", CONFIG_LH_TYPE_4)
    final_template = final_template.replace("___CONFIG_LH_TYPE_5___", CONFIG_LH_TYPE_5)
    final_template = final_template.replace("___CONFIG_LH_TYPE_6___", CONFIG_LH_TYPE_6)
    final_template = final_template.replace("___CONFIG_LH_TYPE_7___", CONFIG_LH_TYPE_7)
    final_template = final_template.replace("___CONFIG_LH_TYPE_8___", CONFIG_LH_TYPE_8)
    final_template = final_template.replace("___CONFIG_LH_TYPE_9___", CONFIG_LH_TYPE_9)
    final_template = final_template.replace("___CONFIG_LH_BOX___", CONFIG_LH_BOX)
    final_template = final_template.replace("___CONFIG_LH_CHUNK___", CONFIG_LH_CHUNK)

    student_out_path = os.path.join(target_folder, "Final_Workbook_Student.html")
    teacher_out_path = os.path.join(target_folder, "Final_Workbook_Answer.html")
    presentation_out_path = os.path.join(target_folder, "Final_Workbook_Presentation.html")

    if not os.path.exists(target_folder):
        print("=" * 60)
        print(f"⚠️ 바탕화면에 '{CONFIG_TARGET_FOLDER}' 폴더가 없습니다.")
        print(f"경로: {target_folder}")
        print("=" * 60)
    else:
        files = [f for f in os.listdir(target_folder) if f.endswith('.json')]
        try:
            files.sort(key=lambda f: int(re.sub(r'\D', '', f)))
        except:
            files.sort()

        if not files:
            print("=" * 60)
            print(f"⚠️ '{CONFIG_TARGET_FOLDER}' 폴더 안에 처리할 .json 파일이 없습니다.")
            print("=" * 60)
        else:
            print(f"📂 총 {len(files)}개의 파일을 병합합니다...")
            print("=" * 60)

            student_body = ""
            teacher_body = ""
            presentation_body = ""
            cover_html = ""

            current_unit = None
            cumulative_vocab = []

            for i, file_name in enumerate(files):
                input_path = os.path.join(target_folder, file_name)
                print(f"   processing: {file_name}...")

                try:
                    with open(input_path, 'r', encoding='utf-8') as f:
                        json_str = f.read()
                        data = json.loads(json_str)
                        meta = data.get('meta_info', {})

                        unit_match = re.search(r'(\d+)', meta.get('source_origin', ''))
                        unit_num = unit_match.group(1).zfill(2) if unit_match else "00"

                        if current_unit is not None and unit_num != current_unit:
                            if CONFIG_MAKE_STUDENT:
                                student_body += generate_review_test_page(current_unit, cumulative_vocab,
                                                                          is_teacher=False)
                            if CONFIG_MAKE_TEACHER:
                                teacher_body += generate_review_test_page(current_unit, cumulative_vocab,
                                                                          is_teacher=True)

                            cumulative_vocab = []

                            divider_html = create_unit_divider(unit_num)
                            if CONFIG_MAKE_STUDENT:
                                student_body += divider_html
                            if CONFIG_MAKE_TEACHER:
                                teacher_body += divider_html
                            if CONFIG_MAKE_PRESENTATION:
                                presentation_body += divider_html

                        elif i == 0:
                            cover_html = create_cover_page(meta)
                            divider_html = create_unit_divider(unit_num)
                            if CONFIG_MAKE_STUDENT:
                                student_body += divider_html
                            if CONFIG_MAKE_TEACHER:
                                teacher_body += divider_html
                            if CONFIG_MAKE_PRESENTATION:
                                presentation_body += divider_html

                        cumulative_vocab.extend(data.get('vocab_list', [])[:10])
                        current_unit = unit_num

                        if CONFIG_MAKE_STUDENT:
                            student_body += generate_unit_pages(json_str, is_teacher=False)
                        if CONFIG_MAKE_TEACHER:
                            teacher_body += generate_unit_pages(json_str, is_teacher=True)
                        if CONFIG_MAKE_PRESENTATION:
                            presentation_body += generate_presentation_pages(json_str, unit_num,
                                                                             f"{unit_num} - {re.search(r'(\d+)', meta.get('question_header', '')).group(1).zfill(2) if re.search(r'(\d+)', meta.get('question_header', '')) else '00'}",
                                                                             CONFIG_HEADER_TITLE)

                except Exception as e:
                    print(f"   ❌ Error reading {file_name}: {e}")

            if cumulative_vocab:
                if CONFIG_MAKE_STUDENT:
                    student_body += generate_review_test_page(current_unit, cumulative_vocab, is_teacher=False)
                if CONFIG_MAKE_TEACHER:
                    teacher_body += generate_review_test_page(current_unit, cumulative_vocab, is_teacher=True)

            back_cover_html = create_back_cover_page()

            if CONFIG_MAKE_STUDENT:
                student_body += back_cover_html
                student_body = insert_page_numbers(student_body)
                full_html_student = final_template + cover_html + student_body + "</body></html>"
                with open(student_out_path, 'w', encoding='utf-8') as f:
                    f.write(full_html_student)
                print(f"   [PDF 변환 중...] 학생용 PDF 생성 중...")
                save_html_to_pdf(full_html_student, student_out_path.replace('.html', '.pdf'))

            if CONFIG_MAKE_TEACHER:
                teacher_body += back_cover_html
                teacher_body = insert_page_numbers(teacher_body)
                full_html_teacher = final_template + cover_html + teacher_body + "</body></html>"
                with open(teacher_out_path, 'w', encoding='utf-8') as f:
                    f.write(full_html_teacher)
                print(f"   [PDF 변환 중...] 교사용 PDF 생성 중...")
                save_html_to_pdf(full_html_teacher, teacher_out_path.replace('.html', '.pdf'))

            if CONFIG_MAKE_PRESENTATION:
                presentation_body += back_cover_html
                presentation_body = insert_page_numbers(presentation_body)
                full_html_presentation = final_template + cover_html + presentation_body + "</body></html>"
                with open(presentation_out_path, 'w', encoding='utf-8') as f:
                    f.write(full_html_presentation)
                print(f"   [PDF 변환 중...] 수업용 PDF 생성 중...")
                save_html_to_pdf(full_html_presentation, presentation_out_path.replace('.html', '.pdf'))

            print("=" * 60)
            print(f"🎉 HTML 및 PDF 생성 완료!")
            if CONFIG_MAKE_STUDENT:
                print(f"   📘 학생용: {os.path.basename(student_out_path)} (.pdf 포함)")
            if CONFIG_MAKE_TEACHER:
                print(f"   📕 교사용: {os.path.basename(teacher_out_path)} (.pdf 포함)")
            if CONFIG_MAKE_PRESENTATION:
                print(f"   🖥️ 수업용: {os.path.basename(presentation_out_path)} (.pdf 포함)")