"""증거와 변론 턴을 처리하는 2단계 로직."""

# 양측 모두 활용 가능한 증거로 구성한다.
EVIDENCE_TEMPLATES = {
    "음식 분쟁": [
        ("사전 합의 기록", "함께 먹기 전 분배·취식 방법을 정했다는 기록", "규칙"),
        ("동석자 증언", "당시 식탁에 있던 사람의 진술", "상황"),
        ("남겨진 음식 사진", "사건 직후 음식 상태가 담긴 사진", "상황"),
        ("평소의 식사 관행", "그동안 서로 음식을 나눠 먹던 방식", "관행"),
        ("실수였다는 정황", "상대가 합의 내용을 몰랐을 가능성", "고의"),
    ],
    "생활 분쟁": [
        ("약속 내용", "함께 약속한 행동과 시간의 기록", "규칙"),
        ("시간 기록", "사건이 발생한 시각을 확인할 수 있는 자료", "상황"),
        ("주변인 진술", "사건을 직접 목격한 사람의 이야기", "상황"),
        ("불가피한 사정", "약속을 지키기 어려웠던 상황에 대한 정황", "고의"),
        ("반복 여부 기록", "같은 행동이 과거에도 반복됐는지에 대한 기록", "관행"),
    ],
    "소통 분쟁": [
        ("대화 내용", "당사자 사이에 오간 메시지", "상황"),
        ("답변 요청 기록", "언제 어떻게 답변을 요청했는지에 관한 기록", "규칙"),
        ("상대의 사정", "응답할 수 없었을 만한 사정을 보여주는 정황", "고의"),
        ("기존 소통 관행", "평소 메시지에 답하는 방식", "관행"),
        ("제3자 증언", "대화를 함께 본 사람의 진술", "상황"),
    ],
    "기타 분쟁": [
        ("당사자 간 합의", "서로 지키기로 정했던 약속", "규칙"),
        ("현장 기록", "당시 상황을 보여주는 사진 또는 메모", "상황"),
        ("목격자 증언", "사건을 본 제3자의 진술", "상황"),
        ("고의성에 관한 정황", "의도적 행동인지 판단할 단서", "고의"),
        ("평소 관행", "비슷한 상황에서 해오던 행동", "관행"),
    ],
}

# 각 기본 사건에 맞춰 증거 제목을 조금 더 구체화한다.
SPECIAL_EVIDENCE = {
    "마지막 닭다리 사건": [
        ("닭다리 분배 약속", "마지막 닭다리를 남겨두기로 한 약속", "규칙"),
        ("빈 치킨 상자", "마지막 닭다리가 사라진 식탁의 상태", "상황"),
        ("동석 친구의 증언", "누가 마지막 닭다리를 먹었는지에 대한 증언", "상황"),
        ("평소 나눠 먹던 방식", "친구들끼리 치킨을 나누던 관행", "관행"),
        ("착각했다는 주장", "마지막 조각인지 몰랐을 가능성", "고의"),
    ],
    "탕수육 소스 무단 투하 사건": [
        ("소스 별도 제공 약속", "찍먹을 하기로 미리 정한 대화", "규칙"),
        ("소스가 부어진 사진", "사건 직후 탕수육의 상태", "상황"),
        ("동석자 증언", "소스를 부은 순간을 목격한 진술", "상황"),
        ("평소 부먹 관행", "일행이 평소 탕수육을 먹던 방식", "관행"),
        ("실수로 쏟았다는 주장", "의도하지 않고 소스를 쏟았을 가능성", "고의"),
    ],
    "알람 7개 무시 사건": [
        ("약속 시간 메시지", "정해진 약속 시각을 확인할 수 있는 메시지", "규칙"),
        ("알람 설정 화면", "설정했던 알람 7개의 기록", "상황"),
        ("기다린 시간 기록", "약속 장소에서 기다린 시간이 담긴 기록", "상황"),
        ("평소 지각 여부", "이전 약속에서도 지각했는지에 관한 기록", "관행"),
        ("기기 오류 가능성", "알람이 울리지 않았을 가능성을 보여주는 정황", "고의"),
    ],
    "단톡방 읽씹 사건": [
        ("답변 요청 메시지", "확실한 답변을 요청한 대화 기록", "규칙"),
        ("읽음 표시", "메시지를 확인했다는 표시", "상황"),
        ("모임 참가자 진술", "답변이 필요했던 상황에 대한 증언", "상황"),
        ("평소 답장 속도", "당사자가 평소 답장하는 관행", "관행"),
        ("바쁜 일정", "답장을 하기 어려웠던 사정을 나타내는 정황", "고의"),
    ],
    "피자 마지막 조각 실종 사건": [
        ("마지막 조각 합의", "마지막 조각을 어떻게 나눌지 정한 약속", "규칙"),
        ("빈 피자 상자", "마지막 조각이 사라진 상황을 보여주는 자료", "상황"),
        ("같이 먹던 사람의 증언", "누가 피자를 가져갔는지에 대한 증언", "상황"),
        ("평소 피자 분배 규칙", "일행이 평소 피자를 나누던 방식", "관행"),
        ("양보한 줄 알았다는 주장", "다른 사람이 포기했다고 오해했을 가능성", "고의"),
    ],
}

