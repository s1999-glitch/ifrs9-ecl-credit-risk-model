import pandas as pd
import numpy as np


def load_loan_data(file_path):
    """
    Load synthetic loan portfolio data.
    """
    df = pd.read_csv(file_path)
    return df


def assign_ifrs9_stage(row):
    """
    Assign simplified IFRS 9 stage based on days past due and previous default flag.
    """

    if row["days_past_due"] >= 90 or row["previous_default_flag"] == 1:
        return "Stage 3"
    elif row["days_past_due"] >= 30:
        return "Stage 2"
    else:
        return "Stage 1"


def calculate_pd(row):
    """
    Estimate simplified Probability of Default using credit risk indicators.
    This is a rule-based PD model for demonstration purposes.
    """

    base_pd = 0.02

    # Credit score adjustment
    if row["credit_score"] < 580:
        base_pd += 0.18
    elif row["credit_score"] < 620:
        base_pd += 0.12
    elif row["credit_score"] < 680:
        base_pd += 0.06
    elif row["credit_score"] < 720:
        base_pd += 0.03

    # Debt-to-income adjustment
    if row["debt_to_income_ratio"] > 0.65:
        base_pd += 0.12
    elif row["debt_to_income_ratio"] > 0.55:
        base_pd += 0.08
    elif row["debt_to_income_ratio"] > 0.45:
        base_pd += 0.04

    # Loan-to-value adjustment
    if row["loan_to_value_ratio"] > 1.2:
        base_pd += 0.10
    elif row["loan_to_value_ratio"] > 1.0:
        base_pd += 0.07
    elif row["loan_to_value_ratio"] > 0.8:
        base_pd += 0.03

    # Days past due adjustment
    if row["days_past_due"] >= 90:
        base_pd += 0.30
    elif row["days_past_due"] >= 60:
        base_pd += 0.18
    elif row["days_past_due"] >= 30:
        base_pd += 0.10
    elif row["days_past_due"] > 0:
        base_pd += 0.03

    # Previous default adjustment
    if row["previous_default_flag"] == 1:
        base_pd += 0.25

    # Cap PD between 1% and 95%
    pd_value = min(max(base_pd, 0.01), 0.95)

    return round(pd_value, 4)


def calculate_lgd(row):
    """
    Estimate simplified Loss Given Default based on collateral coverage.
    """

    outstanding_balance = row["outstanding_balance"]
    collateral_value = row["collateral_value"]

    if outstanding_balance <= 0:
        return 0.0

    collateral_coverage = collateral_value / outstanding_balance

    if collateral_coverage >= 1.5:
        lgd = 0.20
    elif collateral_coverage >= 1.0:
        lgd = 0.35
    elif collateral_coverage >= 0.75:
        lgd = 0.50
    else:
        lgd = 0.65

    return round(lgd, 4)


def assign_risk_band(pd_value):
    """
    Assign risk band based on Probability of Default.
    """

    if pd_value < 0.05:
        return "Low Risk"
    elif pd_value < 0.15:
        return "Medium Risk"
    elif pd_value < 0.30:
        return "High Risk"
    else:
        return "Critical Risk"


def calculate_ecl(df):
    """
    Calculate IFRS 9 stage, PD, LGD, EAD, and ECL.
    """

    df = df.copy()

    df["stage"] = df.apply(assign_ifrs9_stage, axis=1)
    df["pd"] = df.apply(calculate_pd, axis=1)
    df["lgd"] = df.apply(calculate_lgd, axis=1)
    df["ead"] = df["outstanding_balance"]

    # Stage adjustment: Stage 2 and Stage 3 carry higher risk
    df["adjusted_pd"] = np.where(
        df["stage"] == "Stage 1",
        df["pd"],
        np.where(df["stage"] == "Stage 2", df["pd"] * 1.5, df["pd"] * 2.0),
    )

    df["adjusted_pd"] = df["adjusted_pd"].clip(upper=0.95)

    df["ecl"] = df["adjusted_pd"] * df["lgd"] * df["ead"]
    df["ecl"] = df["ecl"].round(2)

    df["risk_band"] = df["adjusted_pd"].apply(assign_risk_band)

    return df


def create_ecl_summary(df):
    """
    Create portfolio-level ECL summary.
    """

    summary = {
        "total_loans": len(df),
        "total_exposure": round(df["ead"].sum(), 2),
        "total_ecl": round(df["ecl"].sum(), 2),
        "average_pd": round(df["adjusted_pd"].mean(), 4),
        "average_lgd": round(df["lgd"].mean(), 4),
        "stage_1_loans": int((df["stage"] == "Stage 1").sum()),
        "stage_2_loans": int((df["stage"] == "Stage 2").sum()),
        "stage_3_loans": int((df["stage"] == "Stage 3").sum()),
    }

    return summary
