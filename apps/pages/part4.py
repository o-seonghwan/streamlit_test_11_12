import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import seaborn as sns

fm.fontManager.addfont("fonts/NanumGothic-Regular.ttf")
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False

DATA = "data/heart_failure_clinical_records_dataset.csv"
df = pd.read_csv(DATA)
st.title("심부전 환자 차트")
counts = df["DEATH_EVENT"].map({0: "생존", 1: "사망"}).value_counts()
st.bar_chart(counts)

fig, ax = plt.subplots()
ax.bar(counts.index, counts.values)
ax.set_title("사망 여부별 환자 수")
st.pyplot(fig)

fig, ax = plt.subplots()
ax.hist(df["age"], bins=11, range=(40, 95), color="#2E6B47")
ax.set_xlabel("나이")
ax.set_ylabel("환자 수")
st.pyplot(fig)

df["사망여부"] = df["DEATH_EVENT"].map({0: "생존", 1: "사망"})
fig, ax = plt.subplots()
sns.boxplot(data=df, x="사망여부", y="ejection_fraction",
hue="사망여부", legend=True, ax=ax)
ax.set_ylabel("박출률(%)")
st.pyplot(fig)

low, high = st.slider("나이 범위", 40, 95, (93, 94))
part = df[(df["age"] >= low) & (df["age"] <= high)]
if len(part) < 2:
    st.info(f"환자가 {len(part)}명이라 그래프를 그리지 않습니다.")
else:
    fig, ax = plt.subplots()
    sns.histplot(part["age"], kde=True, ax=ax)
    st.pyplot(fig)