import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="Enterprise Value Dashboard", layout="wide")

# ============================================================================
# CUSTOM CSS - LIGHT GREEN BACKGROUND WITH DARK TEXT IN MAIN CONTENT ONLY
# ============================================================================
st.markdown("""
<style>
/* Main background - LIGHT GREEN */
.stApp {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
}

/* ========== SIDEBAR STYLING (ORIGINAL - WHITE TEXT) ========== */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a5f 0%, #0d47a1 100%);
}
.css-1d391kg .stMarkdown, 
.css-1d391kg label, 
.css-1d391kg p,
.css-1d391kg .stTextInput label,
.css-1d391kg .stNumberInput label,
.css-1d391kg .stSelectbox label,
.css-1d391kg .stRadio label,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: white !important;
}
.css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: white !important;
}
.css-1d391kg .stRadio div[role="radiogroup"] label span,
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span {
    color: white !important;
}
.css-1d391kg .stSuccess,
[data-testid="stSidebar"] .stSuccess {
    color: #c8e6c9 !important;
}

/* ========== MAIN CONTENT STYLING (DARK TEXT) ========== */
.stMarkdown, .stText, .stCaption, p, span, div {
    color: #1e293b;
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
.modern-card span {
    color: #1e293b;
}

/* Metric Card - Dark background for contrast */
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
    color: white;
}
.metric-card .metric-value {
    font-size: 28px;
    font-weight: 800;
    margin: 10px 0;
    color: white;
}
.metric-card .metric-sub {
    font-size: 12px;
    opacity: 0.8;
    color: white;
}

/* Value Card - Dark background */
.value-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #0d47a1 100%);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}
.value-card .value-label {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.9);
}
.value-card .value-number {
    font-size: 42px;
    font-weight: 800;
    color: #ffd700;
    margin: 15px 0;
}
.value-card .value-formula {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
}

/* Section Header - Dark blue text */
.section-header {
    font-size: 24px;
    font-weight: 700;
    color: #0d47a1;
    margin: 20px 0 15px 0;
    padding-bottom: 10px;
    border-bottom: 3px solid #0d47a1;
    display: inline-block;
}

/* Info Box */
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

/* Warning Box */
.warning-box {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    padding: 12px 16px;
    border-radius: 12px;
    border-left: 4px solid #ff9800;
    margin: 10px 0;
    color: #e65100;
}
.warning-box b {
    color: #e65100;
}

/* Success Box */
.success-box {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    padding: 12px 16px;
    border-radius: 12px;
    border-left: 4px solid #4caf50;
    margin: 10px 0;
    color: #1b5e20;
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
    color: #1e293b;
}
.stTabs [aria-selected="true"] {
    background-color: #0d47a1;
    color: white;
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

/* Headers in main content */
h1, h2, h3, h4 {
    color: #0d47a1;
}

/* Dataframe */
.stDataFrame {
    background-color: white;
    border-radius: 12px;
}

/* Number input in main content (not sidebar) */
div:not(.css-1d391kg) .stNumberInput label,
div:not([data-testid="stSidebar"]) .stNumberInput label {
    color: #1e293b !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("## 📊")
with col_title:
    st.markdown('<h1 style="color: #0d47a1;">Enterprise Value & Multiples Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #1e293b; font-size: 16px;"><i>Professional valuation tool for any public company</i></p>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("## ⚙️ Input Parameters")
    st.markdown("---")
    
    ticker = st.text_input("📌 Company Ticker", "TSLA").upper()
    
    st.markdown("### 💰 Capital Structure")
    diluted_shares = st.number_input("Diluted Shares (millions)", value=3179, step=10)
    total_debt = st.number_input("Total Debt ($M)", value=0, step=1000)
    cash = st.number_input("Cash & Equivalents ($M)", value=16398, step=1000)
    cash_equiv = st.number_input("Other Cash Equivalents ($M)", value=12696, step=1000)
    
    st.markdown("### 📈 Financial Metrics")
    ltm_revenue = st.number_input("LTM Revenue ($M)", value=96773, step=1000)
    fy1_revenue = st.number_input("FY1 Revenue ($M)", value=113026, step=1000)
    ltm_ebitda = st.number_input("LTM EBITDA ($M)", value=13558, step=500)
    fy1_ebitda = st.number_input("FY1 EBITDA ($M)", value=16490, step=500)
    
    st.markdown("### 📅 Price Data Source")
    data_source = st.radio("Choose:", ["Auto-fetch from Yahoo Finance", "Upload CSV"])

# ============================================================================
# FUNCTIONS
# ============================================================================
def calculate_ev(share_price, diluted_shares, total_debt, cash, cash_equiv):
    equity_value = share_price * diluted_shares
    ev = equity_value + total_debt - cash - cash_equiv
    return ev, equity_value

def calculate_multiples(ev, ltm_rev, fy1_rev, ltm_ebitda, fy1_ebitda):
    return {
        "EV / LTM Revenue": ev / ltm_rev if ltm_rev else 0,
        "EV / FY1 Revenue": ev / fy1_rev if fy1_rev else 0,
        "EV / LTM EBITDA": ev / ltm_ebitda if ltm_ebitda else 0,
        "EV / FY1 EBITDA": ev / fy1_ebitda if fy1_ebitda else 0,
    }

# ============================================================================
# DATA LOADING WITH RATE LIMIT HANDLING
# ============================================================================
price_data = None
error_message = None

if data_source == "Auto-fetch from Yahoo Finance":
    if ticker:
        with st.spinner(f"Fetching 52-week data for {ticker}..."):
            try:
                stock = yf.Ticker(ticker)
                end_date = datetime.today()
                start_date = end_date - timedelta(days=400)
                hist = stock.history(start=start_date, end=end_date)
                if not hist.empty:
                    hist = hist.reset_index()
                    hist = hist[["Date", "Close", "Volume"]].copy()
                    hist["Date"] = pd.to_datetime(hist["Date"]).dt.date
                    price_data = hist
                    st.sidebar.success(f"✅ Fetched {len(price_data)} days")
                else:
                    error_message = "No data found for this ticker"
                    st.sidebar.error(error_message)
            except Exception as e:
                error_msg = str(e)
                if "RateLimit" in error_msg or "YFRateLimitError" in error_msg:
                    error_message = "Yahoo Finance rate limit reached. Please use CSV upload or wait a few minutes."
                    st.sidebar.markdown(f"""
                    <div class="warning-box">
                    ⚠️ **Rate Limit Reached**<br><br>
                    Too many requests. Please use <b>CSV Upload</b> instead or wait a few minutes.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    error_message = f"Error: {error_msg[:100]}"
                    st.sidebar.error(error_message)
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV (Date, Close, Volume)", type="csv")
    if uploaded_file:
        try:
            price_data = pd.read_csv(uploaded_file)
            price_data["Date"] = pd.to_datetime(price_data["Date"]).dt.date
            st.sidebar.success(f"✅ Uploaded {len(price_data)} rows")
        except Exception as e:
            error_message = f"Error reading CSV: {e}"
            st.sidebar.error(error_message)

# ============================================================================
# MAIN DISPLAY
# ============================================================================
if price_data is not None and not price_data.empty:
    close_prices = price_data["Close"]
    high_price = close_prices.max()
    low_price = close_prices.min()
    avg_price = close_prices.mean()
    
    most_recent_date = price_data["Date"].max()
    most_recent_row = price_data[price_data["Date"] == most_recent_date].iloc[0]
    current_price = most_recent_row["Close"]
    
    st.markdown(f'<div class="info-box">📅 Using most recent date: <b>{most_recent_date}</b> | Closing Price: <b>${current_price:.2f}</b></div>', unsafe_allow_html=True)
    
    # Calculate EVs
    current_ev, current_equity = calculate_ev(current_price, diluted_shares, total_debt, cash, cash_equiv)
    high_ev, high_equity = calculate_ev(high_price, diluted_shares, total_debt, cash, cash_equiv)
    low_ev, low_equity = calculate_ev(low_price, diluted_shares, total_debt, cash, cash_equiv)
    avg_ev, _ = calculate_ev(avg_price, diluted_shares, total_debt, cash, cash_equiv)
    
    multiples = calculate_multiples(current_ev, ltm_revenue, fy1_revenue, ltm_ebitda, fy1_ebitda)
    
    # ========================================================================
    # VALUE CARD
    # ========================================================================
    st.markdown(f"""
    <div class="value-card">
        <div class="value-label">⭐ CURRENT ENTERPRISE VALUE ⭐</div>
        <div class="value-number">${current_ev:,.0f}M</div>
        <div class="value-formula">= ${current_price:.2f} × {diluted_shares:,}M + ${total_debt:,.0f}M - ${cash + cash_equiv:,.0f}M</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # TWO COLUMN LAYOUT
    # ========================================================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">🏢 Enterprise Value</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="modern-card">
            <b style="color: #0d47a1; font-size: 18px;">📊 Current EV</b><br>
            <span style="font-size: 32px; font-weight: 800; color: #0d47a1;">${current_ev:,.0f}M</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="modern-card">
            <b style="color: #0d47a1; font-size: 18px;">📈 52-Week Range</b><br>
            <span style="color: #1e293b;">High: <b style="color: #0d47a1;">${high_ev:,.0f}M</b></span><br>
            <span style="color: #1e293b;">Low: <b style="color: #0d47a1;">${low_ev:,.0f}M</b></span><br>
            <span style="color: #1e293b;">Average: <b style="color: #0d47a1;">${avg_ev:,.0f}M</b></span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="modern-card">
            <b style="color: #0d47a1; font-size: 18px;">💰 Equity Value</b><br>
            <span style="font-size: 24px; font-weight: 700; color: #0d47a1;">${current_equity:,.0f}M</span><br>
            <span style="font-size: 12px; color: #1e293b;">= ${current_price:.2f} × {diluted_shares:,}M shares</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-header">📊 Valuation Multiples</div>', unsafe_allow_html=True)
        
        for name, value in multiples.items():
            st.markdown(f"""
            <div class="modern-card">
                <b style="color: #0d47a1; font-size: 16px;">{name}</b><br>
                <span style="font-size: 28px; font-weight: 800; color: #0d47a1;">{value:.2f}x</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # PRICE STATISTICS
    # ========================================================================
    st.markdown('<div class="section-header">📅 52-Week Price Statistics</div>', unsafe_allow_html=True)
    
    price_stats = pd.DataFrame({
        "Metric": ["Current", "High", "Low", "Average"],
        "Share Price ($)": [f"${current_price:.2f}", f"${high_price:.2f}", f"${low_price:.2f}", f"${avg_price:.2f}"]
    })
    st.dataframe(price_stats, hide_index=True, use_container_width=True)
    
    # ========================================================================
    # DETAILED CALCULATIONS EXPANDER
    # ========================================================================
    with st.expander("🔍 View Detailed EV Calculation"):
        st.markdown(f"""
        **Enterprise Value Formula:**  
        `EV = (Share Price × Diluted Shares) + Total Debt - Cash - Cash Equivalents`
        
        **Step-by-step calculation:**
        
        | Component | Value | Calculation |
        |-----------|-------|-------------|
        | Share Price | ${current_price:.2f} | Most recent close |
        | Diluted Shares | {diluted_shares:,}M | User input |
        | **Equity Value** | **${current_equity:,.0f}M** | {current_price:.2f} × {diluted_shares:,} |
        | + Total Debt | ${total_debt:,.0f}M | User input |
        | - Cash | ${cash:,.0f}M | User input |
        | - Cash Equivalents | ${cash_equiv:,.0f}M | User input |
        | **= Enterprise Value** | **${current_ev:,.0f}M** | |
        """)
        
        st.markdown(f"""
        **52-Week High EV Calculation:**  
        ${high_price:.2f} × {diluted_shares:,}M + ${total_debt:,.0f}M - ${cash + cash_equiv:,.0f}M = **${high_ev:,.0f}M**
        
        **52-Week Low EV Calculation:**  
        ${low_price:.2f} × {diluted_shares:,}M + ${total_debt:,.0f}M - ${cash + cash_equiv:,.0f}M = **${low_ev:,.0f}M**
        """)
    
    with st.expander("🔍 View Detailed Multiples Calculation"):
        st.markdown(f"""
        **Multiples Formula:** `Multiple = Enterprise Value ÷ Financial Metric`
        
        | Multiple | Formula | Result |
        |----------|---------|--------|
        | EV / LTM Revenue | ${current_ev:,.0f}M ÷ ${ltm_revenue:,}M | **{multiples['EV / LTM Revenue']:.2f}x** |
        | EV / FY1 Revenue | ${current_ev:,.0f}M ÷ ${fy1_revenue:,}M | **{multiples['EV / FY1 Revenue']:.2f}x** |
        | EV / LTM EBITDA | ${current_ev:,.0f}M ÷ ${ltm_ebitda:,}M | **{multiples['EV / LTM EBITDA']:.2f}x** |
        | EV / FY1 EBITDA | ${current_ev:,.0f}M ÷ ${fy1_ebitda:,}M | **{multiples['EV / FY1 EBITDA']:.2f}x** |
        """)
    
    # ========================================================================
    # SAVE TO SHARED STATE (INSIDE THE IF BLOCK - AFTER VARIABLES ARE DEFINED)
    # ========================================================================
    try:
        save_data = {}
        save_data["ev_52wk_low"] = float(low_ev)
        save_data["ev_52wk_high"] = float(high_ev)
        save_data["current_ev"] = float(current_ev)
        
        os.makedirs("data", exist_ok=True)
        with open("data/valuation_state.json", "w") as f:
            json.dump(save_data, f, indent=2)
    except Exception as e:
        pass

else:
    st.markdown("""
    <div class="warning-box">
    ⚠️ **No price data available**<br><br>
    Please use one of these options:<br>
    1. **Auto-fetch**: Wait a minute and try again (Yahoo Finance has rate limits)<br>
    2. **CSV Upload**: Upload your own 52-week price data
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p style="color: #1b5e20;">💡 <b>Pro Tip:</b> Use CSV upload if auto-fetch fails due to rate limits</p>
    <p style="font-size: 12px; color: #1b5e20;">Built with Streamlit • Enterprise Value Dashboard</p>
</div>
""", unsafe_allow_html=True)

# User Guide Link
st.markdown("<div style='text-align: center;'>📚 <b>Need help interpreting these results?</b></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📖 Open User Guide", use_container_width=True):
        st.switch_page("pages/user_guide.py")