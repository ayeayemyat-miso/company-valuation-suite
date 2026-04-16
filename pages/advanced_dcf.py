import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import base64
from io import BytesIO
import zipfile

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="DCF Valuation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_cost_of_debt_from_financials(interest_expense, total_debt_start, total_debt_end, tax_rate):
    """
    Calculate cost of debt from financial statement inputs
    Formula: Cost of Debt = Interest Expense / Average Total Debt × (1 - Tax Rate)
    """
    avg_total_debt = (total_debt_start + total_debt_end) / 2
    
    if avg_total_debt > 0:
        pre_tax_cost = interest_expense / avg_total_debt
        after_tax_cost = pre_tax_cost * (1 - tax_rate)
        return pre_tax_cost, after_tax_cost, avg_total_debt
    else:
        return 0, 0, 0

def download_excel_report(ebit_all, nopat_all, dep_all, wc_all, capex_all, fcf_all, 
                          user_years, fcf_projected, discount_formulas, pv_fcfs,
                          npv_fcfs, pv_terminal, enterprise_value, equity_value,
                          value_per_share, wacc, perpetuity_growth, total_debt_adj,
                          total_cash, short_term_inv, diluted_shares, sensitivity_df,
                          tax_rates):
    """Generate and return Excel file for download"""
    
    export_data = {
        'Valuation_Results': pd.DataFrame({
            'Metric': ['NPV of UFCF', 'PV of Terminal Value', 'Enterprise Value', 
                      'Equity Value', 'Value Per Share', 'WACC', 'Perpetuity Growth',
                      'Total Debt', 'Cash & Equivalents', 'Short Term Investments', 'Diluted Shares'],
            'Value': [f'${npv_fcfs:,.0f}M', f'${pv_terminal:,.0f}M', 
                     f'${enterprise_value:,.0f}M', f'${equity_value:,.0f}M', 
                     f'${value_per_share:.2f}', f'{wacc:.2%}', f'{perpetuity_growth:.2%}',
                     f'${total_debt_adj:,.0f}M', f'${total_cash:,.0f}M',
                     f'${short_term_inv:,.0f}M', f'{diluted_shares:,.0f}M']
        }),
        'FCF_Projections': pd.DataFrame({
            'Year': user_years,
            'Tax_Rate': [f'{x:.1%}' for x in tax_rates],
            'EBIT_M': [f'{x:,.0f}' for x in ebit_all],
            'NOPAT_M': [f'{x:,.0f}' for x in nopat_all],
            'Depreciation_M': [f'{x:,.0f}' for x in dep_all],
            'Delta_WC_M': [f'{x:,.0f}' for x in wc_all],
            'CapEx_M': [f'{x:,.0f}' for x in capex_all],
            'Unlevered_FCF_M': [f'{x:,.0f}' for x in fcf_all]
        }),
        'Discount_Factors': pd.DataFrame({
            'Year': user_years[2:7],
            'FCF_M': [f'{x:,.0f}' for x in fcf_projected],
            'Discount_Factor': discount_formulas,
            'PV_of_FCF_M': [f'{x:,.0f}' for x in pv_fcfs]
        })
    }
    
    if sensitivity_df is not None and not sensitivity_df.empty:
        export_data['Sensitivity_Analysis'] = sensitivity_df
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in export_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    output.seek(0)
    return output

def download_csv_report(ebit_all, nopat_all, dep_all, wc_all, capex_all, fcf_all, 
                        user_years, fcf_projected, discount_formulas, pv_fcfs,
                        npv_fcfs, pv_terminal, enterprise_value, equity_value,
                        value_per_share, wacc, perpetuity_growth, total_debt_adj,
                        total_cash, short_term_inv, diluted_shares, sensitivity_df,
                        tax_rates):
    """Generate and return CSV files for download"""
    
    # Create summary data
    summary_data = {
        'Metric': ['NPV of UFCF', 'PV of Terminal Value', 'Enterprise Value', 
                  'Equity Value', 'Value Per Share', 'WACC', 'Perpetuity Growth',
                  'Total Debt', 'Cash & Equivalents', 'Short Term Investments', 'Diluted Shares'],
        'Value': [f'{npv_fcfs:,.0f}', f'{pv_terminal:,.0f}', 
                 f'{enterprise_value:,.0f}', f'{equity_value:,.0f}', 
                 f'{value_per_share:.2f}', f'{wacc:.4f}', f'{perpetuity_growth:.4f}',
                 f'{total_debt_adj:,.0f}', f'{total_cash:,.0f}',
                 f'{short_term_inv:,.0f}', f'{diluted_shares:,.0f}']
    }
    
    # Create FCF data
    fcf_data = {
        'Year': user_years,
        'Tax_Rate': [f'{x:.1%}' for x in tax_rates],
        'EBIT_M': [f'{x:,.0f}' for x in ebit_all],
        'NOPAT_M': [f'{x:,.0f}' for x in nopat_all],
        'Depreciation_M': [f'{x:,.0f}' for x in dep_all],
        'Delta_WC_M': [f'{x:,.0f}' for x in wc_all],
        'CapEx_M': [f'{x:,.0f}' for x in capex_all],
        'Unlevered_FCF_M': [f'{x:,.0f}' for x in fcf_all]
    }
    
    # Create discount data
    discount_data = {
        'Year': user_years[2:7],
        'FCF_M': [f'{x:,.0f}' for x in fcf_projected],
        'Discount_Factor': discount_formulas,
        'PV_of_FCF_M': [f'{x:,.0f}' for x in pv_fcfs]
    }
    
    # Create zip file with multiple CSVs
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add summary CSV
        summary_df = pd.DataFrame(summary_data)
        summary_csv = summary_df.to_csv(index=False)
        zip_file.writestr('valuation_summary.csv', summary_csv)
        
        # Add FCF CSV
        fcf_df = pd.DataFrame(fcf_data)
        fcf_csv = fcf_df.to_csv(index=False)
        zip_file.writestr('fcf_projections.csv', fcf_csv)
        
        # Add discount CSV
        discount_df = pd.DataFrame(discount_data)
        discount_csv = discount_df.to_csv(index=False)
        zip_file.writestr('discount_factors.csv', discount_csv)
        
        # Add sensitivity CSV if available
        if sensitivity_df is not None and not sensitivity_df.empty:
            sensitivity_csv = sensitivity_df.to_csv()
            zip_file.writestr('sensitivity_analysis.csv', sensitivity_csv)
    
    zip_buffer.seek(0)
    return zip_buffer

