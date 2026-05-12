import streamlit as st
import pandas as pd
import plotly.express as px

from src.ecl_model import load_loan_data, calculate_ecl, create_ecl_summary


st.set_page_config(
    page_title="IFRS 9 ECL Credit Risk Model",
    page_icon="🏦",
    layout="wide"
)


st.title("IFRS 9 Expected Credit Loss Credit Risk Model")

st.write(
    "A simplified IFRS 9 ECL model using synthetic loan portfolio data. "
    "The model calculates PD, LGD, EAD, IFRS 9 stage, Expected Credit Loss, "
    "and portfolio-level credit risk summaries."
)


DATA_PATH = "data/synthetic_loan_portfolio.csv"


try:
    df = load_loan_data(DATA_PATH)
    ecl_df = calculate_ecl(df)
    summary = create_ecl_summary(ecl_df)

    st.success("Synthetic loan portfolio loaded and ECL calculated successfully.")

    st.sidebar.title("Dashboard Filters")

    selected_stage = st.sidebar.multiselect(
        "Select IFRS 9 Stage",
        options=sorted(ecl_df["stage"].unique()),
        default=sorted(ecl_df["stage"].unique())
    )

    selected_region = st.sidebar.multiselect(
        "Select Region",
        options=sorted(ecl_df["region"].unique()),
        default=sorted(ecl_df["region"].unique())
    )

    selected_loan_type = st.sidebar.multiselect(
        "Select Loan Type",
        options=sorted(ecl_df["loan_type"].unique()),
        default=sorted(ecl_df["loan_type"].unique())
    )

    filtered_df = ecl_df[
        (ecl_df["stage"].isin(selected_stage)) &
        (ecl_df["region"].isin(selected_region)) &
        (ecl_df["loan_type"].isin(selected_loan_type))
    ]

    st.subheader("Portfolio Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Loans", len(filtered_df))
    col2.metric("Total Exposure", f"NPR {filtered_df['ead'].sum():,.0f}")
    col3.metric("Total ECL", f"NPR {filtered_df['ecl'].sum():,.0f}")
    col4.metric("Average PD", f"{filtered_df['adjusted_pd'].mean() * 100:.2f}%")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Average LGD", f"{filtered_df['lgd'].mean() * 100:.2f}%")
    col6.metric("Stage 1 Loans", int((filtered_df["stage"] == "Stage 1").sum()))
    col7.metric("Stage 2 Loans", int((filtered_df["stage"] == "Stage 2").sum()))
    col8.metric("Stage 3 Loans", int((filtered_df["stage"] == "Stage 3").sum()))

    st.subheader("Stage-wise Exposure and ECL")

    stage_summary = (
        filtered_df.groupby("stage")
        .agg(
            total_exposure=("ead", "sum"),
            total_ecl=("ecl", "sum"),
            avg_pd=("adjusted_pd", "mean"),
            avg_lgd=("lgd", "mean"),
            loan_count=("loan_id", "count")
        )
        .reset_index()
    )

    st.dataframe(stage_summary, use_container_width=True)

    fig_stage_ecl = px.bar(
        stage_summary,
        x="stage",
        y="total_ecl",
        title="Expected Credit Loss by IFRS 9 Stage",
        text_auto=True
    )

    st.plotly_chart(fig_stage_ecl, use_container_width=True)

    st.subheader("Risk Band Distribution")

    risk_summary = (
        filtered_df.groupby("risk_band")
        .agg(
            loan_count=("loan_id", "count"),
            total_ecl=("ecl", "sum"),
            total_exposure=("ead", "sum")
        )
        .reset_index()
    )

    fig_risk = px.pie(
        risk_summary,
        names="risk_band",
        values="loan_count",
        title="Loan Distribution by Risk Band"
    )

    st.plotly_chart(fig_risk, use_container_width=True)

    st.subheader("ECL by Loan Type")

    loan_type_summary = (
        filtered_df.groupby("loan_type")
        .agg(
            total_ecl=("ecl", "sum"),
            total_exposure=("ead", "sum"),
            loan_count=("loan_id", "count")
        )
        .reset_index()
    )

    fig_loan_type = px.bar(
        loan_type_summary,
        x="loan_type",
        y="total_ecl",
        title="Expected Credit Loss by Loan Type",
        text_auto=True
    )

    st.plotly_chart(fig_loan_type, use_container_width=True)

    st.subheader("ECL by Region")

    region_summary = (
        filtered_df.groupby("region")
        .agg(
            total_ecl=("ecl", "sum"),
            total_exposure=("ead", "sum"),
            loan_count=("loan_id", "count")
        )
        .reset_index()
    )

    fig_region = px.bar(
        region_summary,
        x="region",
        y="total_ecl",
        title="Expected Credit Loss by Region",
        text_auto=True
    )

    st.plotly_chart(fig_region, use_container_width=True)

    st.subheader("Top 10 High-Risk Loans")

    top_risk_loans = filtered_df.sort_values(
        by="ecl",
        ascending=False
    ).head(10)

    st.dataframe(
        top_risk_loans[
            [
                "customer_id",
                "loan_id",
                "loan_type",
                "region",
                "stage",
                "risk_band",
                "credit_score",
                "days_past_due",
                "adjusted_pd",
                "lgd",
                "ead",
                "ecl"
            ]
        ],
        use_container_width=True
    )

    st.subheader("Full ECL Output")

    st.dataframe(ecl_df, use_container_width=True)

    csv = ecl_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download ECL Output CSV",
        data=csv,
        file_name="ecl_output.csv",
        mime="text/csv"
    )

    st.subheader("Business Interpretation")

    st.write(
        "This dashboard demonstrates how IFRS 9 Expected Credit Loss can be calculated "
        "using PD, LGD, and EAD. Stage 3 loans and loans with high PD contribute more "
        "to expected credit loss. The dashboard helps risk teams monitor portfolio quality, "
        "identify high-risk accounts, and support management reporting."
    )


except FileNotFoundError:
    st.error("Data file not found. Please check whether data/synthetic_loan_portfolio.csv exists.")
