# Baseline financial data extracted from annual financial statements
FINANCIAL_DATA = {
    "total_revenue_2025": "$391.04 billion",
    "revenue_growth": "2.02% increase year-over-year",
    "net_income_2025": "$93.74 billion",
    "net_income_change": "decreased by 3.35% from FY2024 ($96.99 billion)",
    "operating_cash_flow": "$118.26 billion",
    "gross_profit_margin": "46.21%"
}

# Predefined query-to-response mapping (normalized keys)
QUERY_RESPONSES = {
    "what is the total revenue?": 
        f"The total revenue for the latest fiscal year is {FINANCIAL_DATA['total_revenue_2025']}.",
    "how has net income changed over the last year?": 
        f"The net income has {FINANCIAL_DATA['net_income_change']}.",
    "what is the operating cash flow?": 
        f"The operating cash flow is {FINANCIAL_DATA['operating_cash_flow']}.",
    "what is the gross profit margin?": 
        f"The gross profit margin stands at {FINANCIAL_DATA['gross_profit_margin']}.",
    "what is the revenue growth rate?": 
        f"Revenue showed a {FINANCIAL_DATA['revenue_growth']}."
}