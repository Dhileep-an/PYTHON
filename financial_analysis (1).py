"""
Financial Data Extraction & Analysis Script (2023–2025)
Companies: Microsoft, Tesla, Apple
Source Data: 10-K SEC Filings
"""

import pandas as pd


def load_financial_data() -> pd.DataFrame:
    """Compiles manually extracted 10-K financial metrics (2023-2025)
    into a pandas DataFrame.
    All figures are in millions of USD ($M).
    """
    raw_data = {
        "Company": [
            "Microsoft",
            "Microsoft",
            "Microsoft",
            "Tesla",
            "Tesla",
            "Tesla",
            "Apple",
            "Apple",
            "Apple",
        ],
        "Year": [2023, 2024, 2025, 2023, 2024, 2025, 2023, 2024, 2025],
        "Total Revenue": [
            211915,
            245122,
            281724,
            96773,
            97690,
            94827,
            383285,
            391035,
            416161,
        ],
        "Net Income": [
            72361,
            88136,
            101832,
            14997,
            7153,
            3794,
            96995,
            93736,
            112010,
        ],
        "Total Assets": [
            411976,
            512163,
            612161,
            106618,
            122070,
            137806,
            352583,
            364980,
            359241,
        ],
        "Total Liabilities": [
            205753,
            243686,
            277192,
            43009,
            48453,
            54999,
            290437,
            308030,
            285508,
        ],
        "Operating Cash Flow": [
            87582,
            118548,
            136168,
            13256,
            14923,
            14747,
            110543,
            118248,
            111482,
        ],
    }
    return pd.DataFrame(raw_data)


def compute_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates Year-over-Year (YoY) growth percentages and financial ratios."""
    # Ensure dataset is sorted chronologically
    df = df.sort_values(by=["Company", "Year"]).reset_index(drop=True)

    metrics = [
        "Total Revenue",
        "Net Income",
        "Total Assets",
        "Total Liabilities",
        "Operating Cash Flow",
    ]

    # Calculate YoY Growth (%)
    for metric in metrics:
        df[f"{metric} YoY Growth (%)"] = (
            df.groupby("Company")[metric].pct_change() * 100
        )

    # Calculate Net Profit Margin (%)
    df["Net Profit Margin (%)"] = (df["Net Income"] / df["Total Revenue"]) * 100

    # Calculate Debt-to-Asset Ratio
    df["Debt-to-Asset Ratio"] = df["Total Liabilities"] / df["Total Assets"]

    return df


def main():
    # 1. Load Data
    df = load_financial_data()

    # 2. Export raw data to CSV for record keeping
    df.to_csv("financial_data_2023_2025.csv", index=False)
    print("✓ Raw financial dataset saved to 'financial_data_2023_2025.csv'
")

    # 3. Analyze Data
    analyzed_df = compute_financial_metrics(df)

    # 4. Print Detailed Financial Results
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    print("=========================================================")
    print("        DETAILED FINANCIAL METRICS & YoY GROWTH          ")
    print("=========================================================")
    print(analyzed_df.round(2))

    # 5. Summary Aggregations
    summary = (
        analyzed_df.groupby("Company")[
            [
                "Total Revenue",
                "Net Income",
                "Net Profit Margin (%)",
                "Operating Cash Flow",
            ]
        ]
        .mean()
        .round(2)
    )

    print("
=========================================================")
    print("         3-YEAR AVERAGE PERFORMANCE SUMMARY ($M)         ")
    print("=========================================================")
    print(summary)


if __name__ == "__main__":
    main()
