
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Diesel Calibration Assistant",
    layout="wide"
)

st.title("🚛 Diesel Calibration Assistant")

baseline_file = st.sidebar.file_uploader(
    "Baseline CSV",
    type=["csv"]
)

candidate_file = st.sidebar.file_uploader(
    "Candidate CSV",
    type=["csv"]
)

if baseline_file and candidate_file:

    baseline = pd.read_csv(baseline_file)
    candidate = pd.read_csv(candidate_file)

    st.success("Files loaded successfully")

    common_cols = list(
        set(baseline.columns).intersection(candidate.columns)
    )

    numeric_cols = []

    for col in common_cols:
        try:
            baseline[col] = pd.to_numeric(
                baseline[col]
            )
            candidate[col] = pd.to_numeric(
                candidate[col]
            )
            numeric_cols.append(col)
        except:
            pass

    result_list = []

    for col in numeric_cols:

        b_mean = baseline[col].mean()
        c_mean = candidate[col].mean()

        if b_mean != 0:
            delta = (
                (c_mean - b_mean)
                / b_mean
                * 100
            )
        else:
            delta = 0

        result_list.append(
            {
                "Signal": col,
                "Baseline": round(b_mean, 2),
                "Candidate": round(c_mean, 2),
                "Delta %": round(delta, 2)
            }
        )

    result_df = pd.DataFrame(result_list)

    st.subheader("📊 KPI Comparison")
    st.dataframe(
        result_df,
        use_container_width=True
    )

    st.subheader("📈 Signal Comparison")

    signal = st.selectbox(
        "Select Signal",
        