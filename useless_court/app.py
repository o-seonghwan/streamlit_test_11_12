"""쓸데없는 재판소 — 재판 진행부터 판례 저장까지 실행하는 앱."""
import streamlit as st
import pandas as pd

from core.trial import REBUTTALS, case_rebuttals, available_evidence, new_trial, respond, submit_evidence
from core.jury import judge
from core.verdict import make_verdict
from core.storage import history, save_case
from core.cases import load_cases, filter_cases, GROUPS

st.set_page_config(page_title="쓸데없는 재판소", page_icon="⚖️", layout="wide")

# 사건 목록은 JSON에서 읽어 분야별로 표시한다.
ALL_CASES = load_cases()
CASES = {row['name']: row for row in ALL_CASES}
CATEGORIES = ["음식 분쟁", "생활 분쟁", "소통 분쟁", "기타 분쟁"]
PAGES = ["홈", "사건 접수", "재판 진행", "판결문", "판례 보관소"]

# Streamlit 재실행 시에도 진행 상황을 보존한다.
for key, value in {"nav": "홈", "trial": None, "current_case": None, "lawyer_side": "원고 측", "result": None, "document": None, "saved_id": None}.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown("""<style>
/* 전체 테마: 장난감 법정 + 도장 찍는 관공서 */
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Gaegu:wght@400;700&display=swap');
:root {--ink:#322819;--paper:#fffaf0;--sun:#ffe6a2;--coral:#ff856a;--sky:#9ed8ed;--teal:#237f80;--edge:#453320}
.stApp {background:repeating-linear-gradient(0deg,#fff8e8 0px,#fff8e8 31px,#f1e4ca 32px,#fff8e8 33px);color:var(--ink)}
.block-container {max-width:1130px;padding-top:3.2rem!important;padding-bottom:3rem}
html,body,[data-testid="stAppViewContainer"],button,input,textarea,[role="radiogroup"] {font-family:'Jua',sans-serif}
[data-testid="stSidebar"] {background:#ffe5bb!important;border-right:4px dashed #a56b43}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {padding-top:1.6rem}
[data-testid="stSidebar"] [data-testid="stRadio"] label {border:0!important}
[data-testid="stSidebar"] [role="radiogroup"] > label {border:2px solid #744f33!important;border-radius:13px;background:#fffaf0!important;margin:.23rem 0;padding:.44rem .65rem;box-shadow:2px 3px 0 #b78b68}
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {background:#ffdf72!important;box-shadow:2px 3px 0 #774526}
[data-testid="stSidebar"] [role="radiogroup"] > label p {color:#312416!important}
.stApp h1,.stApp h2,.stApp h3 {font-family:'Jua',sans-serif!important;color:#53311f!important;letter-spacing:.3px}
.stApp h1 {font-size:2.25rem!important}
.stApp h2 {font-size:1.6rem!important}
.stApp h3 {font-size:1.28rem!important}
.stApp [data-testid="stMarkdownContainer"] p,.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stWidgetLabel"] p,.stApp [data-testid="stMetricLabel"] p,
.stApp [data-testid="stMetricValue"],.stApp [data-testid="stCaptionContainer"] p,
.stApp label,.stApp label p {color:#332719!important;opacity:1!important}
.stApp input,.stApp textarea,.stApp [role="combobox"] {color:#2c2119!important;caret-color:#2c2119!important}
.stApp input::placeholder,.stApp textarea::placeholder {color:#82705f!important;opacity:1!important}
.stApp [data-testid="stTextInput"] input,.stApp [data-testid="stTextArea"] textarea {background:#fffdfa!important;border:2px solid #a48765!important;border-radius:12px!important}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"]>div {background:#fffdfa!important;border:2px solid #a48765!important;border-radius:12px!important}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] * {color:#34271e!important}
.stApp [data-testid="stRadio"] [role="radiogroup"] {gap:.55rem}
.stApp [data-testid="stRadio"] [role="radiogroup"] > label {background:#fffdf7;border:1px solid #c1a98a;padding:.42rem .68rem;border-radius:12px}
.stApp [data-testid="stForm"] {background:#fff4d9!important;border:2px dashed #ba8c56!important;border-radius:18px;padding:1.1rem}
.stApp [data-testid="stMetric"] {background:#fffef9;border:2px solid #65452f;border-radius:16px;padding:.75rem 1rem;box-shadow:4px 4px 0 #dfbc8f}
.stApp [data-testid="stMetricValue"] {color:#ad4d32!important;font-family:'Jua',sans-serif}
.stApp .stButton button,.stApp .stDownloadButton button,.stApp [data-testid="stFormSubmitButton"] button {background:#fff0b9!important;color:#332719!important;border:2px solid #60412b!important;border-radius:12px!important;box-shadow:3px 4px 0 #9b7456!important;font-weight:700!important;transition:transform .12s,box-shadow .12s}
.stApp .stButton button:hover,.stApp .stDownloadButton button:hover,.stApp [data-testid="stFormSubmitButton"] button:hover {transform:translateY(2px);box-shadow:1px 2px 0 #9b7456!important;background:#ffdc83!important}
.stApp button[kind="primary"],.stApp [data-testid="stFormSubmitButton"] button[kind="primary"] {background:#ff9074!important;color:#32251f!important}
.stApp [data-testid="stAlert"] {border:2px solid #947453;border-radius:15px!important;box-shadow:2px 3px 0 #d2b58f}
.stApp [data-testid="stExpander"] {background:#fffdf8;border:2px solid #d6b891;border-radius:13px}
.stApp [data-testid="stProgressBar"] > div > div {background:#ff936e!important}
.stApp hr {border-color:#c6a07a!important;border-width:2px;border-style:dashed}
.stApp [data-testid="stDataFrame"] {border:2px solid #b68f65;border-radius:12px;overflow:hidden}
.stApp [data-testid="stTextArea"] textarea {line-height:1.6}
.court-banner {position:relative;overflow:visible;background:linear-gradient(135deg,#ffe8a5 0%,#ffbd9b 58%,#ffc7ad 100%);border:4px solid #493320;border-radius:20px;padding:36px 155px 28px 28px;margin:22px 12px 30px 8px;box-shadow:4px 5px 0 #9e7659;transform:none;box-sizing:border-box}
.court-banner h1 {font-size:2.5rem!important;line-height:1.5!important;padding:0.18em 0 0.12em!important;margin:0 0 8px!important;color:#4a2d20!important;overflow:visible!important}
.court-banner p {margin:0;color:#573c27!important;font-size:1.05rem}
.court-banner:after {pointer-events:none;content:'⚖️';position:absolute;right:30px;top:17px;font-size:6.4rem;transform:rotate(15deg);filter:drop-shadow(3px 4px 0 #fff9)}
.court-stamp {display:inline-block;border:4px double #a63d36;color:#a63d36;background:#fff7dd;padding:6px 16px;border-radius:7px;font-size:1.05rem;font-weight:900;letter-spacing:2px;transform:rotate(-5deg);margin:8px 0 14px}
.court-ticket {background:#fffcf3;border:3px dashed #b58c5f;border-radius:16px;padding:14px 17px;margin:10px 0 22px;box-shadow:3px 4px 0 #e3c69d}
.court-ticket-title {font-family:'Jua',sans-serif;color:#4e3420;font-size:1.35rem}
.court-ticket-sub {color:#6e5842;font-size:.95rem;margin-top:5px}
.court-tape {display:inline-block;background:#ffdf77;border:2px solid #7c5838;color:#4b3525;border-radius:7px;padding:4px 13px;margin:8px 0;transform:rotate(-2deg);font-weight:700}
.court-paper {background:#fffdfa;border:3px solid #6e4b31;border-radius:14px;padding:17px 18px;box-shadow:4px 5px 0 #e0ba91;margin:8px 0 17px}
.court-persona {font-size:2rem;line-height:1.4}
@media(max-width:700px){.block-container{padding-top:3rem!important}.court-banner{padding:30px 18px 75px;margin-top:20px}.court-banner h1{font-size:1.7rem!important;line-height:1.5!important}.court-banner:after{font-size:3.5rem;right:18px;top:auto;bottom:2px}}
</style>""", unsafe_allow_html=True)