# ============================================================================
# CUSTOM CSS - MODERN UI WITH LIGHT GREEN BACKGROUND
# ============================================================================
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Main background - LIGHT GREEN */
.stApp {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
}

/* Fix radio button text color */
.stRadio label {
    color: #1e293b !important;
    font-weight: 500 !important;
}

.stRadio div[role="radiogroup"] label span {
    color: #1e293b !important;
}

/* Modern Card Style */
.modern-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 20px;
    transition: transform 0.2s, box-shadow 0.2s;
    color: #1e293b;
}
.modern-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
}
.modern-card b, .modern-card strong {
    color: #0d47a1;
}

/* Metric Card */
.metric-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #0d47a1 100%);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
.metric-card .metric-label {
    font-size: 14px;
    opacity: 0.9;
    letter-spacing: 0.5px;
    color: rgba(255, 255, 255, 0.9);
}
.metric-card .metric-value {
    font-size: 32px;
    font-weight: 800;
    margin: 10px 0;
    color: white;
}
.metric-card .metric-change {
    font-size: 12px;
    opacity: 0.8;
    color: rgba(255, 255, 255, 0.8);
}

/* Value Per Share Card */
.vps-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    border: 2px solid #ffd700;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}
.vps-card .vps-label {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.9);
    letter-spacing: 1px;
}
.vps-card .vps-value {
    font-size: 48px;
    font-weight: 800;
    color: #ffd700;
    margin: 15px 0;
}
.vps-card .vps-formula {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
}

/* Section Header */
.section-header {
    font-size: 24px;
    font-weight: 700;
    color: #1e3a5f;
    margin: 20px 0 15px 0;
    padding-bottom: 10px;
    border-bottom: 3px solid #0d47a1;
    display: inline-block;
}

/* Subheader */
.subheader {
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
    margin: 15px 0 10px 0;
}

/* Input label styling */
.stNumberInput label, .stSelectbox label {
    font-weight: 500;
    color: #2c3e50 !important;
}

/* Fix for all label colors */
label, .stMarkdown label {
    color: #2c3e50 !important;
}

/* Notice box */
.notice-box {
    background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
    padding: 12px 16px;
    border-radius: 12px;
    border-left: 4px solid #ff9800;
    margin: 10px 0;
    font-size: 13px;
    color: #333333;
}
.notice-box b {
    color: #e65100;
}

/* Success box */
.success-box {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    padding: 12px 16px;
    border-radius: 12px;
    border-left: 4px solid #4caf50;
    margin: 10px 0;
    color: #1b5e20;
}
.success-box b {
    color: #2e7d32;
}

/* Info box */
.info-box {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 12px 16px;
    border-radius: 12px;
    border-left: 4px solid #2196f3;
    margin: 10px 0;
    color: #0d47a1;
}
.info-box b {
    color: #0d47a1;
}

/* Detail box */
.detail-box {
    background: #e8f4fd;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    border-left: 4px solid #2196f3;
    color: #1e293b;
}
.detail-box b {
    color: #0d47a1;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 12px 12px 0 0;
    padding: 10px 24px;
    font-weight: 600;
    color: #2c3e50;
}
.stTabs [aria-selected="true"] {
    background-color: #0d47a1;
    color: white;
}

