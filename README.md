# IFRS 9 ECL Credit Risk Model

A simplified IFRS 9 Expected Credit Loss model using synthetic loan portfolio data with PD, LGD, EAD, staging logic, portfolio ECL calculation, and dashboard reporting.

## Business Problem

Banks and financial institutions are required to estimate expected credit losses under IFRS 9. This requires assessing credit risk, assigning loans into appropriate IFRS 9 stages, estimating Probability of Default, Loss Given Default, Exposure at Default, and calculating Expected Credit Loss.

This project demonstrates a simplified credit risk analytics framework using synthetic retail loan portfolio data.

## Objective

The objective of this project is to build an end-to-end IFRS 9 ECL model that can:

- Assign loans into IFRS 9 stages
- Estimate Probability of Default
- Calculate Loss Given Default
- Calculate Exposure at Default
- Compute Expected Credit Loss
- Summarise portfolio-level credit risk
- Present results through a simple dashboard

## Key Concepts

### Expected Credit Loss Formula

```text
ECL = PD × LGD × EAD
```

Where:

- **PD** = Probability of Default
- **LGD** = Loss Given Default
- **EAD** = Exposure at Default
- **ECL** = Expected Credit Loss

## IFRS 9 Staging Logic

This project uses simplified IFRS 9 staging rules:

```text
Stage 1: Performing loans
Stage 2: Loans with significant increase in credit risk
Stage 3: Default or credit-impaired loans
```

Simplified rule used:

- **Stage 1:** Days past due less than 30
- **Stage 2:** Days past due between 30 and 89
- **Stage 3:** Days past due 90 or above, or previous default flag equals 1

## Dataset

The project uses synthetic loan portfolio data created for demonstration purposes.

The dataset includes:

- Customer ID
- Loan amount
- Outstanding balance
- Interest rate
- Loan term
- Days past due
- Credit score
- Monthly income
- Debt-to-income ratio
- Collateral value
- Loan-to-value ratio
- Employment type
- Loan type
- Region
- Previous default flag
- IFRS 9 stage
- PD
- LGD
- EAD
- ECL
- Risk band

No confidential or real customer data is used.

## Methodology

The project follows these steps:

1. Generate synthetic loan portfolio data
2. Assign IFRS 9 stages based on days past due and default indicators
3. Estimate PD using credit risk drivers
4. Estimate LGD based on collateral coverage
5. Use outstanding balance as EAD
6. Calculate ECL using PD × LGD × EAD
7. Create portfolio-level summaries
8. Build a Streamlit dashboard for reporting

## Tools and Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Credit Risk Analytics
- IFRS 9 ECL
- Portfolio Risk Reporting

## Project Structure

```text
ifrs9-ecl-credit-risk-model/
│
├── README.md
├── requirements.txt
├── app.py
├── data/
│   └── synthetic_loan_portfolio.csv
├── src/
│   └── ecl_model.py
└── outputs/
    └── ecl_summary.csv
```

## Dashboard Features

The Streamlit dashboard will show:

- Total portfolio exposure
- Total Expected Credit Loss
- Average PD
- Average LGD
- Stage-wise exposure
- Stage-wise ECL
- Risk band distribution
- ECL by loan type
- ECL by region
- Top high-risk loans

## Business Relevance

This project is relevant for:

- Credit risk analytics
- IFRS 9 ECL modeling
- Banking risk management
- Portfolio monitoring
- Regulatory reporting
- Risk consulting
- Financial analytics
- Model governance reporting

## Future Improvements

- Add machine learning-based PD model
- Add macroeconomic scenario adjustment
- Add lifetime ECL for Stage 2 loans
- Add model validation and back-testing
- Add sensitivity testing
- Add stress testing scenarios
- Deploy dashboard using Streamlit Cloud

## Author

Sunam Pokharel  
Data Scientist | Credit Risk Analytics | IFRS 9 ECL | Financial AI | Machine Learning