REBUTTALS = [
    {
        "title": "합의가 없었다는 주장",
        "opponent": "상대 측: 명확히 정한 규칙이 없으므로 위반이라고 단정할 수 없습니다.",
        "choices": [
            ("합의 기록을 다시 제시한다", "규칙", "사전에 정한 내용이 있었음을 강조합니다."),
            ("당사자가 느낀 피해를 설명한다", "피해", "기분과 관계의 손상을 중심으로 반박합니다."),
            ("규칙이 없어도 배려가 필요하다고 주장한다", "관행", "평소 지켜온 예의를 강조합니다."),
        ],
    },
    {
        "title": "고의성이 없었다는 주장",
        "opponent": "상대 측: 문제의 행동이 있었다 해도 실수였으니 책임을 무겁게 물을 수 없습니다.",
        "choices": [
            ("같은 일이 반복되었는지 따져 묻는다", "관행", "반복된 행동이었다는 점을 부각합니다."),
            ("고의 여부와 별개로 피해가 있었다고 주장한다", "피해", "실제 피해에 초점을 맞춥니다."),
            ("실수 가능성에 공감하며 처분을 낮춰 달라고 요청한다", "고의", "상대의 사정을 고려한 절충안을 제시합니다."),
        ],
    },
]


def case_rebuttals(case, side="원고 측"):
    """사건의 입장과 쟁점에 맞춰 3차 변론을 제공한다."""
    if case.get('debate_rounds'):
        result = []
        for round_data in case['debate_rounds']:
            opponent = round_data['plaintiff_challenge'] if side == '원고 측' else round_data['defendant_challenge']
            choices = [(o['name'], o['kind'], o['detail'], o['stance']) for o in round_data['options']]
            result.append({'title': round_data['title'], 'opponent': opponent, 'choices': choices})
        return result
    return REBUTTALS


def available_evidence(case):
    """사건에 맞는 증거 후보를 반환한다."""
    if case.get('evidence_options'):
        return case['evidence_options']
    if "debate" in case:
        d = case["debate"]
        rows = [
            ("주장 측 근거", d["pro"], "찬성"),
            ("반대 측 근거", d["con"], "반대"),
            ("쟁점 정의 자료", f"무엇을 판단하는지 확인: {case['description']}", "분석"),
            ("입증의 한계", d["limit"], "신중"),
            ("조건부 판단 보고서", f"양측의 논거를 비교하여 {d['limit']}라는 한계를 검토", "분석"),
        ]
        return [{"id":i,"name":name,"description":desc,"kind":kind} for i,(name,desc,kind) in enumerate(rows)]
    rows = SPECIAL_EVIDENCE.get(case["name"])
    if rows is None and case.get('group'):
        # 사건별 쟁점을 반영한 가상 증거 5개를 제공한다.
        issue = case['description'].rstrip('?.!')
        rows = [
            ("사건 전 약속 기록", f"'{case['name']}' 관련 사전 약속이나 합의 여부", "규칙"),
            ("당시 현장 기록", f"다음 쟁점에 관한 당시 상황 기록: {issue}", "상황"),
            ("목격자 또는 제3자 진술", f"'{case['name']}' 상황을 지켜본 사람의 가상 진술", "상황"),
            ("평소 행동 기록", f"비슷한 상황에서 당사자들이 평소 어떻게 행동했는지", "관행"),
            ("실수·불가피한 사정", f"'{case['name']}' 관련 행동에 고의가 없었다는 정황", "고의"),
        ]
    if rows is None:
        rows = EVIDENCE_TEMPLATES.get(case["category"], EVIDENCE_TEMPLATES["기타 분쟁"])
    return [{"id": i, "name": name, "description": desc, "kind": kind} for i, (name, desc, kind) in enumerate(rows)]


def new_trial(case, side):
    """사건을 새로 접수할 때 재판 상태를 초기화한다."""
    return {"case": dict(case), "side": side, "stage": "evidence", "evidence": [], "turn": 0, "responses": []}


def submit_evidence(trial, selections, descriptions):
    """선택한 증거를 최대 3개까지 기록한다."""
    if not 1 <= len(selections) <= 3:
        raise ValueError("증거를 1개 이상 3개 이하로 선택해 주세요.")
    available = {item["id"]: item for item in available_evidence(trial["case"])}
    if len(set(selections)) != len(selections) or any(item not in available for item in selections):
        raise ValueError("유효한 증거를 중복 없이 선택해 주세요.")
    trial["evidence"] = [{**available[item], "memo": descriptions.get(item, "").strip()[:300]} for item in selections]
    trial["stage"] = "rebuttal"
    trial["turn"] = 0


def respond(trial, option_index):
    """반박 선택 후 다음 턴으로 이동한다."""
    if trial["stage"] != "rebuttal" or trial["turn"] >= len(case_rebuttals(trial["case"], trial["side"])):
        raise ValueError("지금은 변론을 진행할 수 없습니다.")
    entry = case_rebuttals(trial["case"], trial["side"])[trial["turn"]]
    if not 0 <= option_index < len(entry["choices"]):
        raise ValueError("잘못된 변론 선택입니다.")
    choice = entry["choices"][option_index]
    trial["responses"].append({"round": trial["turn"] + 1, "opponent": entry["opponent"], "choice": choice[0], "kind": choice[1], "effect": choice[2], "stance": choice[3] if len(choice) > 3 else trial["side"]})
    trial["turn"] += 1
    if trial["turn"] == len(case_rebuttals(trial["case"], trial["side"])):
        trial["stage"] = "ready_for_jury"