# 페이지 이동 요청은 메뉴 위젯이 생성되기 전에 적용한다.
if 'pending_page' in st.session_state:
    st.session_state.nav = st.session_state.pop('pending_page')

with st.sidebar:
    st.markdown('### 🏛️ 황당무계 법원')
    st.markdown('<span class="court-stamp">쓸데없음 공식 인증</span>', unsafe_allow_html=True)
    st.caption('제0법정 · 논리보다 진지함이 우선!')
    page = st.radio('메뉴', PAGES, key='nav')
    st.divider()
    if st.session_state.current_case:
        st.success(f"접수 사건: {st.session_state.current_case['name']}")
    else:
        st.info('사건을 먼저 접수해 주세요.')
    st.markdown('---')
    st.caption('📎 본 법원은 진짜 법원이 아닙니다. 판결은 오락용입니다.')


def go(page_name):
    # 위젯이 생성된 뒤에는 nav를 직접 수정할 수 없다.
    st.session_state.pending_page = page_name
    st.rerun()


def case_details(case):
    st.markdown('<div class="court-tape">📌 사건 파일 · '+ __import__('html').escape(case['category']) +'</div>', unsafe_allow_html=True)
    st.subheader(case['name'])
    st.write(case['description'])
    if case.get('research_note'):
        st.caption('📎 ' + case['research_note'])
    left, right = st.columns(2)
    plaintiff = case.get('positions', {}).get('plaintiff', {})
    defendant = case.get('positions', {}).get('defendant', {})
    with left:
        st.info('**🔵 원고 측 · ' + case['plaintiff'] + '**')
        if plaintiff:
            st.write('**주장:** ' + plaintiff['summary'])
    with right:
        st.warning('**🟠 피고 측 · ' + case['defendant'] + '**')
        if defendant:
            st.write('**반론:** ' + defendant['summary'])


