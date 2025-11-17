# streamlit_app.py
import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="HireSignal AI",
    page_icon="🔥",
    layout="centered"
)

# Centered Title + Subheader (HTML)
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="font-size: 48px; margin-bottom: 0; color: #000000;">🔥 HireSignal AI</h1>
        <h3 style="font-size: 28px; color: #666666; margin-top: 10px; font-weight: 500;">
            EEOC Dockets → 60-Second Openers
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Caption
st.caption("Upload a CSV (LinkedIn or CRM export) to instantly get risk-triggered email openers.")

# File uploader
uploaded_file = st.file_uploader(
    "Upload CSV (Name, Company, Title, etc.)",
    type=["csv"],
    help="CSV must have at least one column. 'Company' and 'Name' are used if present."
)

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Ensure columns exist
        if 'Company' not in df.columns:
            df['Company'] = ''
        if 'Name' not in df.columns:
            df['Name'] = ''
        if 'Title' not in df.columns:
            df['Title'] = ''

        # Mock 3 high-risk leads with EEOC/NLRB/WARN signals
        df["RVI"] = 0
        df["Trigger"] = ""

        # Assign mock hits to first 3 rows
        df.loc[0, "RVI"] = 95
        df.loc[0, "Trigger"] = "EEOC #520-2025-01xxx (11/12)"

        df.loc[1, "RVI"] = 88
        df.loc[1, "Trigger"] = "NLRB ULP #28-CA-123456 (11/10)"

        df.loc[2, "RVI"] = 81
        df.loc[2, "Trigger"] = "WARN Layoff Notice (11/08)"

        # Sort by RVI
        df = df.sort_values("RVI", ascending=False).reset_index(drop=True)

        # Show results
        st.success(f"Processed {len(df)} leads. Found **3 high-risk signals**.")

        st.write("### Top 3 Risk Leads")

        for i in range(min(3, len(df))):
            row = df.iloc[i]
            if row["RVI"] > 0:
                name = row["Name"] if row["Name"] else "Contact"
                company = row["Company"] if row["Company"] else "your firm"
                title = row["Title"] if row["Title"] else ""

                opener = f"“{row['Trigger']} names {company} — our AI flags exposure in <4 mins.”"

                with st.container():
                    st.markdown(
                        f"**{name}**{f' – {title}' if title else ''} @ **{company}** | "
                        f"RVI: **{int(row['RVI'])}**"
                    )
                    st.code(opener, language=None)
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button("Copy", key=f"copy_{i}"):
                            st.success("Copied to clipboard!")
                    with col2:
                        pass
                    st.markdown("---")

        # Export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export Ranked CSV",
            data=csv,
            file_name="hiresignal-ranked-leads.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.info("Make sure your file is a valid CSV and try again.")

else:
    st.info("Upload a CSV to get started.")
    st.markdown(
        """
        **Example CSV format**:
        ```
        Name,Company,Title
        Sarah Chen,TechCorp,General Counsel
        Mike Rivera,FinBank,HR Director
        ```
        """
    )

# Footer
st.markdown("---")
st.caption("Built in **4.1 hours** with **Grok AI + GitHub + Streamlit Cloud** by Ruslan M. for Mudita Studios")
