# ⚖️ 쓸데없는 재판소 — 155개 사건, 변론 확장판

Streamlit 기반 가상 재판 게임. 원고·피고 중 한쪽의 변호사를 맡아 사건별 논거를 제출합니다.

## 이번 수정

- 155개 사건 전체에 원고·피고의 주장, 목표, 반대측 예상 반박을 연결
- 접수 화면에서 분야별 검색 후 양측 입장을 나란히 비교하고 변호사 선택
- 사건별 가상 증거 8개 중 1~3개 제출 (입장에 따라 유불리 표시)
- 상대방 질문에 맞춰 3차례 변론, 각 4가지 전략 선택
- 증거/변론의 방향(원고/피고/중립)을 배심원 점수에 반영
- 판결문 다운로드, SQLite 판례 저장, 직접 사건 작성 및 기존 12개 분야 유지

### 실행

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### 테스트

```powershell
python test_project.py
```

게임의 자료는 실제 증빙 서류가 아닌 **가상의 증거 후보와 논변**입니다. 철학·우주·초자연 주제의 판결도 과학적 사실 확정을 의미하지 않습니다. 외부 생성형 AI API는 사용하지 않고 규칙 기반 판결을 실행합니다. 개발에는 ChatGPT를 활용했습니다.

기존 사용자가 가진 `data/court.db`는 새 프로젝트의 `data/`에 직접 복사해 과거 판례를 유지할 수 있습니다.


## UI 개편
- 비어 있던 `pages/` 폴더(4개 빈 페이지) 삭제: 사이드바 중복 메뉴 제거
- 장난감 법정/엉뚱한 관공서 콘셉트의 스탬프, 종이 카드, 메뉴/폼/버튼 CSS 적용
- 기존 155개 사건, 12개 분야, 증거/변론/판결/판례 기능은 그대로 유지
- 외부 Google Fonts 요청이 차단되면 기본 sans-serif 글꼴로 표시

## 증거·변론 개편 (v1.4)
- 증거 카드에서 `원고 측 유리 / 피고 측 유리 / 중립`이라는 사전 정답 노출을 제거했습니다.
- 각 사건에 8개 증거·논거 카드, 3차례의 반대신문과 차례당 4개의 대응을 준비했습니다.
- 제출 시 선택한 카드가 어떤 논리인지 설명을 확인할 수 있습니다.
- 배심원 계산의 방향값은 내부 게임 규칙으로 유지하지만, 이를 사실의 진위·과학적 확증으로 해석하지 않습니다.
- 과학·초자연·철학 사건은 실증적 사실 / 가설 / 사고실험을 구별하도록 작성했습니다. 다수 사건은 주제별 논증 틀을 조합한 시나리오이며 독립적으로 학술 검증된 증거 목록은 아닙니다.

### 자료 작성 시 참고한 개념 자료
- NASA UAP FAQ: https://science.nasa.gov/uap/faqs/
- NASA Exoplanets Big Questions: https://science.nasa.gov/exoplanets/big-questions/
- Stanford Encyclopedia of Philosophy — Time Travel: https://plato.stanford.edu/entries/time-travel/
