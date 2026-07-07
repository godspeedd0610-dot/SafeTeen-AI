import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(
    page_title="SafeTeen AI",
    page_icon="🛡",
    layout="centered"
)

# AI 모델 불러오기
model = joblib.load("fraud_ai_model.pkl")

st.title("🛡 SafeTeen AI")
st.subheader("청소년 금융사기 위험도 분석")

st.markdown("""
최근 청소년을 대상으로 한 금융사기가 증가하고 있습니다.

간단한 설문을 통해
AI가 금융사기 위험도를 분석해드립니다.
""")

st.divider()

st.header("📝 설문조사")

grade = st.selectbox(
    "학년",
    [1,2,3]
)

used_market = st.radio(
    "중고거래를 해본 적이 있나요?",
    ["예","아니오"]
)

game_trade = st.radio(
    "게임 아이템 또는 계정 거래를 해본 적이 있나요?",
    ["예","아니오"]
)

clicked_link = st.radio(
    "모르는 사람이 보낸 링크를 눌러본 적이 있나요?",
    ["예","아니오"]
)

sns_parttime = st.radio(
    "SNS에서 고수익 알바 광고를 보고 연락한 적이 있나요?",
    ["예","아니오"]
)

personal_info = st.radio(
    "낯선 사이트에 개인정보를 입력한 적이 있나요?",
    ["예","아니오"]
)

education = st.radio(
    "금융사기 예방교육을 받은 적이 있나요?",
    ["예","아니오"]
)

confidence = st.selectbox(
    "금융사기를 구별할 자신이 있나요?",
    ["낮음","보통","높음"]
)
if st.button("🤖 AI 위험도 분석하기"):

    confidence_value = {
        "낮음": 0,
        "보통": 1,
        "높음": 2
    }

    input_data = pd.DataFrame([{
        "grade": grade,
        "used_market": 1 if used_market=="예" else 0,
        "game_trade": 1 if game_trade=="예" else 0,
        "clicked_link": 1 if clicked_link=="예" else 0,
        "sns_parttime": 1 if sns_parttime=="예" else 0,
        "personal_info": 1 if personal_info=="예" else 0,
        "education": 1 if education=="예" else 0,
        "confidence": confidence_value[confidence]
    }])

    result = model.predict(input_data)[0]

    st.divider()
    st.header("🤖 AI 분석 결과")

    if result == "낮음":
        percent = 25
        color = "🟢"
    elif result == "보통":
        percent = 60
        color = "🟡"
    else:
        percent = 90
        color = "🔴"

    st.metric(
        label="위험도",
        value=f"{color} {result}"
    )

    st.progress(percent/100)

    st.write(f"위험도 점수 : {percent}%")

    st.divider()
    st.subheader("📌 AI가 판단한 주요 위험 요인")

    reasons = []

    if clicked_link == "예":
        reasons.append("⚠️ 모르는 링크를 클릭한 경험")

    if personal_info == "예":
        reasons.append("⚠️ 낯선 사이트에 개인정보를 입력한 경험")

    if sns_parttime == "예":
        reasons.append("⚠️ SNS 고수익 알바 광고 접촉 경험")

    if used_market == "예":
        reasons.append("⚠️ 중고거래 경험")

    if game_trade == "예":
        reasons.append("⚠️ 게임 아이템·계정 거래 경험")

    if education == "아니오":
        reasons.append("⚠️ 금융사기 예방교육 경험 부족")

    if len(reasons) == 0:
        st.success("현재 응답에서는 뚜렷한 위험 요인이 발견되지 않았습니다.")
    else:
        for r in reasons:
            st.write(r)

    st.divider()

    st.subheader("🛡 맞춤형 예방법")

    if result == "높음":
        st.error("""
- 모르는 링크는 절대 클릭하지 마세요.
- 선입금을 요구하면 거래를 중단하세요.
- 개인정보와 인증번호를 입력하지 마세요.
- 의심되면 부모님이나 선생님과 상담하세요.
""")

    elif result == "보통":
        st.warning("""
- 거래 전 판매자를 확인하세요.
- 안전결제를 이용하세요.
- 문자 속 링크는 한 번 더 확인하세요.
""")

    else:
        st.success("""
- 현재 예방 습관이 좋은 편입니다.
- 앞으로도 개인정보를 신중하게 관리하세요.
- 의심되는 문자는 즉시 삭제하세요.
""")
       st.divider()

    st.subheader("📖 실제 청소년 금융사기 사례")

    if result == "높음":
        st.error("""
중고거래에서 선입금을 요구받고 입금했지만 판매자와 연락이 끊긴 사례가 있습니다.

👉 선입금은 매우 위험합니다.
""")

    elif result == "보통":
        st.warning("""
택배 주소 수정 문자를 받고 링크를 눌러 개인정보가 유출된 사례가 있습니다.

👉 문자 속 링크는 반드시 확인하세요.
""")

    else:
        st.success("""
금융사기 예방교육을 받은 학생이 의심스러운 문자를 발견하고 신고하여 피해를 예방한 사례가 있습니다.

👉 지금처럼 안전한 습관을 계속 유지하세요!
""")

    st.divider()

    st.info("🛡 본 결과는 교육용 AI 분석 결과이며 실제 금융사기 여부를 판단하는 서비스는 아닙니다.")

    st.balloons()
      
  
