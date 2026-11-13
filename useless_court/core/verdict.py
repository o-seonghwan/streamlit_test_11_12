"""재판 결과를 유머 판결문으로 변환한다."""

PUNISHMENTS = {
    "음식 분쟁": "다음 모임에서 음식 배분 담당 3회 수행",
    "생활 분쟁": "다음 약속 시간 10분 일찍 도착하기 3회",
    "소통 분쟁": "단톡방에 귀여운 이모티콘으로 성실히 답변하기 3회",
    "기타 분쟁": "상대에게 진심을 담은 사과와 간식 1개 전달",
}


def make_verdict(trial, result):
    """사건별 판결 이유와 결과 문자열을 만든다."""
    case = trial["case"]
    verdict = result["verdict"]
    votes = result["votes"]
    count = sum(v["vote"] == verdict for v in votes)
    # 분야별 황당한 형벌을 선택한다.
    group_punishments = {
        "음식": "다음 모임에서 메뉴 선정권을 상대에게 양보하기 3회",
        "학교·공부": "칠판 앞에서 사과문을 또박또박 낭독하기 1회",
        "친구·인간관계": "단톡방에 성의 있는 칭찬 메시지 보내기 3회",
        "일상생활": "공동 공간 정리 및 청소 담당 3회",
        "게임·인터넷": "게임 시작 전에 팀원 칭찬 3회 외치기",
        "동물·사물": "문제의 물건에게 정중하게 사과문 제출하기",
        "완전히 황당한 사건": "우주 평화 유지를 위한 반성문 1장 작성하기",
        "우주·외계인": "미확인 우주 신호를 정중하게 관찰하는 숙제 3회",
        "시간여행·평행우주": "미래의 자신에게 반성 편지 1통 작성",
        "귀신·초자연현상": "무서운 이야기의 출처를 꼼꼼히 확인하기 3회",
        "AI·미래기술": "로봇 윤리 규칙 3개를 진지하게 써오기",
        "철학·존재": "자기 주장에 대한 반론 3개 직접 적어오기",
    }
    punishment = group_punishments.get(case.get("group"), PUNISHMENTS.get(case["category"], PUNISHMENTS["기타 분쟁"])) if verdict == "유죄" else "무죄로서 형벌 없음. 화해를 권고함"
    summary = ("제출된 증거와 변론을 게임 규칙에 따라 검토한 결과, "
               f"배심원 {count}명이 {verdict} 의견을 제시하였습니다. "
               "이 재판은 재미를 위한 가상 판단이며 실제 법률적 효력이 없습니다.")
    if "debate" in case:
        summary += (f" 주요 쟁점은 '{case['description']}'이며, "
                    f"판단의 한계는 '{case['debate']['limit']}'입니다. "
                    "본 판결은 사실의 과학적 입증이나 법률적 결정을 의미하지 않습니다.")
    return {"punishment": punishment, "reason": summary,
            "text": f"[쓸데없는 재판소 판결문]\n사건: {case['name']}\n사실관계: {case['description']}\n원고: {case['plaintiff']}\n피고: {case['defendant']}\n변호사: {trial['side']}\n판결: {verdict}\n배심원 의견: {count}/3\n판결 이유: {summary}\n선고: {punishment}\n승패: {'승소' if result['won'] else '패소'}\n\n※ 본 문서는 오락용 가상 판결문입니다."}
