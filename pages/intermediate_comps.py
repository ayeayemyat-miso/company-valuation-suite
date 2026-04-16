import streamlit as st
import pandas as pd
import numpy as np
import statistics
from io import StringIO

st.set_page_config(page_title="Comparable Company Analysis", layout="wide")

# ============================================================================
# CUSTOM CSS - MATCHING BEGINNER DASHBOARD
# ============================================================================
st.markdown("""
<style>
/* Main background - LIGHT GREEN */
.stApp {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
}

/* ========== SIDEBAR STYLING (WHITE TEXT) ========== */
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
.css-1d391kg .stSuccess,
[data-testid="stSidebar"] .stSuccess {
    color: #c8e6c9 !important;
}
.css-1d391kg .stButton button p,
[data-testid="stSidebar"] .stButton button p {
    color: white !important;
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

/* Value Card */
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

/* Section Header */
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

/* Success Box */
.success-box {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    padding: 12px 16px;
    border-radius: 12px;
    border-left: 4px solid #4caf50;
    margin: 10px 0;
    color: #1b5e20;
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

/* Headers */
h1, h2, h3, h4 {
    color: #0d47a1;
}

/* Dataframe */
.stDataFrame {
    background-color: white;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("## 🏢")
with col_title:
    st.markdown('<h1 style="color: #0d47a1;">Comparable Company Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #1e293b; font-size: 16px;"><i>Value any company using peer multiples</i></p>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# INITIALIZE SESSION STATE WITH DEFAULT SAMPLE DATA
# ============================================================================
def get_default_peers():
    """Return default sample peer data"""
    return [
        {
            "Company Name": "BYD (Sample)",
            "Market Cap (M)": 80840,
            "Total Debt (M)": 15000,
            "Cash (M)": 12000,
            "LTM Revenue (M)": 96773,
            "LTM EBITDA (M)": 13558,
            "Enterprise Value (M)": 80840 + 15000 - 12000,  # 83840
            "EV/Rev LTM": (80840 + 15000 - 12000) / 96773,
            "EV/EBITDA LTM": (80840 + 15000 - 12000) / 13558
        },
        {
            "Company Name": "General Motors (Sample)",
            "Market Cap (M)": 48910,
            "Total Debt (M)": 145100,
            "Cash (M)": 25000,
            "LTM Revenue (M)": 156000,
            "LTM EBITDA (M)": 22000,
            "Enterprise Value (M)": 48910 + 145100 - 25000,  # 169010
            "EV/Rev LTM": (48910 + 145100 - 25000) / 156000,
            "EV/EBITDA LTM": (48910 + 145100 - 25000) / 22000
        }
    ]

def get_default_target():
    """Return default sample target company data"""
    return {
        "Company Name": "Tesla Inc (Sample)",
        "LTM Revenue (M)": 96773,
        "LTM EBITDA (M)": 13558
    }

# Initialize session state
if "manual_peers" not in st.session_state:
    st.session_state.manual_peers = get_default_peers()

if "target_company" not in st.session_state:
    st.session_state.target_company = get_default_target()

# ============================================================================
# SIDEBAR - PEER DATA INPUT METHODS
# ============================================================================
with st.sidebar:
    st.markdown("## 📊 Peer Data Input")
    st.markdown("---")
    
    # Display current peer count
    st.markdown(f"**Current Peers:** {len(st.session_state.manual_peers)} companies")
    
    st.markdown("---")
    
    input_method = st.radio(
        "Choose input method:",
        ["✏️ Manual Entry (Add/Edit Peers)", "📁 Upload CSV File"],
        horizontal=False
    )
    
    st.markdown("---")
    
    # ========================================================================
    # MANUAL ENTRY FORM (ALWAYS VISIBLE)
    # ========================================================================
    st.markdown("### ➕ Add New Peer")
    
    with st.form("add_peer_form"):
        company_name = st.text_input("Company Name", key="new_peer_name")
        
        col1, col2 = st.columns(2)
        with col1:
            market_cap = st.number_input("Market Cap (M)", value=0, step=1000, key="new_mc")
            total_debt = st.number_input("Total Debt (M)", value=0, step=1000, key="new_debt")
            cash = st.number_input("Cash (M)", value=0, step=1000, key="new_cash")
        with col2:
            revenue = st.number_input("LTM Revenue (M)", value=0, step=1000, key="new_rev")
            ebitda = st.number_input("LTM EBITDA (M)", value=0, step=1000, key="new_ebitda")
        
        submitted = st.form_submit_button("➕ Add Peer Company")
        
        if submitted and company_name:
            ev = market_cap + total_debt - cash
            ev_rev = ev / revenue if revenue > 0 else 0
            ev_ebitda = ev / ebitda if ebitda > 0 else 0
            
            st.session_state.manual_peers.append({
                "Company Name": company_name,
                "Market Cap (M)": market_cap,
                "Total Debt (M)": total_debt,
                "Cash (M)": cash,
                "LTM Revenue (M)": revenue,
                "LTM EBITDA (M)": ebitda,
                "Enterprise Value (M)": ev,
                "EV/Rev LTM": ev_rev,
                "EV/EBITDA LTM": ev_ebitda
            })
            st.success(f"✅ Added {company_name}")
            st.rerun()
    
    st.markdown("---")
    
    # ========================================================================
    # CSV UPLOAD
    # ========================================================================
    if input_method == "📁 Upload CSV File":
        st.markdown("### 📁 Upload CSV")
        st.markdown("Required columns:")
        st.caption("Company Name, Market Cap (M), Total Debt (M), Cash (M), LTM Revenue (M), LTM EBITDA (M)")
        
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                required_cols = ["Company Name", "Market Cap (M)", "Total Debt (M)", "Cash (M)", "LTM Revenue (M)", "LTM EBITDA (M)"]
                
                if all(col in df.columns for col in required_cols):
                    # Clear existing and add from CSV
                    new_peers = []
                    for _, row in df.iterrows():
                        ev = row["Market Cap (M)"] + row["Total Debt (M)"] - row["Cash (M)"]
                        ev_rev = ev / row["LTM Revenue (M)"] if row["LTM Revenue (M)"] > 0 else 0
                        ev_ebitda = ev / row["LTM EBITDA (M)"] if row["LTM EBITDA (M)"] > 0 else 0
                        
                        new_peers.append({
                            "Company Name": row["Company Name"],
                            "Market Cap (M)": row["Market Cap (M)"],
                            "Total Debt (M)": row["Total Debt (M)"],
                            "Cash (M)": row["Cash (M)"],
                            "LTM Revenue (M)": row["LTM Revenue (M)"],
                            "LTM EBITDA (M)": row["LTM EBITDA (M)"],
                            "Enterprise Value (M)": ev,
                            "EV/Rev LTM": ev_rev,
                            "EV/EBITDA LTM": ev_ebitda
                        })
                    
                    st.session_state.manual_peers = new_peers
                    st.success(f"✅ Loaded {len(new_peers)} peers from CSV")
                    st.rerun()
                else:
                    st.error(f"Missing columns. Need: {required_cols}")
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    st.markdown("---")
    
    # ========================================================================
    # MANAGE PEERS
    # ========================================================================
    st.markdown("### 🗑️ Manage Peers")
    
    if st.button("🗑️ Delete All Peers", use_container_width=True):
        st.session_state.manual_peers = []
        st.success("Deleted all peers")
        st.rerun()
    
    if st.button("📋 Reset to Sample Peers (2 companies)", use_container_width=True):
        st.session_state.manual_peers = get_default_peers()
        st.success("Reset to sample peers")
        st.rerun()

# ============================================================================
# FUNCTIONS
# ============================================================================
def calculate_peer_stats(peers_df):
    """Calculate High, Mean, Median, Low for each multiple"""
    stats = {}
    
    for multiple in ["EV/Rev LTM", "EV/EBITDA LTM"]:
        values = peers_df[multiple].dropna().tolist()
        if values and len(values) >= 2:
            stats[multiple] = {
                "High": max(values),
                "Mean": sum(values) / len(values),
                "Median": statistics.median(values),
                "Low": min(values)
            }
        else:
            stats[multiple] = {"High": 0, "Mean": 0, "Median": 0, "Low": 0}
    
    return stats

def value_target_company(target_metrics, peer_stats):
    """Apply peer multiples to target company"""
    valuations = {}
    
    valuations["Based on EV/Revenue LTM"] = {
        "High": target_metrics["LTM Revenue"] * peer_stats["EV/Rev LTM"]["High"],
        "Mean": target_metrics["LTM Revenue"] * peer_stats["EV/Rev LTM"]["Mean"],
        "Median": target_metrics["LTM Revenue"] * peer_stats["EV/Rev LTM"]["Median"],
        "Low": target_metrics["LTM Revenue"] * peer_stats["EV/Rev LTM"]["Low"]
    }
    
    valuations["Based on EV/EBITDA LTM"] = {
        "High": target_metrics["LTM EBITDA"] * peer_stats["EV/EBITDA LTM"]["High"],
        "Mean": target_metrics["LTM EBITDA"] * peer_stats["EV/EBITDA LTM"]["Mean"],
        "Median": target_metrics["LTM EBITDA"] * peer_stats["EV/EBITDA LTM"]["Median"],
        "Low": target_metrics["LTM EBITDA"] * peer_stats["EV/EBITDA LTM"]["Low"]
    }
    
    return valuations

# ============================================================================
# MAIN DISPLAY
# ============================================================================
if st.session_state.manual_peers:
    peers_df = pd.DataFrame(st.session_state.manual_peers)
    
    # ========================================================================
    # PEER TABLE WITH EDIT/DELETE
    # ========================================================================
    st.markdown('<div class="section-header">📊 Peer Companies</div>', unsafe_allow_html=True)
    
    # Display peer table with edit/delete options
    for i, peer in enumerate(st.session_state.manual_peers):
        with st.expander(f"✏️ Edit: {peer['Company Name']}"):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                new_name = st.text_input("Company Name", value=peer["Company Name"], key=f"name_{i}")
                new_mc = st.number_input("Market Cap (M)", value=peer["Market Cap (M)"], step=1000, key=f"mc_{i}")
                new_debt = st.number_input("Total Debt (M)", value=peer["Total Debt (M)"], step=1000, key=f"debt_{i}")
                new_cash = st.number_input("Cash (M)", value=peer["Cash (M)"], step=1000, key=f"cash_{i}")
                new_rev = st.number_input("LTM Revenue (M)", value=peer["LTM Revenue (M)"], step=1000, key=f"rev_{i}")
                new_ebitda = st.number_input("LTM EBITDA (M)", value=peer["LTM EBITDA (M)"], step=1000, key=f"ebitda_{i}")
            
            with col2:
                if st.button("💾 Save", key=f"save_{i}"):
                    ev = new_mc + new_debt - new_cash
                    ev_rev = ev / new_rev if new_rev > 0 else 0
                    ev_ebitda = ev / new_ebitda if new_ebitda > 0 else 0
                    
                    st.session_state.manual_peers[i] = {
                        "Company Name": new_name,
                        "Market Cap (M)": new_mc,
                        "Total Debt (M)": new_debt,
                        "Cash (M)": new_cash,
                        "LTM Revenue (M)": new_rev,
                        "LTM EBITDA (M)": new_ebitda,
                        "Enterprise Value (M)": ev,
                        "EV/Rev LTM": ev_rev,
                        "EV/EBITDA LTM": ev_ebitda
                    }
                    st.success(f"Saved {new_name}")
                    st.rerun()
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    st.session_state.manual_peers.pop(i)
                    st.success(f"Deleted {peer['Company Name']}")
                    st.rerun()
    
    # Display summary table
    st.markdown('<div class="section-header">📋 Peer Summary</div>', unsafe_allow_html=True)
    
    display_cols = ["Company Name", "Market Cap (M)", "Enterprise Value (M)", "EV/Rev LTM", "EV/EBITDA LTM"]
    st.dataframe(peers_df[display_cols].style.format({
        "Market Cap (M)": "${:,.0f}M",
        "Enterprise Value (M)": "${:,.0f}M",
        "EV/Rev LTM": "{:.2f}x",
        "EV/EBITDA LTM": "{:.2f}x"
    }), use_container_width=True, hide_index=True)
    
    # ========================================================================
    # PEER SELECTION FOR ANALYSIS
    # ========================================================================
    st.markdown('<div class="section-header">✅ Select Peers for Analysis</div>', unsafe_allow_html=True)
    
    all_peers = peers_df["Company Name"].tolist()
    selected_peers = []
    
    cols = st.columns(4)
    for i, peer in enumerate(all_peers):
        with cols[i % 4]:
            default_selected = True if len(all_peers) <= 5 else False
            if st.checkbox(peer, value=default_selected, key=f"select_{peer}"):
                selected_peers.append(peer)
    
    if len(selected_peers) >= 2:
        st.markdown(f'<div class="success-box">✅ Selected {len(selected_peers)} peers for analysis</div>', unsafe_allow_html=True)
        
        # Filter selected peers
        filtered_df = peers_df[peers_df["Company Name"].isin(selected_peers)]
        
        # Calculate statistics
        stats = calculate_peer_stats(filtered_df)
        
        # Display statistics table
        st.markdown('<div class="section-header">📈 Peer Multiples Statistics</div>', unsafe_allow_html=True)
        
        stats_data = []
        for multiple, values in stats.items():
            stats_data.append({
                "Multiple": multiple,
                "High": f"{values['High']:.2f}x",
                "Mean": f"{values['Mean']:.2f}x",
                "Median": f"{values['Median']:.2f}x",
                "Low": f"{values['Low']:.2f}x"
            })
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        # ====================================================================
        # TARGET COMPANY INPUT
        # ====================================================================
        st.markdown('<div class="section-header">🎯 Company You Want to Value</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_name = st.text_input("Company Name", value=st.session_state.target_company["Company Name"])
            target_ltm_revenue = st.number_input("LTM Revenue ($M)", value=st.session_state.target_company["LTM Revenue (M)"], step=1000)
        
        with col2:
            target_ltm_ebitda = st.number_input("LTM EBITDA ($M)", value=st.session_state.target_company["LTM EBITDA (M)"], step=500)
        
        # Save target to session state
        st.session_state.target_company = {
            "Company Name": target_name,
            "LTM Revenue (M)": target_ltm_revenue,
            "LTM EBITDA (M)": target_ltm_ebitda
        }
        
        target_metrics = {
            "LTM Revenue": target_ltm_revenue,
            "LTM EBITDA": target_ltm_ebitda
        }
        
        # Calculate valuations
        valuations = value_target_company(target_metrics, stats)
        
        # ====================================================================
        # VALUATION RESULTS
        # ====================================================================
        st.markdown(f'<div class="section-header">💰 Implied Enterprise Value for {target_name}</div>', unsafe_allow_html=True)
        
        for method, values in valuations.items():
            st.markdown(f"""
            <div class="modern-card">
                <b style="color: #0d47a1; font-size: 18px;">{method}</b><br>
                <table style="width: 100%; margin-top: 10px;">
                    <tr>
                        <td><b>High:</b></td>
                        <td style="color: #0d47a1; font-weight: 800;">${values['High']:,.0f}M</td>
                        <td><b>Mean:</b></td>
                        <td style="color: #0d47a1; font-weight: 800;">${values['Mean']:,.0f}M</td>
                    </tr>
                    <tr>
                        <td><b>Median:</b></td>
                        <td style="color: #0d47a1; font-weight: 800;">${values['Median']:,.0f}M</td>
                        <td><b>Low:</b></td>
                        <td style="color: #0d47a1; font-weight: 800;">${values['Low']:,.0f}M</td>
                    </tr>
                 </table>
            </div>
            """, unsafe_allow_html=True)
        
        # ====================================================================
        # DETAILED CALCULATIONS EXPANDER
        # ====================================================================
        with st.expander("🔍 View Detailed Calculations"):
            st.markdown("### How Peer Multiples Are Calculated")
            st.markdown("""
            **For each peer company:**
            
            | Calculation | Formula |
            |-------------|---------|
            | Enterprise Value (EV) | Market Cap + Total Debt - Cash |
            | EV/Revenue | Enterprise Value ÷ LTM Revenue |
            | EV/EBITDA | Enterprise Value ÷ LTM EBITDA |
            """)
            
            st.markdown(f"### How {target_name} Is Valued")
            st.markdown(f"""
            **Formula:** Implied EV = Peer Multiple × {target_name}'s Financial Metric
            
            **Example using Median multiples:**
            - EV/Revenue LTM Median: {stats['EV/Rev LTM']['Median']:.2f}x × ${target_ltm_revenue:,}M = **${valuations['Based on EV/Revenue LTM']['Median']:,.0f}M**
            - EV/EBITDA LTM Median: {stats['EV/EBITDA LTM']['Median']:.2f}x × ${target_ltm_ebitda:,}M = **${valuations['Based on EV/EBITDA LTM']['Median']:,.0f}M**
            """)
            
            # Show individual peer calculations
            st.markdown("### Individual Peer Calculations")
            calc_data = []
            for _, row in filtered_df.iterrows():
                calc_data.append({
                    "Company": row["Company Name"],
                    "Market Cap": f"${row['Market Cap (M)']:,.0f}M",
                    "Total Debt": f"${row['Total Debt (M)']:,.0f}M",
                    "Cash": f"${row['Cash (M)']:,.0f}M",
                    "EV": f"${row['Enterprise Value (M)']:,.0f}M",
                    "EV/Rev": f"{row['EV/Rev LTM']:.2f}x",
                    "EV/EBITDA": f"{row['EV/EBITDA LTM']:.2f}x"
                })
            st.dataframe(pd.DataFrame(calc_data), use_container_width=True, hide_index=True)
        
    else:
        st.markdown(f'<div class="warning-box">⚠️ Please select at least 2 peers for meaningful statistics. Currently selected: {len(selected_peers)}</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="info-box">💡 No peers added yet. Use the sidebar to add peer companies via manual entry or CSV upload.</div>', unsafe_allow_html=True)
    
    with st.expander("📖 Quick Start Guide"):
        st.markdown("""
        ### Try the Sample Data
        Click **"Reset to Sample Peers"** in the sidebar to load 2 example companies (BYD and General Motors).
        
        ### Then:
        1. Select both peers using checkboxes
        2. Enter your target company's revenue and EBITDA
        3. See the valuation results instantly!
        
        ### To analyze your own companies:
        - **Edit** existing peers by clicking the expander and modifying values
        - **Add** new peers using the form in sidebar
        - **Delete** unwanted peers
        - **Upload CSV** for bulk import
        """)

# Save comps range to shared state
try:
    import json
    import os
    # Load existing
    state_file = "data/valuation_state.json"
    os.makedirs("data", exist_ok=True)
    
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
    else:
        state = {}
    
    # Find min and max from valuations
    all_values = []
    for method, values in valuations.items():
        all_values.extend([values["Low"], values["High"]])
    
    state["comps_low"] = min(all_values)
    state["comps_high"] = max(all_values)
    
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)
except Exception as e:
    pass

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p style="color: #1b5e20;">💡 <b>Pro Tip:</b> Use 5-10 comparable companies for best results. Exclude outliers with unusually high/low multiples.</p>
    <p style="font-size: 12px; color: #1b5e20;">Built with Streamlit • Comparable Company Analysis Dashboard</p>
</div>
""", unsafe_allow_html=True)
# Add at the very bottom, before the footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>📚 <b>Need help interpreting these results?</b></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📖 Open User Guide", use_container_width=True):
        st.switch_page("pages/user_guide.py")