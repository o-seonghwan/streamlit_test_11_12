"""배심원별 가중치로 판결을 산출한다."""

JURORS = [
    {"name": "원칙주의 감자", "emoji": "🥔", "weights": {"규칙": .60, "피해": .20, "고의": .20}},
    {"name": "감성파 고양이", "emoji": "🐱", "weights": {"규칙": .20, "피해": .60, "고의": .20}},
    {"name": "귀찮은 나무늘보", "emoji": "🦥", "weights": {"규칙": .20, "피해": .20, "고의": .60}},
]


def judge(trial):
    """제출한 선택을 게임용 유죄 점수로 계산한다."""
    # 증거는 사건 사실 확정이 아닌 게임 선택지로만 취급한다.
    features = {"규칙": 50., "피해": 50., "고의": 50.}
    side_sign = 1 if trial["side"] == "원고 측" else -1
    evidence_effects = {"규칙": ("규칙", 18), "상황": ("피해", 12), "관행": ("규칙", 8), "고의": ("고의", -18)}
    for ev in trial['evidence']:
        if 'direction' in ev:
            # 증거가 유리한 쪽을 반영하며, 방향이 중립이면 변동을 작게 한다.
            direction = ev['direction']
            key = ev['kind'] if ev['kind'] in features else '규칙'
            features[key] += 12 * direction
        elif "debate" in trial["case"]:
            key, delta = {"찬성": ("규칙", 20), "반대": ("규칙", -20), "분석": ("피해", 10), "신중": ("고의", -12)}[ev['kind']]
            features[key] += delta
        else:
            key, delta = evidence_effects.get(ev['kind'], ('피해', 0))
            features[key] += delta * side_sign
    response_effects = {"규칙": ("규칙", 20), "피해": ("피해", 20), "관행": ("규칙", 12), "고의": ("고의", -20)}
    for resp in trial['responses']:
        if trial['case'].get('debate_rounds'):
            key = resp['kind'] if resp['kind'] in features else '규칙'
            direction = {'plaintiff': 1, 'defendant': -1, 'neutral': 0}.get(resp.get('stance'), 0)
            features[key] += 14 * direction
        elif 'debate' in trial['case']:
            key, delta = {'규칙': ('규칙', 18), '피해': ('피해', 12), '신중': ('고의', -8)}[resp['kind']]
            features[key] += delta * side_sign if resp['kind'] != '신중' else delta
        else:
            key, delta = response_effects[resp['kind']]
            features[key] += delta if resp['kind'] == '고의' else delta * side_sign
    features = {k: max(0, min(100, v)) for k, v in features.items()}
    votes = []
    for juror in JURORS:
        score = round(sum(features[k] * w for k, w in juror["weights"].items()), 1)
        votes.append({"name": juror["name"], "emoji": juror["emoji"], "score": score,
                      "vote": "유죄" if score >= 50 else "무죄"})
    guilty = sum(v["vote"] == "유죄" for v in votes) >= 2
    verdict = "유죄" if guilty else "무죄"
    return {"features": features, "votes": votes, "verdict": verdict,
            "won": (guilty and trial["side"] == "원고 측") or (not guilty and trial["side"] == "피고 측")}
