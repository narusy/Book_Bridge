import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="도서 추천 프로그램", layout="wide")
st.title("##도서 추천 프로그램##")

# 로컬에 있는 기본 CSV 경로 (배포할 때 repo에 포함)
csv_path = Path(__file__).parent / "2-2프봉_도서목록.csv"

# 파일 업로드 위젯: 사용자가 직접 업로드 가능 (Google Drive 파일 소유권 문제 해결)
uploaded = st.file_uploader("원본 CSV 파일을 업로드하세요 (선택). 업로드하지 않으면 앱에 포함된 기본 파일을 사용합니다.", type=["csv"])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded, encoding='cp949')
    except Exception:
        df = pd.read_csv(uploaded)  # 인코딩 실패 시 재시도
else:
    if csv_path.exists():
        try:
            df = pd.read_csv(csv_path, encoding='cp949')
        except Exception:
            df = pd.read_csv(csv_path, encoding='utf-8', engine='python')

# 데이터 확인
if 'df' not in locals():
    st.error("데이터를 불러오지 못했습니다. CSV 파일을 업로드하거나, 관리자인 경우 앱에 CSV를 추가해주세요.")
    st.stop()

# UI
분야 = st.selectbox("분야를 선택하세요", ["인문", "사회", "자연", "공학", "의약", "예체능"])
진로_분류 = {
    "인문": ["전체보기", "인문", "국어", "영어", "문학", "역사", "미디어", "상담심리", "도덕"],
    "사회": ["전체보기", "사회", "경영", "경제", "교육"],
    "자연": ["전체보기", "과학", "수학", "환경", "생명"],
    "공학": ["전체보기", "건축", "기계공학", "로봇공학", "컴퓨터공학", "소프트웨어공학", "전기전자공학", "화학공학", "과학기술"],
    "의약": ["전체보기", "의학_의예", "의학_치의예", "의학_수의예", "약학", "간호"],
    "예체능": ["전체보기", "미술", "음악", "체육"]
}
진로 = st.selectbox("세부 진로를 선택하세요", 진로_분류[분야])

# 필터링 전에 컬럼명 정리(공백,대소문자 예민 문제 완화)
df.columns = [c.strip() for c in df.columns]

if 진로 == "전체보기":
    filtered = df[df['분야'].astype(str).str.strip() == 분야]
else:
    filtered = df[df['진로'].astype(str).str.strip() == 진로]

st.markdown(f"### 결과: {len(filtered)} 건")
st.dataframe(filtered, use_container_width=True)

# CSV 다운로드 버튼 (사용자가 결과를 받을 수 있게)
def convert_df(df_in):
    return df_in.to_csv(index=False).encode('utf-8-sig')

csv_bytes = convert_df(filtered)
st.download_button("결과 CSV 다운로드", csv_bytes, file_name="추천_도서.csv", mime="text/csv")