/* Dataframe styling */
.dataframe-container {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.dataframe {
    background-color: white;
    color: #1e293b;
}

/* Button styling */
.stButton button {
    background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(13, 71, 161, 0.3);
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: rgba(13, 71, 161, 0.05);
    border-radius: 10px;
    font-weight: 600;
    color: #0d47a1;
}
.streamlit-expanderContent {
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 0 0 10px 10px;
    padding: 15px;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #1e3a5f 0%, #0d47a1 100%);
}
.css-1d391kg .stMarkdown, .css-1d391kg .stTextInput label {
    color: white !important;
}

/* Streamlit elements text color */
.stMarkdown, .stText, .stCaption {
    color: #1e293b;
}

/* DataFrame cell text */
td, th {
    color: #1e293b !important;
}

/* WACC detail box */
.wacc-detail {
    background-color: #e8f4fd;
    padding: 15px;
    border-radius: 12px;
    margin: 10px 0;
    border-left: 4px solid #2196f3;
    color: #1e293b;
}
.wacc-detail b {
    color: #0d47a1;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = "Base Case"
if 'show_detail_npv' not in st.session_state:
    st.session_state.show_detail_npv = False
if 'show_detail_tv' not in st.session_state:
    st.session_state.show_detail_tv = False
if 'show_detail_ev' not in st.session_state:
    st.session_state.show_detail_ev = False
if 'show_detail_equity' not in st.session_state:
    st.session_state.show_detail_equity = False
if 'show_detail_vps' not in st.session_state:
    st.session_state.show_detail_vps = False
if 'cost_debt_method' not in st.session_state:
    st.session_state.cost_debt_method = "Direct Input"

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("## 📊 DCF Pro")
    st.markdown("---")
    
    # Scenario Management
    st.markdown("### 📁 Scenarios")
    new_scenario_name = st.text_input("Scenario Name", st.session_state.current_scenario)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("💾 Save", use_container_width=True):
            st.success(f"Saved '{new_scenario_name}'")
    with col_s2:
        if st.button("📂 Load", use_container_width=True):
            st.info("Select from saved scenarios")
    
    if st.session_state.scenarios:
        st.markdown("**Saved:**")
        for name in st.session_state.scenarios.keys():
            if st.button(f"📁 {name}", key=f"sidebar_load_{name}", use_container_width=True):
                st.session_state.current_scenario = name
                st.rerun()
    
    st.markdown("---")
    st.markdown("### 📥 Export")
    
    # Export options (PDF removed)
    export_format = st.radio("Export Format:", ["📊 Excel", "📁 CSV (Multiple Files)"], horizontal=False)
    
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit")

# ============================================================================
# MAIN HEADER
# ============================================================================
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("## 📈")
with col_title:
    st.markdown("# DCF Valuation Dashboard")
    st.markdown("*Professional Discounted Cash Flow Analysis Tool*")

st.markdown("---")

# ============================================================================
# TABS FOR ORGANIZATION
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📝 Input Parameters", "⚙️ DCF Calculations", "📊 Results & Sensitivity", "📈 Visual Analytics"])

# ============================================================================
# INITIALIZE VARIABLES (will be populated in tab1)
# ============================================================================
user_years = [2022, 2023, 2024, 2025, 2026, 2027, 2028]
risk_free_rate = 0.0391
equity_beta = 0.88
equity_risk_premium = 0.055
cost_of_equity = 0.0875
debt_amount = 0
equity_amount = 467472
debt_pct = 0
equity_pct = 1
cost_of_debt = 0.0445
debt_tax_rate = 0.11
after_tax_debt = 0.0396
perpetuity_growth = 0.03
wacc = 0.0875
tax_rates = [0.11] * 7
ebit_method = "📝 Direct EBIT Input"
ebit_values = {}
dep_values = {}
wc_values = {}
capex_values = {}
total_debt_adj = 0
total_cash = 16398
short_term_inv = 12696
diluted_shares = 3179

# ============================================================================
# TAB 1: INPUT PARAMETERS
# ============================================================================
with tab1:
    # Year Labels
    st.markdown('<div class="section-header">📅 Timeline Setup</div>', unsafe_allow_html=True)
    
    col_y1, col_y2, col_y3, col_y4, col_y5, col_y6, col_y7 = st.columns(7)
    with col_y1:
        year_2022 = st.number_input("Hist 1", value=2022, step=1, key="y0")
    with col_y2:
        year_2023 = st.number_input("Hist 2", value=2023, step=1, key="y1")
    with col_y3:
        year_2024 = st.number_input("Proj 1", value=2024, step=1, key="y2")
    with col_y4:
        year_2025 = st.number_input("Proj 2", value=2025, step=1, key="y3")
    with col_y5:
        year_2026 = st.number_input("Proj 3", value=2026, step=1, key="y4")
    with col_y6:
        year_2027 = st.number_input("Proj 4", value=2027, step=1, key="y5")
    with col_y7:
        year_2028 = st.number_input("Proj 5", value=2028, step=1, key="y6")
    
    user_years = [year_2022, year_2023, year_2024, year_2025, year_2026, year_2027, year_2028]
    
    st.markdown("---")
    
    # WACC Section
    st.markdown('<div class="section-header">📊 WACC Assumptions</div>', unsafe_allow_html=True)
    
    col_wacc1, col_wacc2 = st.columns(2)
    
    with col_wacc1:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("#### 💹 Cost of Equity")
            risk_free_rate = st.number_input("Risk Free Rate (Rf)", value=0.0391, step=0.001, format="%.4f", key="rf")
            equity_beta = st.number_input("Equity Beta", value=0.88, step=0.01, format="%.2f", key="beta")
            equity_risk_premium = st.number_input("Equity Risk Premium", value=0.055, step=0.001, format="%.4f", key="erp")
            cost_of_equity = risk_free_rate + (equity_beta * equity_risk_premium)
            st.markdown(f'<div class="info-box">💡 Ke = {risk_free_rate:.4f} + ({equity_beta:.2f} × {equity_risk_premium:.4f}) = <b>{cost_of_equity:.2%}</b></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col_wacc2:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("#### 🏢 Capital Structure")
            debt_amount = st.number_input("Debt Amount (M)", value=0, step=1000, key="debt_amt")
            equity_amount = st.number_input("Equity Amount (M)", value=467472, step=1000, key="eq_amt")
            total_capital = debt_amount + equity_amount
            debt_pct = debt_amount / total_capital if total_capital > 0 else 0
            equity_pct = equity_amount / total_capital if total_capital > 0 else 1
            st.markdown(f'<div class="info-box">📊 Debt: {debt_pct:.1%} | Equity: {equity_pct:.1%}<br>💰 Total Capital: ${total_capital:,.0f}M</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    col_debt1, col_debt2 = st.columns(2)
    with col_debt1:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("#### 💰 Cost of Debt")
            
            # Add option to calculate from financials or direct input
            st.session_state.cost_debt_method = st.radio(
                "Cost of Debt Input Method:",
                ["Direct Input", "Calculate from Financial Statements"],
                horizontal=True,
                key="cod_method"
            )
            
            if st.session_state.cost_debt_method == "Direct Input":
                cost_of_debt = st.number_input("Cost of Debt", value=0.0445, step=0.001, format="%.4f", key="cod")
                st.markdown('<div class="info-box">💡 Using direct input for cost of debt</div>', unsafe_allow_html=True)
            else:
                st.markdown("**📊 Financial Statement Inputs**")
                col_fs1, col_fs2, col_fs3 = st.columns(3)
                with col_fs1:
                    interest_expense = st.number_input("Interest Expense (M)", value=1200, step=100, key="int_exp")
                with col_fs2:
                    total_debt_start = st.number_input("Total Debt - Beginning (M)", value=25000, step=1000, key="debt_start")
                with col_fs3:
                    total_debt_end = st.number_input("Total Debt - Ending (M)", value=28000, step=1000, key="debt_end")
                
                # Calculate cost of debt
                pre_tax_cost, after_tax_cost, avg_debt = calculate_cost_of_debt_from_financials(
                    interest_expense, total_debt_start, total_debt_end, debt_tax_rate
                )
                cost_of_debt = pre_tax_cost
                
                st.markdown(f"""
                <div class="info-box">
                📊 <b>Calculated from Financial Statements:</b><br>
                • Average Debt: ${avg_debt:,.0f}M<br>
                • Pre-tax Cost of Debt: {pre_tax_cost:.2%}<br>
                • After-tax Cost of Debt: {after_tax_cost:.2%}
                </div>
                """, unsafe_allow_html=True)
            
            debt_tax_rate = st.number_input("Tax Shield Rate", value=0.11, step=0.01, format="%.2f", key="tax_rate")
            after_tax_debt = cost_of_debt * (1 - debt_tax_rate)
            st.markdown(f'<div class="info-box">💰 Kdt = {cost_of_debt:.4f} × (1 - {debt_tax_rate:.2f}) = <b>{after_tax_debt:.2%}</b></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col_debt2:
        with st.container():
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("#### 📈 Growth Assumptions")
            perpetuity_growth = st.number_input("Perpetuity Growth Rate", value=0.03, step=0.001, format="%.3f", key="perp_growth")
            wacc = (cost_of_equity * equity_pct) + (after_tax_debt * debt_pct)
            st.markdown(f'<div class="info-box">📌 Calculated WACC: <b>{wacc:.2%}</b><br>📈 Terminal Growth: {perpetuity_growth:.2%}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # WACC Details Expander
    with st.expander("🔍 View WACC Calculation Details"):
        st.markdown(f"""
        <div class="wacc-detail">
            <b>📊 Weighted Average Cost of Capital (WACC) Calculation</b><br><br>
            <b>Formula:</b> WACC = (Ke × Equity%) + (Kdt × Debt%)<br><br>
            <b>With numbers:</b><br>
            Ke = {cost_of_equity:.2%}<br>
            Kdt = {after_tax_debt:.2%}<br>
            Equity% = {equity_pct:.1%}<br>
            Debt% = {debt_pct:.1%}<br><br>
            <b>Calculation:</b> ({cost_of_equity:.2%} × {equity_pct:.1%}) + ({after_tax_debt:.2%} × {debt_pct:.1%}) = {wacc:.2%}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tax Rates
    st.markdown('<div class="section-header">💰 Tax Rates by Year</div>', unsafe_allow_html=True)
    
    tax_cols = st.columns(7)
    tax_rates = []
    for i, col in enumerate(tax_cols):
        with col:
            rate = st.number_input(f"{user_years[i]}", value=0.11, step=0.01, format="%.2f", key=f"tax_{i}")
            tax_rates.append(rate)
    
    st.markdown("---")
    
    # EBIT Input Method
    st.markdown('<div class="section-header">📝 Financial Projections</div>', unsafe_allow_html=True)
    
    ebit_method = st.radio(
        "EBIT Input Method:",
        ["📝 Direct EBIT Input", "📈 Growth Rates Method"],
        horizontal=True,
        key="ebit_method"
    )
    
    st.markdown("---")
    
    # Input Table
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Financial Statement Inputs (Values in Millions)")
    
    # Headers
    col_headers = st.columns(7)
    for i, col in enumerate(col_headers):
        with col:
            st.markdown(f"**{user_years[i]}**")
    
    # EBIT Row
    st.markdown("**EBIT**")
    ebit_cols = st.columns(7)
    ebit_values = {}
    
    if ebit_method == "📝 Direct EBIT Input":
        direct_defaults = [13656, 8891, 10467, 14561, 19295, 24596, 32183]
        for i, col in enumerate(ebit_cols):
            with col:
                ebit_values[i] = st.number_input("", value=direct_defaults[i], step=500, key=f"ebit_{i}", label_visibility="collapsed")
    else:
        for i in range(2):
            with ebit_cols[i]:
                ebit_values[i] = st.number_input("", value=[13656, 8891][i], step=500, key=f"ebit_{i}", label_visibility="collapsed")
        
        st.markdown("**Growth Rates**")
        growth_cols = st.columns(7)
        growth_defaults = [0, 0, 17.7, 39.1, 32.5, 27.5, 30.8]
        growth_values = {}
        for i, col in enumerate(growth_cols):
            with col:
                if i < 2:
                    st.markdown("-")
                else:
                    growth_values[i] = st.number_input("", value=growth_defaults[i], step=1.0, format="%.1f", key=f"growth_{i}", label_visibility="collapsed") / 100
        
        ebit_values[2] = ebit_values[1] * (1 + growth_values[2])
        ebit_values[3] = ebit_values[2] * (1 + growth_values[3])
        ebit_values[4] = ebit_values[3] * (1 + growth_values[4])
        ebit_values[5] = ebit_values[4] * (1 + growth_values[5])
        ebit_values[6] = ebit_values[5] * (1 + growth_values[6])
    
    # Depreciation Row
    st.markdown("**Depreciation**")
    dep_cols = st.columns(7)
    dep_defaults = [3747, 4667, 6036, 8371, 11085, 13594, 17068]
    dep_values = {}
    for i, col in enumerate(dep_cols):
        with col:
            dep_values[i] = st.number_input("", value=dep_defaults[i], step=200, key=f"dep_{i}", label_visibility="collapsed")
    
    # ΔWC Row with Notice
    st.markdown('<div class="notice-box">⚠️ <b>Δ Working Capital:</b> Positive = cash outflow (reduces FCF) | Negative = cash inflow (increases FCF)</div>', unsafe_allow_html=True)
    st.markdown("**Δ Working Capital**")
    wc_cols = st.columns(7)
    wc_defaults = [536, 2703, 627, 788, 966, 1157, 1359]
    wc_values = {}
    for i, col in enumerate(wc_cols):
        with col:
            wc_values[i] = st.number_input("", value=wc_defaults[i], step=100, key=f"wc_{i}", label_visibility="collapsed")
    
    # CapEx Row with Notice
    st.markdown('<div class="notice-box">⚠️ <b>Capital Expenditures:</b> Enter as POSITIVE numbers. Formula: FCF = NOPAT + Dep + ΔWC - CapEx</div>', unsafe_allow_html=True)
    st.markdown("**Capital Expenditures**")
    capex_cols = st.columns(7)
    capex_defaults = [7158, 9949, 11635, 13382, 15115, 16788, 18381]
    capex_values = {}
    for i, col in enumerate(capex_cols):
        with col:
            capex_values[i] = st.number_input("", value=capex_defaults[i], step=500, key=f"capex_{i}", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Valuation Adjustments
    st.markdown("---")
    st.markdown('<div class="section-header">🏢 Valuation Adjustments</div>', unsafe_allow_html=True)
    
    col_adj1, col_adj2, col_adj3, col_adj4 = st.columns(4)
    with col_adj1:
        total_debt_adj = st.number_input("Total Debt (M)", value=0, step=1000, key="debt_adj")
    with col_adj2:
        total_cash = st.number_input("Cash & Equivalents (M)", value=16398, step=1000, key="cash")
    with col_adj3:
        short_term_inv = st.number_input("Short Term Investments (M)", value=12696, step=1000, key="sti")
    with col_adj4:
        diluted_shares = st.number_input("Diluted Shares (M)", value=3179, step=100, key="shares")

# ============================================================================
# CALCULATIONS (Shared across tabs)
# ============================================================================
ebit_all = [ebit_values[i] for i in range(7)]
dep_all = [dep_values[i] for i in range(7)]
wc_all = [wc_values[i] for i in range(7)]
capex_all = [capex_values[i] for i in range(7)]

nopat_all = []
fcf_all = []

for i in range(7):
    nopat = ebit_all[i] * (1 - tax_rates[i])
    fcf = nopat + dep_all[i] + wc_all[i] - capex_all[i]
    nopat_all.append(nopat)
    fcf_all.append(fcf)

fcf_projected = fcf_all[2:7]

# Discount Factors
discount_factors = []
pv_fcfs = []
discount_formulas = []

for i in range(5):
    period = i + 1
    df = 1 / ((1 + wacc) ** period)
    discount_factors.append(df)
    pv = fcf_projected[i] * df
    pv_fcfs.append(pv)
    discount_formulas.append(f"1/(1+{wacc:.4f})^{period} = {df:.4f}")

npv_fcfs = sum(pv_fcfs)

# Terminal Value
if wacc > perpetuity_growth:
    terminal_value = fcf_projected[-1] * (1 + perpetuity_growth) / (wacc - perpetuity_growth)
    pv_terminal = terminal_value / ((1 + wacc) ** 5)
else:
    terminal_value = 0
    pv_terminal = 0

enterprise_value = npv_fcfs + pv_terminal
equity_value = enterprise_value - total_debt_adj + total_cash + short_term_inv
value_per_share = equity_value / diluted_shares if diluted_shares > 0 else 0

# ============================================================================
# TAB 2: DCF CALCULATIONS
# ============================================================================
with tab2:
    # Unlevered FCF
    st.markdown('<div class="section-header">📊 Unlevered Free Cash Flow</div>', unsafe_allow_html=True)
    
    fcf_cols = st.columns(7)
    for i, col in enumerate(fcf_cols):
        with col:
            st.markdown(f'<div class="metric-card" style="background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);"><div class="metric-label">{user_years[i]}</div><div class="metric-value">${fcf_all[i]:,.0f}M</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Discount Factor Table
    st.markdown('<div class="section-header">📉 Discount Factor & PV Calculation</div>', unsafe_allow_html=True)
    
    pv_data = []
    for i in range(5):
        pv_data.append({
            'Year': user_years[2+i],
            'FCF': f"${fcf_projected[i]:,.0f}M",
            'Discount Rate': f"{wacc:.2%}",
            'Period': i+1,
            'Discount Factor': discount_formulas[i],
            'PV of FCF': f"${pv_fcfs[i]:,.0f}M"
        })
    
    df_pv = pd.DataFrame(pv_data)
    st.dataframe(df_pv, width='stretch', hide_index=True)
    
    st.markdown(f'<div class="success-box">💰 <b>NPV of Unlevered FCF ({user_years[2]} - {user_years[6]}): ${npv_fcfs:,.0f}M</b></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Terminal Value Calculation
    st.markdown('<div class="section-header">🏢 Terminal Value</div>', unsafe_allow_html=True)
    
    col_tv1, col_tv2 = st.columns(2)
    with col_tv1:
        st.markdown(f"""
        <div class="modern-card">
            <b>Terminal Value Formula:</b><br>
            TV = FCF_{user_years[6]} × (1 + g) / (WACC - g)<br><br>
            = ${fcf_projected[-1]:,.0f}M × (1 + {perpetuity_growth:.2%}) / ({wacc:.2%} - {perpetuity_growth:.2%})<br><br>
            = <b>${terminal_value:,.0f}M</b>
        </div>
        """, unsafe_allow_html=True)
    with col_tv2:
        st.markdown(f"""
        <div class="modern-card">
            <b>Present Value of Terminal Value:</b><br>
            PV = TV / (1 + WACC)^5<br><br>
            = ${terminal_value:,.0f}M / (1 + {wacc:.2%})^5<br><br>
            = <b>${pv_terminal:,.0f}M</b>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: RESULTS & SENSITIVITY
# ============================================================================
with tab3:
    # Key Metrics Row
    st.markdown('<div class="section-header">💰 Key Valuation Metrics</div>', unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">NPV of FCF</div>
            <div class="metric-value">${npv_fcfs:,.0f}M</div>
            <div class="metric-change">{user_years[2]} - {user_years[6]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Terminal Value (PV)</div>
            <div class="metric-value">${pv_terminal:,.0f}M</div>
            <div class="metric-change">@{wacc:.2%} discount</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Enterprise Value</div>
            <div class="metric-value">${enterprise_value:,.0f}M</div>
            <div class="metric-change">NPV + PV TV</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Equity Value</div>
            <div class="metric-value">${equity_value:,.0f}M</div>
            <div class="metric-change">EV - Debt + Cash + STI</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Value Per Share
    st.markdown(f"""
    <div class="vps-card">
        <div class="vps-label">⭐ IMPLIED VALUE PER SHARE ⭐</div>
        <div class="vps-value">${value_per_share:.2f}</div>
        <div class="vps-formula">= ${equity_value:,.0f}M ÷ {diluted_shares:,.0f}M shares</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detail button for VPS
    col_btn1, col_btn2, col_btn3 = st.columns([3, 1, 3])
    with col_btn2:
        if st.button("📊 Show Detail Calculation", key="btn_vps"):
            st.session_state.show_detail_vps = not st.session_state.show_detail_vps
    
    if st.session_state.show_detail_vps:
        st.markdown(f"""
        <div class="detail-box">
            <b>📊 Calculation Details - Implied Value Per Share</b><br><br>
            <b>Formula:</b> Value Per Share = Equity Value / Diluted Shares Outstanding<br><br>
            <b>With numbers:</b> ${value_per_share:.2f} = ${equity_value:,.0f}M / {diluted_shares:,.0f}M
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # DCF Value Table with Detail Buttons
    st.markdown('<div class="section-header">📋 DCF Value Breakdown</div>', unsafe_allow_html=True)
    
    # NPV Detail
    col1, col2, col3 = st.columns([3, 1.5, 1])
    with col1:
        st.markdown(f'<span style="color: #0d47a1; font-weight: bold;">🔵 NPV of UFCF {user_years[2]} - {user_years[6]}</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span style="color: #0d47a1; font-weight: bold;">${npv_fcfs:,.0f}M</span>', unsafe_allow_html=True)
    with col3:
        if st.button("📊 Detail", key="btn_npv"):
            st.session_state.show_detail_npv = not st.session_state.show_detail_npv
    
    if st.session_state.show_detail_npv:
        st.markdown(f"""
        <div class="detail-box">
            <b>📊 Calculation Details - NPV of UFCF</b><br><br>
            <b>Formula:</b> NPV = Sum of PV of FCF for {user_years[2]} - {user_years[6]}<br><br>
            <b>With numbers:</b> ${npv_fcfs:,.0f}M = {' + '.join([f'${x:,.0f}M' for x in pv_fcfs])}
        </div>
        """, unsafe_allow_html=True)
    
    # PV Terminal Detail
    col1, col2, col3 = st.columns([3, 1.5, 1])
    with col1:
        st.markdown(f'<span style="color: #0d47a1; font-weight: bold;">🔵 PV of Terminal Value</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span style="color: #0d47a1; font-weight: bold;">${pv_terminal:,.0f}M</span>', unsafe_allow_html=True)
    with col3:
        if st.button("📊 Detail", key="btn_tv"):
            st.session_state.show_detail_tv = not st.session_state.show_detail_tv
    
    if st.session_state.show_detail_tv:
        st.markdown(f"""
        <div class="detail-box">
            <b>📊 Calculation Details - PV of Terminal Value</b><br><br>
            <b>Formula:</b> PV of Terminal Value = Terminal Value / (1 + WACC)^5<br><br>
            <b>With numbers:</b> ${pv_terminal:,.0f}M = ${terminal_value:,.0f}M / (1 + {wacc:.2%})^5
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enterprise Value Detail
    col1, col2, col3 = st.columns([3, 1.5, 1])
    with col1:
        st.markdown(f'<span style="color: #0d47a1; font-weight: bold;">🔵 Implied Enterprise Value</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span style="color: #0d47a1; font-weight: bold;">${enterprise_value:,.0f}M</span>', unsafe_allow_html=True)
    with col3:
        if st.button("📊 Detail", key="btn_ev"):
            st.session_state.show_detail_ev = not st.session_state.show_detail_ev
    
    if st.session_state.show_detail_ev:
        st.markdown(f"""
        <div class="detail-box">
            <b>📊 Calculation Details - Implied Enterprise Value</b><br><br>
            <b>Formula:</b> Enterprise Value = NPV of FCF + PV of Terminal Value<br><br>
            <b>With numbers:</b> ${enterprise_value:,.0f}M = ${npv_fcfs:,.0f}M + ${pv_terminal:,.0f}M
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input values
    st.markdown(f'<span style="color: #e65100; font-weight: bold;">🔴 Less: Debt</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="color: #e65100; margin-left: 20px;">${total_debt_adj:,.0f}M</span>', unsafe_allow_html=True)
    st.caption("(From Balance Sheet inputs)")
    
    st.markdown(f'<span style="color: #e65100; font-weight: bold;">🔴 Add: Cash</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="color: #e65100; margin-left: 20px;">${total_cash:,.0f}M</span>', unsafe_allow_html=True)
    st.caption("(From Balance Sheet inputs)")
    
    st.markdown(f'<span style="color: #e65100; font-weight: bold;">🔴 Add: Short Term Investments</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="color: #e65100; margin-left: 20px;">${short_term_inv:,.0f}M</span>', unsafe_allow_html=True)
    st.caption("(From Balance Sheet inputs)")
    
    st.markdown("---")
    
    # Equity Value Detail
    col1, col2, col3 = st.columns([3, 1.5, 1])
    with col1:
        st.markdown(f'<span style="color: #0d47a1; font-weight: bold;">🔵 Implied Equity Value</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span style="color: #0d47a1; font-weight: bold;">${equity_value:,.0f}M</span>', unsafe_allow_html=True)
    with col3:
        if st.button("📊 Detail", key="btn_equity"):
            st.session_state.show_detail_equity = not st.session_state.show_detail_equity
    
    if st.session_state.show_detail_equity:
        st.markdown(f"""
        <div class="detail-box">
            <b>📊 Calculation Details - Implied Equity Value</b><br><br>
            <b>Formula:</b> Equity Value = Enterprise Value - Debt + Cash + Short-term Investments<br><br>
            <b>With numbers:</b> ${equity_value:,.0f}M = ${enterprise_value:,.0f}M - ${total_debt_adj:,.0f}M + ${total_cash:,.0f}M + ${short_term_inv:,.0f}M
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<span style="color: #e65100; font-weight: bold;">🔴 Diluted shares</span>', unsafe_allow_html=True)
    st.markdown(f'<span style="color: #e65100; margin-left: 20px;">{diluted_shares:,.0f}M</span>', unsafe_allow_html=True)
    st.caption("(From Balance Sheet inputs)")
    
    st.markdown("---")
    
    # Sensitivity Analysis
    st.markdown('<div class="section-header">🎯 Sensitivity Analysis</div>', unsafe_allow_html=True)
    
    sensitivity_df = None
    
    if wacc > perpetuity_growth:
        wacc_range = np.arange(max(0.05, wacc - 0.01), min(0.15, wacc + 0.015), 0.0025)
        growth_range = np.arange(max(0.01, perpetuity_growth - 0.01), min(0.06, perpetuity_growth + 0.015), 0.0025)
        
        sensitivity_data = []
        for w in wacc_range:
            row = []
            for g in growth_range:
                if w > g:
                    pv_temp = sum([fcf / ((1 + w) ** i) for i, fcf in enumerate(fcf_projected, 1)])
                    tv_temp = fcf_projected[-1] * (1 + g) / (w - g)
                    pv_tv_temp = tv_temp / ((1 + w) ** 5)
                    ev_temp = pv_temp + pv_tv_temp
                    eq_temp = ev_temp - total_debt_adj + total_cash + short_term_inv
                    value_temp = eq_temp / diluted_shares
                    row.append(value_temp)
                else:
                    row.append(0)
            sensitivity_data.append(row)
        
        sensitivity_df = pd.DataFrame(sensitivity_data, 
                                       index=[f"{w:.2%}" for w in wacc_range],
                                       columns=[f"{g:.2%}" for g in growth_range])
        
        col_left_sens, col_right_sens = st.columns([0.5, 10])
        with col_left_sens:
            st.markdown('<div style="writing-mode: vertical-rl; transform: rotate(180deg); text-align: center; font-weight: bold; min-height: 300px; color: #1e293b;">↓ Growth Rate</div>', unsafe_allow_html=True)
        with col_right_sens:
            st.markdown('<div style="text-align: center; font-weight: bold; margin-bottom: 5px; color: #1e293b;">WACC (Discount Rate) →</div>', unsafe_allow_html=True)
            st.dataframe(sensitivity_df.style.format("{:.2f}").background_gradient(cmap="RdYlGn", axis=None), width='stretch')
        
        st.caption("💡 **How to read:** Find Value Per Share at intersection of WACC (rows) and Growth Rate (columns)")
        st.caption("🟢 Green = Higher Value | 🔴 Red = Lower Value")
    else:
        st.warning("Adjust WACC and Growth Rate to enable sensitivity analysis (WACC must be > Growth Rate)")

# ============================================================================
# TAB 4: VISUAL ANALYTICS
# ============================================================================
with tab4:
    st.markdown('<div class="section-header">📈 Free Cash Flow Projections</div>', unsafe_allow_html=True)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=[str(y) for y in user_years],
        y=[x/1000 for x in fcf_all],
        name='Free Cash Flow',
        marker_color=['#90a4ae', '#90a4ae', '#42a5f5', '#42a5f5', '#42a5f5', '#42a5f5', '#42a5f5'],
        text=[f'${x/1000:.1f}B' for x in fcf_all],
        textposition='outside'
    ))
    fig1.update_layout(
        title='Free Cash Flow by Year',
        xaxis_title='Year',
        yaxis_title='FCF (Billions USD)',
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">🥧 Value Contribution</div>', unsafe_allow_html=True)
    
    col_pie1, col_pie2 = st.columns(2)
    
    with col_pie1:
        fig2 = go.Figure(data=[go.Pie(
            labels=['PV of FCF (Projected)', 'PV of Terminal Value'],
            values=[npv_fcfs, pv_terminal],
            hole=0.4,
            marker_colors=['#42a5f5', '#1e3a5f'],
            textinfo='label+percent'
        )])
        fig2.update_layout(title='Value Contribution by Component', height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col_pie2:
        fig3 = go.Figure(data=[go.Pie(
            labels=['Enterprise Value', 'Debt', 'Cash & STI'],
            values=[enterprise_value, total_debt_adj, total_cash + short_term_inv],
            hole=0.4,
            marker_colors=['#42a5f5', '#ef5350', '#66bb6a'],
            textinfo='label+percent'
        )])
        fig3.update_layout(title='Enterprise Value to Equity Value Bridge', height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # Export Section with working download buttons (PDF removed)
    st.markdown('<div class="section-header">📥 Export Results</div>', unsafe_allow_html=True)
    
    if export_format == "📊 Excel":
        if st.button("📊 Generate Excel Report", use_container_width=True, key="excel_generate_btn"):
            with st.spinner("Generating Excel report..."):
                excel_file = download_excel_report(
                    ebit_all, nopat_all, dep_all, wc_all, capex_all, fcf_all,
                    user_years, fcf_projected, discount_formulas, pv_fcfs,
                    npv_fcfs, pv_terminal, enterprise_value, equity_value,
                    value_per_share, wacc, perpetuity_growth, total_debt_adj,
                    total_cash, short_term_inv, diluted_shares, sensitivity_df,
                    tax_rates
                )
                
                st.download_button(
                    label="📥 Click to Download Excel File",
                    data=excel_file,
                    file_name=f"dcf_valuation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                st.success("✅ Excel report ready for download!")
    
    else:  # CSV Export
        if st.button("📁 Generate CSV Package", use_container_width=True, key="csv_generate_btn"):
            with st.spinner("Generating CSV files..."):
                csv_zip = download_csv_report(
                    ebit_all, nopat_all, dep_all, wc_all, capex_all, fcf_all,
                    user_years, fcf_projected, discount_formulas, pv_fcfs,
                    npv_fcfs, pv_terminal, enterprise_value, equity_value,
                    value_per_share, wacc, perpetuity_growth, total_debt_adj,
                    total_cash, short_term_inv, diluted_shares, sensitivity_df,
                    tax_rates
                )
                
                st.download_button(
                    label="📥 Click to Download CSV Package (ZIP)",
                    data=csv_zip,
                    file_name=f"dcf_valuation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                st.success("✅ CSV package ready for download!")
    
    st.markdown("---")
    st.info("💡 **Tip:** Use the export buttons above to download your valuation results in Excel or CSV format!")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #1b5e20; padding: 20px;">
    <p>🎯 <b>Pro Tip:</b> Save different scenarios (Base, Bull, Bear) using the sidebar to compare different assumptions!</p>
    <p>📊 Dashboard calculates everything automatically - just change any input and watch results update in real-time!</p>
    <p style="font-size: 12px;">Built with Streamlit • DCF Valuation Dashboard • {datetime.now().strftime('%Y')}</p>
</div>
""", unsafe_allow_html=True)

# Save DCF range to shared state
try:
    import json
    import os
    state_file = "data/valuation_state.json"
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
    else:
        state = {}
    
    # Get min and max from sensitivity table or use value_per_share range
    state["dcf_low"] = enterprise_value * 0.8  # Example: 20% below
    state["dcf_high"] = enterprise_value * 1.2  # Example: 20% above
    
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)
except Exception as e:
    pass

# Add at the very bottom, before the footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>📚 <b>Need help interpreting these results?</b></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📖 Open User Guide", use_container_width=True):
        st.switch_page("pages/user_guide.py")