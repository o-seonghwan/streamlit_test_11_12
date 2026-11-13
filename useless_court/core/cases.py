"""사건 목록을 읽고 분야별로 분류한다."""
import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'cases.json'
GROUPS = ["음식", "학교·공부", "친구·인간관계", "일상생활", "게임·인터넷", "동물·사물", "완전히 황당한 사건", "우주·외계인", "시간여행·평행우주", "귀신·초자연현상", "AI·미래기술", "철학·존재"]


def load_cases():
    return json.loads(DATA_PATH.read_text(encoding='utf-8'))


def filter_cases(cases, group='전체', keyword=''):
    """선택한 분야와 검색어에 맞는 사건만 반환한다."""
    term = keyword.strip().casefold()
    return [case for case in cases if (group == '전체' or case['group'] == group)
            and (not term or term in case['name'].casefold() or term in case['description'].casefold())]
