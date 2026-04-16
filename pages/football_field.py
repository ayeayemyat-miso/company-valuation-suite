import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="Football Field - Valuation Ranges", layout="wide")

# ============================================================================
# CUSTOM CSS - MATCHING OTHER DASHBOARDS
# ============================================================================
st.markdown("""
<style>
/* Main background - LIGHT GREEN */
.stApp {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
}

/* Force ALL text to be dark */
body, .stApp, .main, .stMarkdown, .stText, p, div, span, li, ul, ol, h1, h2, h3, h4, h5, h6 {
    color: #1e293b !important;
}

/* Force bold text to be dark blue */
strong, b {
    color: #0d47a1 !important;
}

/* Section Header */
.section-header {
    font-size: 28px;
    font-weight: 700;
    color: #0d47a1;
    margin: 30px 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 3px solid #0d47a1;
    display: inline-block;
}

/* Card styling */
.info-card, .success-card, .warning-card, .verdict-card {
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

.verdict-card {
    border-left: 5px solid #0d47a1;
}

/* Button styling */
.stButton button {
    background: #0d47a1;
    color: white !important;
}

/* Headers */
h1, h2, h3 {
    color: #0d47a1 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FILE PATHS
# ============================================================================
DATA_DIR = "data"
STATE_FILE = f"{DATA_DIR}/valuation_state.json"

def load_state():
    """Load valuation state from JSON file with proper error handling"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    for key, value in data.items():
                        if isinstance(value, (int, float)):
                            data[key] = float(value)
                    return data
                else:
                    return {}
        else:
            return {}
    except json.JSONDecodeError:
        return {}
    except Exception as e:
        return {}

def save_state(data):
    """Save valuation state to JSON file"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        return False

# ============================================================================
# HEADER
# ============================================================================
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("## 🎯")
with col_title:
    st.markdown("# Football Field - Valuation Ranges")
    st.markdown("*Compare valuation ranges from all methods*")

st.markdown("---")

# ============================================================================
# LOAD SAVED STATE
# ============================================================================
saved_state = load_state()

# Default values (as floats to avoid type errors)
DEFAULT_EV_LOW = 438378.0
DEFAULT_EV_HIGH = 903434.0
DEFAULT_COMPS_LOW = 56128.0
DEFAULT_COMPS_HIGH = 1280306.0
DEFAULT_DCF_LOW = 500000.0
DEFAULT_DCF_HIGH = 900000.0
DEFAULT_CURRENT_EV = 438378.0

if saved_state:
    saved_ev_low = float(saved_state.get("ev_52wk_low", DEFAULT_EV_LOW))
    saved_ev_high = float(saved_state.get("ev_52wk_high", DEFAULT_EV_HIGH))
    saved_comps_low = float(saved_state.get("comps_low", DEFAULT_COMPS_LOW))
    saved_comps_high = float(saved_state.get("comps_high", DEFAULT_COMPS_HIGH))
    saved_dcf_low = float(saved_state.get("dcf_low", DEFAULT_DCF_LOW))
    saved_dcf_high = float(saved_state.get("dcf_high", DEFAULT_DCF_HIGH))
    saved_current_ev = float(saved_state.get("current_ev", DEFAULT_CURRENT_EV))
    
    st.success("✅ Loaded saved results from Beginner, Comps, and DCF dashboards!")
else:
    saved_ev_low = DEFAULT_EV_LOW
    saved_ev_high = DEFAULT_EV_HIGH
    saved_comps_low = DEFAULT_COMPS_LOW
    saved_comps_high = DEFAULT_COMPS_HIGH
    saved_dcf_low = DEFAULT_DCF_LOW
    saved_dcf_high = DEFAULT_DCF_HIGH
    saved_current_ev = DEFAULT_CURRENT_EV
    
    st.info("📝 No saved results found. Use manual inputs below or run the other dashboards and save your results.")

# ============================================================================
# MANUAL INPUT SECTION
# ============================================================================
st.markdown("## 📝 Manual Input (or use saved results)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Enterprise Value Range (Beginner)**")
    ev_low = st.number_input("52-Week Low EV ($M)", value=saved_ev_low, step=10000.0, key="ev_low")
    ev_high = st.number_input("52-Week High EV ($M)", value=saved_ev_high, step=10000.0, key="ev_high")

with col2:
    st.markdown("**Comps Analysis Range (Intermediate)**")
    comps_low = st.number_input("Comps Low EV ($M)", value=saved_comps_low, step=10000.0, key="comps_low")
    comps_high = st.number_input("Comps High EV ($M)", value=saved_comps_high, step=10000.0, key="comps_high")

st.markdown("**DCF Range (Advanced)**")
dcf_low = st.number_input("DCF Low EV ($M)", value=saved_dcf_low, step=10000.0, key="dcf_low")
dcf_high = st.number_input("DCF High EV ($M)", value=saved_dcf_high, step=10000.0, key="dcf_high")

current_ev = st.number_input("Current EV for Reference ($M)", value=saved_current_ev, step=10000.0, key="current_ev")

# Save manual inputs button
if st.button("💾 Save Current Inputs", use_container_width=True):
    save_data = {
        "ev_52wk_low": float(ev_low),
        "ev_52wk_high": float(ev_high),
        "comps_low": float(comps_low),
        "comps_high": float(comps_high),
        "dcf_low": float(dcf_low),
        "dcf_high": float(dcf_high),
        "current_ev": float(current_ev)
    }
    if save_state(save_data):
        st.success("✅ Inputs saved successfully!")
    else:
        st.error("❌ Failed to save inputs")

st.markdown("---")

# ============================================================================
# FOOTBALL CHART
# ============================================================================
if st.button("🎯 Generate Football Field", use_container_width=True, type="primary"):
    methods = ["52-Week EV", "Comps Analysis", "DCF Model"]
    lows = [float(ev_low), float(comps_low), float(dcf_low)]
    highs = [float(ev_high), float(comps_high), float(dcf_high)]
    midpoints = [(l + h) / 2 for l, h in zip(lows, highs)]
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, (method, low, high, mid, color) in enumerate(zip(methods, lows, highs, midpoints, colors)):
        fig.add_trace(go.Bar(
            name=method,
            y=[method],
            x=[high - low],
            base=low,
            orientation='h',
            marker=dict(color=color, opacity=0.7),
            text=f"${mid:,.0f}M",
            textposition='inside',
            hovertemplate=f"{method}<br>Low: ${low:,.0f}M<br>High: ${high:,.0f}M<br>Mid: ${mid:,.0f}M<extra></extra>"
        ))
    
    # Add current EV line
    fig.add_vline(x=float(current_ev), line_dash="dash", line_color="red", 
                  annotation_text=f"Current EV: ${current_ev:,.0f}M", annotation_position="top")
    
    fig.update_layout(
        title="Football Field - Valuation Ranges by Method",
        xaxis_title="Enterprise Value ($ millions)",
        yaxis_title="Valuation Method",
        height=400,
        showlegend=False,
        xaxis=dict(tickformat="$,.0f"),
        plot_bgcolor='rgba(255,255,255,0.8)',
        paper_bgcolor='rgba(255,255,255,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # SUMMARY TABLE
    # ========================================================================
    st.subheader("📊 Valuation Summary")
    summary_data = []
    for method, low, high, mid in zip(methods, lows, highs, midpoints):
        summary_data.append({
            "Method": method,
            "Low ($M)": f"${low:,.0f}",
            "High ($M)": f"${high:,.0f}",
            "Midpoint ($M)": f"${mid:,.0f}",
            "Range ($M)": f"${high - low:,.0f}"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # CURRENT EV POSITION
    # ========================================================================
    st.subheader("📍 Current EV Position")
    
    in_ev_range = ev_low <= current_ev <= ev_high
    in_comps_range = comps_low <= current_ev <= comps_high
    in_dcf_range = dcf_low <= current_ev <= dcf_high
    
    if in_ev_range:
        st.success("✅ Current EV is within 52-Week EV range")
    else:
        st.warning("⚠️ Current EV is OUTSIDE 52-Week EV range")
    
    if in_comps_range:
        st.success("✅ Current EV is within Comps Analysis range")
    else:
        st.warning("⚠️ Current EV is OUTSIDE Comps Analysis range")
    
    if in_dcf_range:
        st.success("✅ Current EV is within DCF range")
    else:
        st.warning("⚠️ Current EV is OUTSIDE DCF range")
    
    # ========================================================================
    # INTERPRETATION & VERDICT
    # ========================================================================
    st.markdown("---")
    st.markdown('<div class="section-header">🎯 Interpretation & Verdict</div>', unsafe_allow_html=True)
    
    # Count how many methods suggest undervalued/overvalued
    undervalued_count = 0
    overvalued_count = 0
    fairly_valued_count = 0
    
    # Compare current EV to each method's midpoint
    ev_midpoint = (ev_low + ev_high) / 2
    comps_midpoint = (comps_low + comps_high) / 2
    dcf_midpoint = (dcf_low + dcf_high) / 2
    
    # 52-Week EV comparison
    if current_ev < ev_midpoint * 0.9:
        undervalued_count += 1
    elif current_ev > ev_midpoint * 1.1:
        overvalued_count += 1
    else:
        fairly_valued_count += 1
    
    # Comps comparison
    if current_ev < comps_midpoint * 0.9:
        undervalued_count += 1
    elif current_ev > comps_midpoint * 1.1:
        overvalued_count += 1
    else:
        fairly_valued_count += 1
    
    # DCF comparison
    if current_ev < dcf_midpoint * 0.9:
        undervalued_count += 1
    elif current_ev > dcf_midpoint * 1.1:
        overvalued_count += 1
    else:
        fairly_valued_count += 1
    
    # Determine overall verdict
    if overvalued_count >= 2:
        verdict = "🔴 POTENTIALLY OVERVALUED"
        verdict_color = "warning-card"
        verdict_explanation = "Most valuation methods suggest the current price is above fair value."
    elif undervalued_count >= 2:
        verdict = "🟢 POTENTIALLY UNDERVALUED"
        verdict_color = "success-card"
        verdict_explanation = "Most valuation methods suggest the current price is below fair value."
    else:
        verdict = "🟡 FAIRLY VALUED"
        verdict_color = "info-card"
        verdict_explanation = "Valuation methods are mixed or current price is within reasonable ranges."
    
    # Display verdict
    st.markdown(f"""
    <div class="{verdict_color}">
        <b>{verdict}</b><br>
        {verdict_explanation}
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed interpretation by method
    st.markdown("### 📋 Method-by-Method Interpretation")
    
    # 52-Week EV interpretation
    st.markdown(f"""
    <div class="info-card">
    <b>📊 52-Week EV Range</b><br>
    - Range: <b>${ev_low:,.0f}M - ${ev_high:,.0f}M</b><br>
    - Midpoint: <b>${ev_midpoint:,.0f}M</b><br>
    - Current EV: <b>${current_ev:,.0f}M</b><br><br>
    <b>Interpretation:</b><br>
    This range represents where Tesla's EV has traded over the past 52 weeks.
    - Current EV is {'✅ WITHIN' if in_ev_range else '⚠️ OUTSIDE'} this historical range.
    - {'This suggests the stock is trading within its historical valuation band.' if in_ev_range else 'This suggests the stock is trading outside its historical range (could indicate a trend change or overreaction).'}
    </div>
    """, unsafe_allow_html=True)
    
    # Comps interpretation
    st.markdown(f"""
    <div class="info-card">
    <b>🏢 Comps Analysis Range</b><br>
    - Range: <b>${comps_low:,.0f}M - ${comps_high:,.0f}M</b><br>
    - Midpoint: <b>${comps_midpoint:,.0f}M</b><br>
    - Current EV: <b>${current_ev:,.0f}M</b><br><br>
    <b>Interpretation:</b><br>
    This range comes from applying peer company multiples to Tesla's financials.
    - Current EV is {'✅ WITHIN' if in_comps_range else '⚠️ OUTSIDE'} the valuation range suggested by peers.
    - {'This suggests Tesla is fairly valued compared to its peers.' if in_comps_range else 'This suggests Tesla is trading at a premium/discount to its peers. If above the range → potentially overvalued. If below → potentially undervalued.'}
    </div>
    """, unsafe_allow_html=True)
    
    # DCF interpretation
    st.markdown(f"""
    <div class="info-card">
    <b>📈 DCF Model Range</b><br>
    - Range: <b>${dcf_low:,.0f}M - ${dcf_high:,.0f}M</b><br>
    - Midpoint: <b>${dcf_midpoint:,.0f}M</b><br>
    - Current EV: <b>${current_ev:,.0f}M</b><br><br>
    <b>Interpretation:</b><br>
    This range comes from discounting Tesla's projected future cash flows.
    - Current EV is {'✅ WITHIN' if in_dcf_range else '⚠️ OUTSIDE'} the intrinsic value range suggested by DCF.
    - {'This suggests the market price aligns with fundamental value.' if in_dcf_range else 'If current EV is above the DCF range → potentially overvalued (market is optimistic). If below → potentially undervalued (market is pessimistic).'}
    </div>
    """, unsafe_allow_html=True)
    
    # Final guidance
    st.markdown("""
    <div class="verdict-card">
    <b>💡 What To Do With This Information:</b><br><br>
    
    | If the verdict is... | Consider... |
    |---------------------|-------------|
    | 🟢 **Undervalued** | The stock may be trading at a discount. Investigate WHY (temporary issues? market overreaction?) before buying. |
    | 🟡 **Fairly Valued** | The stock is trading near fair value. HOLD unless you have a strong thesis for upside. |
    | 🔴 **Overvalued** | The stock may be expensive. Consider taking profits or waiting for a better entry price. |
    
    <b>⚠️ Remember:</b> Valuation is not an exact science. Use this as ONE input in your investment decision, not the sole factor. Always consider:
    - Company growth prospects
    - Industry trends
    - Management quality
    - Your own risk tolerance
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("💡 The football field helps visualize valuation ranges from different methodologies. The wider the bar, the more uncertainty in that method.")