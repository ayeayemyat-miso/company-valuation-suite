import streamlit as st
import pandas as pd

st.set_page_config(page_title="User Guide - Valuation Suite", layout="wide")

# ============================================================================
# SIMPLE CSS - FORCES DARK TEXT EVERYWHERE (WORKING VERSION)
# ============================================================================
st.markdown("""
<style>
/* Force ALL text to be dark */
body, .stApp, .main, .stMarkdown, .stText, p, div, span, li, ul, ol, h1, h2, h3, h4, h5, h6 {
    color: #1e293b !important;
}

/* Force bold text to be dark blue */
strong, b {
    color: #0d47a1 !important;
}

/* Make background light green */
.stApp {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
}

/* Card styling with dark text */
.info-card, .success-card, .warning-card {
    background-color: white;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.info-card {
    border-left: 5px solid #2196f3;
}

.success-card {
    border-left: 5px solid #4caf50;
}

.warning-card {
    border-left: 5px solid #ff9800;
}

/* Button styling */
.stButton button {
    background: #0d47a1;
    color: white !important;
}

/* Dataframe styling */
.stDataFrame {
    background-color: white;
}

/* Headers */
h1, h2, h3 {
    color: #0d47a1 !important;
}

/* Blockquote styling */
blockquote {
    background-color: #f0f7ff;
    padding: 10px 15px;
    border-radius: 10px;
    border-left: 4px solid #0d47a1;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.markdown("# 📚 User Guide & Interpretation Guide")
st.markdown("*Learn how to find data, calculate multiples, and interpret valuation results*")
st.markdown("---")

# ============================================================================
# SECTION 1: HOW TO FIND DATA
# ============================================================================
st.markdown("## 🔍 How to Find Financial Data for Any Company")

st.markdown("""
**📊 Best Free Sources:**
- **Yahoo Finance** (finance.yahoo.com) - Most user-friendly
- **SEC EDGAR** (sec.gov/edgar) - Official company filings (10-K, 10-Q)
- **Macrotrends** (macrotrends.net) - Long-term historical data
- **Google Finance** (google.com/finance) - Quick market data
""")

st.markdown("### 📋 Step-by-Step: Finding Data on Yahoo Finance")

st.markdown("""
**Step 1:** Go to **finance.yahoo.com**

**Step 2:** Enter company ticker (e.g., TSLA, AAPL, MSFT)

**Step 3:** Navigate to different sections:
""")

# DataFrame for data sources
data_source_df = pd.DataFrame({
    "Data Point": ["Market Cap", "Shares Outstanding", "Revenue", "EBITDA", "Total Debt", "Cash & Equivalents", "Historical Prices"],
    "Where to Find": ["Key Statistics", "Key Statistics", "Income Statement", "Income Statement", "Balance Sheet", "Balance Sheet", "Historical Data"],
    "Location": [
        "Statistics → Market Cap",
        "Statistics → Shares Outstanding",
        "Financials → Income Statement → Total Revenue",
        "Financials → Income Statement → EBITDA",
        "Financials → Balance Sheet → Total Debt",
        "Financials → Balance Sheet → Cash & Equivalents",
        "Historical Data → Select 1 Year → Download CSV"
    ]
})
st.dataframe(data_source_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================================
# SECTION 2: UNDERSTANDING THE CALCULATIONS
# ============================================================================
st.markdown("## 🧮 Understanding the Calculations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
    **📊 Enterprise Value (EV)**
    
    **Formula:** EV = Market Cap + Total Debt - Cash
    
    **What it means:** The true cost to buy the entire company.
    
    **Why it matters:** Two companies with same market cap can have different EV due to debt.
    
    > 📝 **Note:** This is a simplified EV formula. Professional valuations also include preferred stock and minority interests. For most public companies, the simplified version is sufficient.
    
    🔗 **See the Beginner EV Dashboard** for the full working implementation.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
    **📈 EV / Revenue Multiple**
    
    **Formula:** EV ÷ LTM Revenue
    
    **What it means:** How much you pay for each $1 of sales.
    
    **Best for:** Early-stage, low-profit, or high-growth companies (SaaS, biotech).
    
    > ⚠️ **Limitation:** Does NOT consider profitability.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
    **💰 EV / EBITDA Multiple**
    
    **Formula:** EV ÷ LTM EBITDA
    
    **What it means:** How much you pay for each $1 of operating profit.
    
    **Why preferred:** Removes effects of capital structure, taxes, and depreciation differences.
    
    > ⚠️ **Important:** EBITDA is NOT actual cash flow. It ignores Capital Expenditures (capex) and Working Capital changes.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
    **📉 Discounted Cash Flow (DCF)**
    
    **Formula:** Company Value = Σ(FCF ÷ (1+WACC)^t) + Terminal Value
    
    **Where:**
    - **FCF** = Free Cash Flow (Operating Cash Flow - Capital Expenditures)
    - **WACC** = Weighted Average Cost of Capital (discount rate reflecting risk)
    - **Terminal Value** = Value of cash flows beyond projection period
    
    **Why use it:** Most theoretically sound valuation method.
    
    🔗 **Implementation Note:** This is the conceptual formula. For the complete step-by-step implementation including NOPAT, UFCF, discount factors, PV calculations, and sensitivity analysis, **see the Advanced DCF Dashboard**.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SECTION 3: INDUSTRY BENCHMARKS
# ============================================================================
st.markdown("## 📊 Industry Benchmark Multiples (EV/Revenue)")

st.markdown("""
<div class="warning-card">
**⚠️ Important:** These are GENERAL GUIDELINES only. Actual multiples vary by:
- Market cycles (bull vs bear markets)
- Interest rate environment
- Company-specific growth rates and profitability
- **These ranges change over time**

**What "Cheap" and "Expensive" Mean:**
- **"Cheap"** = Multiple is LOWER than typical range → You pay LESS for each $1 of revenue
- **"Expensive"** = Multiple is HIGHER than typical range → You pay MORE for each $1 of revenue

> ⚠️ **Critical:** "Cheap" does NOT mean "buy immediately." A low multiple may reflect poor growth, high risk, or structural problems. Always investigate WHY.
</div>
""", unsafe_allow_html=True)

benchmark_df = pd.DataFrame({
    "Industry": ["Automotive (Traditional)", "Automotive (EV/New Energy)", "Software / SaaS", "Semiconductors", "Retail (General)", "Biotechnology"],
    "Typical EV/Revenue": ["0.3x - 1.0x", "2x - 8x", "5x - 15x", "3x - 10x", "0.3x - 1.0x", "5x - 30x"],
    "What's Cheap": ["< 0.3x", "< 2x", "< 5x", "< 3x", "< 0.3x", "< 5x"],
    "What's Expensive": ["> 1.5x", "> 10x", "> 20x", "> 12x", "> 1.5x", "> 40x"]
})
st.dataframe(benchmark_df, use_container_width=True, hide_index=True)

st.caption("💡 Always compare to direct competitors for best results. Industry averages are a starting point, not a rule.")

st.markdown("---")

# ============================================================================
# SECTION 4: HOW TO INTERPRET RESULTS
# ============================================================================
st.markdown("## 🎯 How to Determine Undervalued vs Overvalued")

st.markdown("""
<div class="success-card">
**✅ Step-by-Step Interpretation Framework:**

**1. Compare to Direct Competitors**
Use the **Comparable Company Analysis (Comps)** dashboard.
- If your multiple is LOWER than peer average = potentially undervalued
- If HIGHER than peer average = potentially overvalued

**2. Compare to Industry Averages**
Use the benchmark table above.
- Below industry range = cheap (but check why)
- Above industry range = expensive (but check if justified by growth)

**3. Compare to Company's Own History**
Look at 5-year historical multiples (Macrotrends).
- Below historical average = potentially undervalued
- Above historical average = potentially overvalued

**4. Compare DCF Value to Current Price**
Use the **DCF Valuation** dashboard.
- DCF > Current Price = undervalued (consider buying)
- DCF < Current Price = overvalued (consider selling)
- Within ±10% = fairly valued

**5. Consider Qualitative Factors**
- Is the company growing faster than peers? (justifies higher multiple)
- Is there recent bad news? (temporary discount)
- Is the industry out of favor? (opportunity)
- What do analysts say? (check price targets)
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="warning-card">
**⚠️ Critical Warning: Low Multiple Does NOT Automatically Mean "Cheap"**

A stock is NOT undervalued just because its multiple is low. Low multiples may reflect:
- Poor growth prospects
- High risk or excessive debt
- Structural industry problems
- Declining profitability or competitive position
- One-time issues or scandals

**Always investigate WHY the multiple is low before concluding "undervalued."**
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SECTION 5: COMPLETE EXAMPLE (TESLA)
# ============================================================================
st.markdown("## 📝 Complete Example: Valuing Tesla (TSLA)")

st.markdown("**Step 1: Gather Data (from Yahoo Finance - April 2024)**")

tesla_data = pd.DataFrame({
    "Metric": ["Share Price", "Diluted Shares", "Market Cap", "Total Debt", "Cash", "LTM Revenue", "LTM EBITDA"],
    "Value": ["$147.05", "3,179M", "$467,472M", "$0M", "$16,398M", "$96,773M", "$13,558M"]
})
st.dataframe(tesla_data, use_container_width=True, hide_index=True)

st.markdown("""
**Step 2: Calculate Enterprise Value & Multiples**

- EV = $467,472M + $0M - $16,398M = **$451,074M**
- EV/Revenue = $451,074M ÷ $96,773M = **4.66x**
- EV/EBITDA = $451,074M ÷ $13,558M = **33.3x**

**Step 3: Compare to Peers (Apples-to-Apples)**
""")

# Separate peer comparisons
st.markdown("**Auto / EV Peers (Direct Comparison):**")

auto_peers_df = pd.DataFrame({
    "Peer": ["BYD", "General Motors", "Volkswagen"],
    "EV/Revenue": ["4.64x", "0.84x", "0.58x"],
    "EV/EBITDA": ["13.24x", "6.25x", "3.41x"]
})
st.dataframe(auto_peers_df, use_container_width=True, hide_index=True)

st.markdown("""
**Analysis vs Auto Peers:**
- Tesla's 4.66x is **ABOVE** traditional auto (0.5x-1.5x) → premium for growth expectations
- This premium is typical for EV/New Energy companies

**Tech Peers (For Growth Context Only - NOT Direct Comparison):**
""")

tech_peers_df = pd.DataFrame({
    "Peer": ["Nvidia"],
    "EV/Revenue": ["31.02x"],
    "EV/EBITDA": ["53.12x"]
})
st.dataframe(tech_peers_df, use_container_width=True, hide_index=True)

st.markdown("""
> ⚠️ **Note:** Comparing Tesla to Nvidia is NOT an apples-to-apples comparison (different industries). Tech peers are shown ONLY to provide context on growth company valuations.

**Step 4: Final Verdict (April 2024)**

✅ Tesla appears **FAIRLY VALUED to SLIGHTLY OVERVALUED**

- Trading at premium to legacy auto (justified by growth expectations)
- DCF (assuming reasonable growth and WACC) suggests fair value ~$140-150 per share
- Current price ~$147 falls within fair value range

**Conclusion:** HOLD - Wait for pullback to $130-140 for entry
""")

st.markdown("---")

# ============================================================================
# SECTION 6: COMMON MISTAKES TO AVOID
# ============================================================================
st.markdown("## ⚠️ Common Mistakes to Avoid")

mistakes_df = pd.DataFrame({
    "Mistake": [
        "Using Basic Shares Instead of Diluted",
        "Forgetting to Subtract Cash from EV",
        "Comparing Across Industries",
        "Using Trailing vs Forward Incorrectly",
        "Ignoring Growth Rates",
        "One Method is Not Enough",
        "Assuming Low Multiple = Undervalued"
    ],
    "Explanation": [
        "Always use DILUTED shares outstanding. Basic shares understate true equity value.",
        "Cash is non-operating. EV = Market Cap + Debt - Cash. Ignoring cash overstates EV.",
        "Don't compare Tesla to a software company. Different industries have different norms.",
        "LTM = historical last 12 months. FY1 = forward estimates. Don't mix them.",
        "A high multiple might be justified by high growth. Always check growth rates.",
        "Use multiple methods (EV, Comps, DCF) for a complete picture.",
        "A low multiple may reflect risk, weak growth, or structural problems - not just cheap valuation."
    ]
})
st.dataframe(mistakes_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================================
# SECTION 7: QUICK REFERENCE CARD
# ============================================================================
st.markdown("## 📋 Quick Reference Card")

st.markdown("""
<div class="warning-card">
**📊 Valuation Multiples - Typical Ranges (Market-Dependent)**

> ⚠️ These ranges vary by market cycle. Use as general guidance only.
</div>
""", unsafe_allow_html=True)

multiples_ref_df = pd.DataFrame({
    "Multiple": ["EV/Revenue", "EV/EBITDA", "P/E Ratio"],
    "Low (Cheap)": ["< 2x", "< 8x", "< 15x"],
    "Average": ["2x - 8x", "8x - 15x", "15x - 25x"],
    "High (Expensive)": ["> 10x", "> 20x", "> 30x"]
})
st.dataframe(multiples_ref_df, use_container_width=True, hide_index=True)

st.markdown("""
**🎯 Decision Framework:**

| If your multiple is... | Compared to... | Action |
|------------------------|----------------|--------|
| Significantly LOWER | Industry average | 🟢 Investigate why. Could be opportunity OR value trap. |
| AROUND the same | Industry average | 🟡 HOLD / Fairly valued |
| Significantly HIGHER | Industry average | 🔴 Investigate if justified by growth. Could be overvalued. |

**📈 Growth Adjustments:**
- High growth (20%+ revenue growth) → Can justify 2-3x higher multiples
- Low growth (0-5% revenue growth) → Should trade at discount to average

**⚠️ Remember:** A low multiple alone does NOT make a company undervalued. Always investigate the WHY.
""")

st.markdown("---")

# ============================================================================
# SECTION 8: LINKS TO OTHER DASHBOARDS
# ============================================================================
st.markdown("## 🔗 Ready to Value a Company?")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Go to EV Dashboard", key="go_beginner", use_container_width=True):
        st.switch_page("pages/beginner_ev.py")

with col2:
    if st.button("🏢 Go to Comps Dashboard", key="go_intermediate", use_container_width=True):
        st.switch_page("pages/intermediate_comps.py")

with col3:
    if st.button("📈 Go to DCF Dashboard", key="go_advanced", use_container_width=True):
        st.switch_page("pages/advanced_dcf.py")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("💡 **Remember:** Valuation is art + science. No single number is perfect. Use multiple methods and your own judgment.")
st.markdown("*Built with Streamlit • Valuation Suite User Guide*")