if page == '홈':
    st.markdown('<div class="court-banner"><h1>🏛️ 쓸데없는 재판소</h1><p>세상에서 가장 사소한 문제를 가장 진지하게 판결합니다.<br>재판장: 오늘도 별것 아닌 일로 출근했습니다.</p></div>', unsafe_allow_html=True)
    st.write('황당한 사건을 접수하고 변호사가 되어 증거와 변론으로 배심원을 설득해 보세요!')
    a, b, c = st.columns(3)
    a.metric('기본 사건', len(CASES))
    b.metric('가상 배심원', '3명')
    completed = history()
    c.metric('종결된 사건', f'{len(completed)}건')
    st.markdown('<div class="court-ticket"><div class="court-ticket-title">📢 오늘의 법원 공지</div><div class="court-ticket-sub">증거는 진지하게, 형벌은 엉뚱하게! 감자 배심원이 여러분을 기다립니다.</div></div>', unsafe_allow_html=True)
    st.subheader('오늘의 추천 사건')
    st.info('총 12개 분야에서 155개 사건을 골라 재판해 보세요. 분야별 선택과 검색이 가능합니다.')
    if st.button('사건 접수하러 가기', type='primary'):
        go('사건 접수')

elif page == '사건 접수':
    st.title('📝 사건 접수처')
    st.markdown('<span class="court-stamp">접수 대기 중</span>', unsafe_allow_html=True)
    st.caption('사건을 고르면 양측 주장부터 훑어보세요. 사건 목록은 분야별로 분리되어 있습니다.')
    mode = st.radio('접수 방식', ['기본 사건 선택', '직접 작성'], horizontal=True)
    if mode == '기본 사건 선택':
        left, right = st.columns([1, 2])
        group = left.selectbox('🗂️ 사건 분야 (12개)', ['전체'] + GROUPS, key='case_group')
        keyword = right.text_input('🔎 사건 검색', placeholder='예: 치킨, 알람, 월요일', key='case_keyword')
        matches = filter_cases(ALL_CASES, group, keyword)
        st.caption(f'검색 결과 {len(matches)}건 / 전체 {len(ALL_CASES)}건')
        st.caption('분야를 고르면 해당 분야 사건만 표시됩니다. 검색어로 다시 좁힐 수 있습니다.')
        if matches:
            selected_case = st.selectbox('📂 사건 파일 꺼내기', matches, format_func=lambda c: c['name'], key='selected_case')
            st.info(f"**재판 쟁점:** {selected_case['description']}")
            case_details(selected_case)
            if selected_case.get('positions'):
                positions = selected_case['positions']
                with st.expander('양측의 목표와 약점 비교'):
                    a, b = st.columns(2)
                    for col, name, key in ((a, '원고', 'plaintiff'), (b, '피고', 'defendant')):
                        data = positions[key]
                        with col:
                            st.write(f'**{name} 측 승리 목표:** {data["goal"]}')
                            st.caption(data['weakness'])
            if selected_case.get('debate'):
                st.caption('가상·철학 논쟁: 여기서의 판결은 과학적 사실 확정이 아닌 게임 결과입니다.')
            name = selected_case['name']
            category = selected_case['category']
            description = selected_case['description']
            plaintiff = selected_case['plaintiff']
            defendant = selected_case['defendant']
        else:
            selected_case = None
            st.warning('검색 결과가 없습니다. 다른 분야나 검색어를 선택해 주세요.')
    else:
        selected_case = None
    st.markdown('### 🎭 어느 편에 설까요?')
    st.caption('원고는 주장을 인정받으려 하고, 피고는 그 주장에 이의를 제기합니다.')
    side = st.radio('변호인석 선택', ['원고 측', '피고 측'], horizontal=True)
    if mode == '기본 사건 선택' and selected_case:
        position_key = 'plaintiff' if side == '원고 측' else 'defendant'
        position = selected_case.get('positions', {}).get(position_key)
        if position:
            st.info('**선택한 편의 목표:** ' + position['goal'])
    with st.form('case_form'):
        if mode == '직접 작성':
            name = st.text_input('사건명', placeholder='예: 마지막 붕어빵 꼬리 절도 사건', max_chars=100)
            category = st.selectbox('사건 유형', CATEGORIES)
            description = st.text_area('사건 내용', max_chars=1000)
            plaintiff = st.text_input('원고', max_chars=100)
            defendant = st.text_input('피고', max_chars=100)
        submitted = st.form_submit_button('사건 접수하기', type='primary', use_container_width=True)
    if submitted:
        if mode == '기본 사건 선택' and selected_case is None:
            st.error('먼저 사건을 선택해 주세요.')
        elif any(not field.strip() for field in [name, description, plaintiff, defendant]):
            st.error('모든 사건 정보를 입력해 주세요.')
        else:
            case = dict(name=name.strip(), category=category, description=description.strip(),
                        plaintiff=plaintiff.strip(), defendant=defendant.strip())
            if selected_case is not None:
                # 사건별 입장·증거·변론 데이터까지 함께 전달한다.
                case = dict(selected_case)
            st.session_state.current_case = case
            st.session_state.lawyer_side = side
            st.session_state.trial = new_trial(case, side)
            st.session_state.result = None
            st.session_state.document = None
            st.session_state.saved_id = None
            st.success('새 사건이 접수되었습니다.')
    if st.session_state.current_case:
        st.divider()
        case_details(st.session_state.current_case)
        st.write('**담당 변호사:**', st.session_state.lawyer_side)
        if st.button('재판 시작하기'):
            go('재판 진행')

