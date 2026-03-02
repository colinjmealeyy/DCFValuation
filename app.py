import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title="DCF Valuation Tool", layout="wide")

st.title("📈 DCF Valuation Tool")
st.markdown("Calculate the intrinsic value of a stock using the Discounted Cash Flow (DCF) method.")

# Sidebar - Inputs
st.sidebar.header("1. Input Parameters")
ticker_input = st.sidebar.text_input("Stock Ticker", value="AAPL").upper()

st.sidebar.header("2. Assumptions")
wacc = st.sidebar.slider("WACC / Discount Rate (%)", 5.0, 20.0, 10.0, step=0.5) / 100.0
revenue_growth_rate = st.sidebar.slider("Revenue Growth Rate (%) (Years 1-5)", -10.0, 50.0, 5.0, step=0.5) / 100.0
terminal_growth_rate = st.sidebar.slider("Terminal Growth Rate (%)", 1.0, 5.0, 2.5, step=0.1) / 100.0
operating_margin = st.sidebar.slider("Operating Margin (%)", 1.0, 50.0, 30.0, step=1.0) / 100.0
tax_rate = st.sidebar.slider("Tax Rate (%)", 0.0, 40.0, 15.0, step=1.0) / 100.0

@st.cache_data
def get_financial_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # We need to extract the most recent year's data for our base year.
        current_revenue = info.get('totalRevenue')
        shares_outstanding = info.get('sharesOutstanding')
        cash = info.get('totalCash') or 0
        debt = info.get('totalDebt') or 0
        current_price = info.get('currentPrice')
        
        # If yf.info fails to fetch some data, try to be safe
        if current_revenue is None and not stock.financials.empty:
            try:
                current_revenue = stock.financials.loc['Total Revenue'].iloc[0]
            except Exception:
                pass

        if shares_outstanding is None:
            shares_outstanding = 1  # Prevent division by zero if completely missing
            
        data = {
            'revenue': current_revenue,
            'shares_outstanding': shares_outstanding,
            'cash': cash,
            'debt': debt,
            'current_price': current_price,
            'company_name': info.get('longName', ticker)
        }
        return data, True
    except Exception as e:
        return str(e), False

data, success = get_financial_data(ticker_input)

if success and data['revenue']:
    # Base Year Data
    current_revenue = data['revenue']
    shares_outstanding = data['shares_outstanding']
    total_cash = data['cash']
    total_debt = data['debt']
    current_price = data['current_price']
    
    st.write(f"### {data['company_name']} ({ticker_input})")
    
    col1, col2, col3, col4 = st.columns(4)
    if current_price:
        col1.metric("Current Price", f"${current_price:.2f}")
    else:
        col1.metric("Current Price", "N/A")
    col2.metric("Base Revenue", f"${current_revenue:,.0f}")
    col3.metric("Total Cash", f"${total_cash:,.0f}")
    col4.metric("Total Debt", f"${total_debt:,.0f}")
    
    # Projections
    years = 5
    projected_revenues = [current_revenue * (1 + revenue_growth_rate)**i for i in range(1, years + 1)]
    projected_ebit = [rev * operating_margin for rev in projected_revenues]
    projected_nopat = [ebit * (1 - tax_rate) for ebit in projected_ebit]
    
    # We use NOPAT as a proxy for Unlevered Free Cash Flow (UFCF) 
    free_cash_flows = projected_nopat
    
    # Discounted Cash Flows
    discount_factors = [1 / ((1 + wacc)**i) for i in range(1, years + 1)]
    pv_fcfs = [fcf * df for fcf, df in zip(free_cash_flows, discount_factors)]
    
    # Terminal Value calculation (Gordon Growth Model)
    # Next year's FCF = Year 5 FCF * (1 + terminal_growth_rate)
    terminal_value = (free_cash_flows[-1] * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
    pv_tv = terminal_value * discount_factors[-1]
    
    # Enterprise to Equity Value Bridge
    enterprise_value = sum(pv_fcfs) + pv_tv
    equity_value = enterprise_value + total_cash - total_debt
    implied_share_price = equity_value / shares_outstanding
    
    st.header("DCF Outputs")
    colA, colB, colC = st.columns(3)
    colA.metric("Enterprise Value", f"${enterprise_value:,.0f}")
    colB.metric("Equity Value", f"${equity_value:,.0f}")
    
    if current_price:
        delta = ((implied_share_price / current_price) - 1) * 100
        colC.metric("Implied Share Price", f"${implied_share_price:.2f}", f"{delta:.1f}% vs Current")
    else:
        colC.metric("Implied Share Price", f"${implied_share_price:.2f}")

    st.subheader("Proj. Cash Flows & Present Value")
    
    df_projections = pd.DataFrame({
        "Revenue": projected_revenues,
        "EBIT": projected_ebit,
        "NOPAT (FCF proxy)": free_cash_flows,
        "Discount Factor": discount_factors,
        "PV of FCF": pv_fcfs
    }, index=[f"Year {i}" for i in range(1, years + 1)])
    
    st.dataframe(df_projections.style.format("{:,.0f}"))
    
    # Sensitivity Analysis
    st.header("Sensitivity Analysis")
    st.markdown("Shows how implied share price changes with different WACC and Growth assumptions.")
    
    # Create ranges for WACC and Growth
    wacc_steps = np.array([-0.02, -0.01, 0.0, 0.01, 0.02])
    growth_steps = np.array([-0.02, -0.01, 0.0, 0.01, 0.02])
    
    wacc_range = wacc + wacc_steps
    growth_range = revenue_growth_rate + growth_steps
    
    sensitivity_table = []
    
    for w in wacc_range:
        row = []
        for g in growth_range:
            # Recalculate
            revs = [current_revenue * (1 + g)**i for i in range(1, years + 1)]
            ebits = [r * operating_margin for r in revs]
            nopats = [eb * (1 - tax_rate) for eb in ebits]
            fcfs = nopats
            
            dfs = [1 / ((1 + w)**i) for i in range(1, years + 1)]
            pvs = [f * d for f, d in zip(fcfs, dfs)]
            
            tv = (fcfs[-1] * (1 + terminal_growth_rate)) / (w - terminal_growth_rate)
            pv_tv_temp = tv * dfs[-1]
            
            ev = sum(pvs) + pv_tv_temp
            eq = ev + total_cash - total_debt
            price = eq / shares_outstanding
            row.append(price)
            
        sensitivity_table.append(row)
        
    df_sens = pd.DataFrame(sensitivity_table, 
                           index=[f"{w*100:.1f}%" for w in wacc_range],
                           columns=[f"{g*100:.1f}%" for g in growth_range])
    
    st.write("**Rows: WACC (%) | Columns: Revenue Growth (%)**")
    
    # Display styled table
    st.dataframe(df_sens.style.background_gradient(cmap='RdYlGn', axis=None).format("${:.2f}"))

else:
    st.error(f"Could not load data for {ticker_input}. Please check the ticker symbol.")
    if not success:
        st.write("Error details:", data)
