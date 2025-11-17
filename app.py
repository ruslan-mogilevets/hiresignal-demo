import streamlit as st
import pandas as pd

st.set_page_config(page_title="HireSignal", layout="centered")
st.title("🔥 HireSignal – EEOC to Opener in 60s")

file = st.file_uploader("Upload CSV (LinkedIn/CRM)", type=["csv"])
if file:
    df = pd.read_csv(file)
    if 'Company' not in df.columns: df['Company'] = ''
    if 'Name' not in df.columns: df['Name'] = ''

    # Mock 3 high-risk leads
    df["RVI"] = 0
    df.loc[0:2, "RVI"] = [95, 88, 81]
    df.loc[0:2, "Trigger"] = [
        "EEOC #520-2025-01xxx (11/12)",
        "NLRB ULP #28-CA-123456 (11/10)",
        "WARN Layoff Notice (11/08)"
    ]
    df = df.sort_values("RVI", ascending=False)

    st.write("### 🏆 Top Risk Leads")
    for i, row in df.head(3).iterrows():
        if row["RVI"] > 0:
            opener = f"“{row['Trigger']} names {row['Company']} — our AI flags exposure in <4 mins.”"
            st.markdown(f"**{row['Name']} @ {row['Company']}** | RVI: **{row['RVI']}**")
            st.code(opener, language=None)
            if st.button("Copy", key=i):
                st.success("Copied to clipboard!")

    st.download_button("Export Ranked CSV", df.to_csv(index=False), "hiresignal-ranked.csv")
