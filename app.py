import streamlit as st
import json
import re
import os
import subprocess
import tempfile
import zipfile
import io
import datetime
import base64

# ==========================================
# Playwright 브라우저 자동 설치 (클라우드 배포 대응)
# ==========================================
@st.cache_resource
def install_playwright_browser():
    subprocess.run(
        ["python", "-m", "playwright", "install", "--with-deps", "chromium"],
        check=True
    )

install_playwright_browser()

import mock_exam_engine as engine

# ==========================================
# 페이지 설정
# ==========================================
st.set_page_config(
    page_title="Roy's 모의고사 교재 만들기",
    page_icon="📕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 900; color: #003b6f; margin-bottom: 0; letter-spacing: -1px; }
    .sub-title { font-size: 1rem; color: #78909c; font-weight: 500; margin-top: -10px; margin-bottom: 30px; }
    .log-box { background: #263238; color: #b0bec5; font-family: 'Courier New', monospace; font-size: 13px;
               padding: 15px; border-radius: 8px; max-height: 300px; overflow-y: auto; line-height: 1.6; }
    .log-ok { color: #66bb6a; } .log-err { color: #ef5350; } .log-warn { color: #ffa726; } .log-info { color: #42a5f5; }
    .log-time { color: #78909c; }
    .stDownloadButton > button { width: 100%; font-weight: 700; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 로그 시스템
# ==========================================
def init_log():
    if 'log_messages' not in st.session_state:
        st.session_state['log_messages'] = []

def log(msg, level="info"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    icon = {"ok": "✅", "err": "❌", "warn": "⚠️", "info": "📋"}.get(level, "📋")
    css = {"ok": "log-ok", "err": "log-err", "warn": "log-warn", "info": "log-info"}.get(level, "log-info")
    st.session_state['log_messages'].append(
        f'<span class="log-time">[{now}]</span> {icon} <span class="{css}">{msg}</span>'
    )

def render_log():
    if st.session_state.get('log_messages'):
        lines = "<br>".join(st.session_state['log_messages'])
        st.markdown(f'<div class="log-box">{lines}</div>', unsafe_allow_html=True)


def auto_download(data_bytes, file_name, mime_type):
    b64 = base64.b64encode(data_bytes).decode()
    html = f'''
    <html><body>
    <script>
        var a = document.createElement("a");
        a.href = "data:{mime_type};base64,{b64}";
        a.download = "{file_name}";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    </script>
    </body></html>
    '''
    st.components.v1.html(html, height=0, width=0)


# ==========================================
# 빌드 + PDF 생성
# ==========================================
def build_and_generate_pdf(uploaded_files, config, gen_student, gen_teacher, gen_presentation):
    init_log()
    st.session_state['log_messages'] = []
    log("모의고사 교재 생성을 시작합니다.", "info")

    # 엔진 설정 반영
    engine.CONFIG_ACADEMY_NAME = config["academy_name"]
    engine.CONFIG_SERIES_TAG = config["series_tag"]
    engine.CONFIG_SUB_TITLE = config["sub_title"]
    engine.CONFIG_COPYRIGHT = config["copyright"]
    engine.CONFIG_WATERMARK_TEXT = config["watermark"]
    engine.CONFIG_HEADER_TITLE = config["header_title"]
    engine.CONFIG_COVER_TITLE_HTML = config["cover_title_html"]
    engine.CONFIG_ENG_TITLE_MAIN = config["eng_title_main"]
    engine.CONFIG_ENG_TITLE_SUB = config["eng_title_sub"]

    # 파일 정렬
    file_entries = []
    for uf in uploaded_files:
        file_entries.append({'name': uf.name, 'content': uf.getvalue().decode('utf-8')})

    try:
        file_entries.sort(key=lambda x: int(re.sub(r'\D', '', x['name']) or '0'))
    except (ValueError, TypeError):
        file_entries.sort(key=lambda x: x['name'])

    st.session_state['first_file_name'] = file_entries[0]['name'].replace('.json', '')
    log(f"{len(file_entries)}개 JSON 파일 로드 완료", "ok")

    # HTML 템플릿 준비
    final_template = engine.WORKBOOK_TEMPLATE.replace("___CONFIG_ENG_TITLE_MAIN___", engine.CONFIG_ENG_TITLE_MAIN)
    for i in range(1, 10):
        final_template = final_template.replace(f"___CONFIG_LH_TYPE_{i}___", getattr(engine, f"CONFIG_LH_TYPE_{i}"))
    final_template = final_template.replace("___CONFIG_LH_BOX___", engine.CONFIG_LH_BOX)
    final_template = final_template.replace("___CONFIG_LH_CHUNK___", engine.CONFIG_LH_CHUNK)

    student_body = ""
    teacher_body = ""
    presentation_body = ""
    cover_html = ""
    current_unit = None
    cumulative_vocab = []
    errors = []

    progress_bar = st.progress(0, text="HTML 생성 중...")

    for i, entry in enumerate(file_entries):
        progress_bar.progress((i + 1) / len(file_entries) * 0.5, text=f"HTML 생성 중: {entry['name']}")

        try:
            data = json.loads(entry['content'])
            meta = data.get('meta_info', {})

            unit_match = re.search(r'(\d+)', meta.get('source_origin', ''))
            unit_num = unit_match.group(1).zfill(2) if unit_match else "00"

            q_header = meta.get('question_header', '')
            range_match = re.search(r'(\d+)[\-~](\d+)', q_header)
            if range_match:
                q_num = f"{range_match.group(1)},{range_match.group(2)}"
            else:
                q_num_match = re.search(r'(\d+)', q_header)
                q_num = q_num_match.group(1).zfill(2) if q_num_match else "00"

            badge_text = f"{unit_num} - {q_num}"

            if current_unit is not None and unit_num != current_unit:
                if gen_student:
                    student_body += engine.generate_review_test_page(current_unit, cumulative_vocab, is_teacher=False)
                if gen_teacher:
                    teacher_body += engine.generate_review_test_page(current_unit, cumulative_vocab, is_teacher=True)
                cumulative_vocab = []

                divider = engine.create_unit_divider(unit_num)
                if gen_student: student_body += divider
                if gen_teacher: teacher_body += divider
                if gen_presentation: presentation_body += divider

            elif i == 0:
                cover_html = engine.create_cover_page(meta)
                divider = engine.create_unit_divider(unit_num)
                if gen_student: student_body += divider
                if gen_teacher: teacher_body += divider
                if gen_presentation: presentation_body += divider

            cumulative_vocab.extend(data.get('vocab_list', [])[:10])
            current_unit = unit_num

            if gen_student:
                student_body += engine.generate_unit_pages(entry['content'], is_teacher=False)
            if gen_teacher:
                teacher_body += engine.generate_unit_pages(entry['content'], is_teacher=True)
            if gen_presentation:
                presentation_body += engine.generate_presentation_pages(
                    entry['content'], unit_num, badge_text, engine.CONFIG_HEADER_TITLE)

            log(f"  {entry['name']} 처리 완료", "ok")
        except Exception as e:
            errors.append(f"{entry['name']}: {str(e)}")
            log(f"  {entry['name']} 오류: {str(e)}", "err")

    # 마지막 유닛 Review Test
    if cumulative_vocab:
        if gen_student:
            student_body += engine.generate_review_test_page(current_unit, cumulative_vocab, is_teacher=False)
        if gen_teacher:
            teacher_body += engine.generate_review_test_page(current_unit, cumulative_vocab, is_teacher=True)

    back_cover = engine.create_back_cover_page()

    log("HTML 생성 완료. PDF 변환을 시작합니다.", "info")

    # PDF 변환
    first_name = st.session_state.get('first_file_name', 'MockExam')
    pdf_tasks = []

    if gen_student:
        student_body += back_cover
        student_body = engine.insert_page_numbers(student_body)
        full_html = final_template + cover_html + student_body + "</body></html>"
        pdf_tasks.append((full_html, f'{first_name}(학생용).pdf', '학생용'))

    if gen_teacher:
        teacher_body += back_cover
        teacher_body = engine.insert_page_numbers(teacher_body)
        full_html = final_template + cover_html + teacher_body + "</body></html>"
        pdf_tasks.append((full_html, f'{first_name}(교사용).pdf', '교사용'))

    if gen_presentation:
        presentation_body += back_cover
        presentation_body = engine.insert_page_numbers(presentation_body)
        full_html = final_template + cover_html + presentation_body + "</body></html>"
        pdf_tasks.append((full_html, f'{first_name}(수업용).pdf', '수업용'))

    pdf_files = {}
    total_tasks = len(pdf_tasks)

    for idx, (html_content, fname, label) in enumerate(pdf_tasks):
        progress_bar.progress(0.5 + (idx + 1) / total_tasks * 0.5, text=f"PDF 변환 중: {label}...")
        log(f"  PDF 변환 중: {label}...", "info")

        try:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                tmp_path = tmp.name
            engine.save_html_to_pdf(html_content, tmp_path)
            with open(tmp_path, 'rb') as f:
                pdf_files[fname] = f.read()
            os.unlink(tmp_path)
            log(f"  {label} PDF 변환 완료", "ok")
        except Exception as e:
            log(f"  {label} PDF 변환 실패: {str(e)}", "err")
            errors.append(f"PDF 변환 실패 ({label}): {str(e)}")

    progress_bar.progress(1.0, text="완료!")

    total_msg = f"총 {len(pdf_files)}개 PDF 생성 완료"
    if errors:
        total_msg += f" ({len(errors)}개 오류 발생)"
        log(total_msg, "warn")
    else:
        log(total_msg, "ok")

    return pdf_files, errors


def create_zip(file_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for name, data in file_dict.items():
            if isinstance(data, str):
                data = data.encode('utf-8')
            zf.writestr(name, data)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# ==========================================
# 사이드바
# ==========================================
with st.sidebar:
    st.markdown("## 설정")

    st.markdown("#### 표지 텍스트")
    academy_name = st.text_input("학원명", value="With ROY")
    series_tag = st.text_input("시리즈 태그", value="2026 Curriculum")
    sub_title = st.text_input("부제목", value="빈순삽합 실전편 1-8회")
    header_title = st.text_input("헤더 타이틀", value="빈순삽합 실전")
    cover_title = st.text_input("메인 타이틀 (HTML)", value='특목고 대비 <span class="highlight">READING - Part 1</span>')
    eng_main = st.text_input("영어 타이틀 (메인)", value="SG")
    eng_sub = st.text_input("영어 타이틀 (서브)", value="어학원")
    copyright_text = st.text_input("저작권", value="© CEDU 빈순삽합 실전편 구매한 학생들에게만 배부되는 수업용 자료입니다.")

    st.markdown("---")
    st.markdown("#### 출력 옵션")
    watermark = st.text_input("워터마크", value="Super")
    gen_student = st.checkbox("학생용", value=False)
    gen_teacher = st.checkbox("교사용", value=False)
    gen_presentation = st.checkbox("수업용 (Presentation)", value=True)

    st.markdown("---")
    st.markdown("<div style='color:#90a4ae; font-size:12px; text-align:center;'>Roy's Mock Exam Workbook Generator v1.0</div>", unsafe_allow_html=True)


# ==========================================
# 메인 영역
# ==========================================
st.markdown('<div class="main-title">Roy\'s 모의고사 교재 만들기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">JSON 파일을 업로드하면 학생용/교사용/수업용 PDF 교재를 자동 생성합니다.</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "JSON 파일을 드래그하여 업로드하세요 (복수 선택 가능)",
    type=['json'],
    accept_multiple_files=True,
    help="모의고사 분석 JSON 파일을 여기에 올리면 됩니다."
)

if uploaded_files:
    st.markdown(f"**{len(uploaded_files)}개 파일 업로드됨**")

    with st.expander("업로드된 파일 목록", expanded=False):
        for uf in sorted(uploaded_files, key=lambda x: x.name):
            size_kb = len(uf.getvalue()) / 1024
            st.markdown(f"- `{uf.name}` ({size_kb:.1f} KB)")

    if st.button("PDF 교재 생성하기", type="primary", use_container_width=True):
        if not gen_student and not gen_teacher and not gen_presentation:
            st.error("최소 하나의 출력 옵션을 선택하세요.")
        else:
            config = {
                "academy_name": academy_name,
                "series_tag": series_tag,
                "sub_title": sub_title,
                "copyright": copyright_text,
                "watermark": watermark,
                "header_title": header_title,
                "cover_title_html": cover_title,
                "eng_title_main": eng_main,
                "eng_title_sub": eng_sub,
            }

            pdf_files, errors = build_and_generate_pdf(
                uploaded_files, config, gen_student, gen_teacher, gen_presentation
            )

            if pdf_files:
                st.session_state['pdf_files'] = pdf_files
                st.session_state['generation_done'] = True

                # 수업용 자동 다운로드
                pres_files = {k: v for k, v in pdf_files.items() if '수업용' in k}
                if pres_files:
                    fname = list(pres_files.keys())[0]
                    auto_download(pres_files[fname], fname, "application/pdf")

    # 로그 표시
    init_log()
    if st.session_state.get('log_messages'):
        st.markdown("#### 처리 로그")
        render_log()

    # PDF 다운로드 버튼
    if st.session_state.get('generation_done') and st.session_state.get('pdf_files'):
        pdf_files = st.session_state['pdf_files']

        st.markdown("---")
        st.markdown("### PDF 다운로드")

        for name, data in pdf_files.items():
            st.download_button(
                f"{name}",
                data=data,
                file_name=name,
                mime="application/pdf",
                use_container_width=True,
                key=f"dl_{name}"
            )

        if len(pdf_files) > 1:
            st.markdown("---")
            zip_data = create_zip(pdf_files)
            first_name = st.session_state.get('first_file_name', 'MockExam')
            st.download_button(
                "전체 PDF ZIP 다운로드",
                data=zip_data,
                file_name=first_name + ".zip",
                mime="application/zip",
                use_container_width=True,
                key="dl_zip"
            )

else:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 1. 설정\n왼쪽 사이드바에서\n표지, 출력 옵션을 조정하세요.")
    with col2:
        st.markdown("#### 2. 업로드\n모의고사 분석 JSON 파일을\n드래그 앤 드롭하세요.")
    with col3:
        st.markdown("#### 3. 다운로드\n'PDF 교재 생성하기'를 누르면\nPDF를 바로 다운로드합니다.")