elif page == '재판 진행':
    st.title('⚖️ 제0법정 · 오늘도 개정!')
    st.markdown('<div class="court-tape">🔔 질서! 모두 진지한 표정을 지어주세요.</div>', unsafe_allow_html=True)
    trial = st.session_state.trial
    if not trial:
        st.warning('먼저 사건을 접수해야 합니다.')
        if st.button('사건 접수하기'):
            go('사건 접수')
    else:
        case_details(trial['case'])
        st.write(f"**내 역할:** {trial['side']} 변호사")
        stages = {'evidence': ('증거 제출', .15), 'rebuttal': ('변론 진행', .4 + trial['turn'] * .25), 'ready_for_jury': ('배심원 심사', .9), 'judged': ('판결 완료', 1.)}
        stage_name, progress = stages[trial['stage']]
        st.progress(progress, text=f'현재 단계: {stage_name}')
        if trial['stage'] == 'evidence':
            st.subheader('📁 증거 제출 (1~3개, 후보 8개)')
            st.caption('제출할 증거를 최대 3개 선택하세요. 실제 사실을 입증하는 자료가 아니라 게임상의 가상 증거입니다.')
            with st.form('evidence_form'):
                selected, notes = [], {}
                for evidence in available_evidence(trial['case']):
                    # 자료의 유불리는 화면에 미리 공개하지 않는다.
                    if st.checkbox(f"{evidence['name']} — {evidence['description']}", key=f"evidence_{trial['case'].get('id', trial['case']['name'])}_{evidence['id']}"):
                        selected.append(evidence['id'])
                        notes[evidence['id']] = st.text_input('추가 설명 (선택)', key=f"memo_{trial['case'].get('id', trial['case']['name'])}_{evidence['id']}", max_chars=300)
                sent = st.form_submit_button('증거 제출 및 변론 시작', type='primary')
            if sent:
                try:
                    submit_evidence(trial, selected, notes)
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
        elif trial['stage'] == 'rebuttal':
            st.subheader(f"🗣️ 변론 {trial['turn'] + 1} / {len(case_rebuttals(trial['case'], trial['side']))}")
            with st.expander('제출한 증거'):
                for evidence in trial['evidence']:
                    st.write(f"- {evidence['name']}" + (f" — {evidence['memo']}" if evidence['memo'] else ''))
            for response in trial['responses']:
                st.info(f"{response['round']}차 반박: {response['choice']}")
            entry = case_rebuttals(trial['case'], trial['side'])[trial['turn']]
            st.caption('심리 주제: ' + entry['title'])
            st.caption('각 선택지는 증거의 해석과 주장 방식이 다릅니다. 설명을 읽고 판단하세요.')
            st.warning(f"**{trial['case']['name']}** — {entry['opponent']}")
            with st.form(f"response_{trial['turn']}"):
                idx = st.radio('어떻게 반박하시겠습니까?', list(range(len(entry['choices']))),
                               format_func=lambda i: entry['choices'][i][0])
                st.info('📝 선택한 변론의 논리: ' + entry['choices'][idx][2])
                sent = st.form_submit_button('반박 제출', type='primary')
            if sent:
                respond(trial, idx)
                st.rerun()
        elif trial['stage'] == 'ready_for_jury':
            st.success(f"증거 제출과 재반박 {len(trial['responses'])}회가 종료되었습니다.")
            with st.expander('전체 재판 기록', expanded=True):
                for evidence in trial['evidence']:
                    st.write('**증거:**', evidence['name'])
                for response in trial['responses']:
                    st.write(f"**{response['round']}차 변론:**", response['choice'])
                    st.caption(response['effect'])
            if st.button('배심원 심사 및 최종 판결', type='primary'):
                result = judge(trial)
                document = make_verdict(trial, result)
                trial['stage'] = 'judged'
                # 같은 사건이 재실행 시 중복 저장되지 않도록 한다.
                st.session_state.saved_id = save_case(trial, result, document)
                st.session_state.result = result
                st.session_state.document = document
                go('판결문')
        else:
            st.success('판결이 완료되었습니다.')
            if st.button('판결문 보기'):
                go('판결문')

elif page == '판결문':
    st.title('📜 판결 선고실')
    st.markdown('<span class="court-stamp">공식 아닌 공식 판결</span>', unsafe_allow_html=True)
    result, document = st.session_state.result, st.session_state.document
    if not result or not document:
        st.info('재판 진행 화면에서 배심원 심사를 마쳐 주세요.')
    else:
        st.subheader(f"선고: {result['verdict']} 🎉")
        if result['won']:
            st.success(f"🏆 {st.session_state.lawyer_side} 변호사 승소!")
        else:
            st.error(f"📉 {st.session_state.lawyer_side} 변호사 패소!")
        cols = st.columns(3)
        for col, vote in zip(cols, result['votes']):
            col.metric(f"{vote['emoji']} {vote['name']}", vote['vote'], f"유죄 점수 {vote['score']}", delta_color='off')
        st.subheader('배심원 판단 점수')
        st.bar_chart(pd.DataFrame([{'배심원':v['name'], '유죄 점수':v['score']} for v in result['votes']]).set_index('배심원'))
        st.info(document['reason'])
        st.warning('**선고:** ' + document['punishment'])
        st.text_area('판결문 전문', document['text'], height=340)
        st.download_button('판결문 다운로드 (.txt)', data=document['text'].encode('utf-8-sig'),
                           file_name=f"verdict_{st.session_state.saved_id}.txt", mime='text/plain')
        st.caption('실제 법적 판결이 아닌 오락용 시뮬레이션 결과입니다.')
        if st.button('판례 보관소 열기'):
            go('판례 보관소')

elif page == '판례 보관소':
    st.title('📚 황당 사건 기록 보관소')
    st.markdown('<div class="court-ticket"><div class="court-ticket-title">🗃️ 판례 박물관</div><div class="court-ticket-sub">과거의 엄숙하고도 쓸데없는 판결을 전시합니다.</div></div>', unsafe_allow_html=True)
    query = st.text_input('사건명 검색', placeholder='사건명을 입력하세요')
    rows = history(query)
    all_rows = history()
    a, b, c = st.columns(3)
    a.metric('전체 판례', len(all_rows))
    wins = sum(row[6] for row in all_rows)
    b.metric('승소 수', wins)
    c.metric('승률', f'{wins / len(all_rows) * 100:.1f}%' if all_rows else '0.0%')
    if not rows:
        st.info('저장된 판례가 없습니다.')
    else:
        st.dataframe(pd.DataFrame([{'번호':r[0], '날짜':r[1], '사건명':r[2], '유형':r[3],
                                   '변호사':r[4], '판결':r[5], '결과':'승소' if r[6] else '패소'} for r in rows]),
                     hide_index=True, use_container_width=True)
        selected_id = st.selectbox('판결문 자세히 보기', [r[0] for r in rows], format_func=lambda i: f'제{i}호 — {next(r[2] for r in rows if r[0]==i)}')
        record = next(r for r in rows if r[0] == selected_id)
        st.text_area('저장된 판결문', record[7], height=300)
        st.download_button('이 판결문 다운로드', record[7].encode('utf-8-sig'), file_name=f'verdict_{selected_id}.txt')
