import streamlit as st

st.set_page_config(page_title="Valuation Suite", layout="centered", page_icon="🏦")

st.title("🏦 Valuation Suite")
st.markdown("### Complete Company Valuation Toolkit")
st.markdown("---")

st.markdown("""
Welcome to the Valuation Suite! Select a valuation method below:

| Method | Description | Best For |
|--------|-------------|----------|
| 📊 **Enterprise Value** | EV calculation, multiples, 52-week ranges | Quick valuation check |
| 🏢 **Comps Analysis** | Peer comparison using trading multiples | Market-relative valuation |
| 📈 **DCF Model** | Discounted cash flow analysis | Intrinsic value calculation |
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊")
    st.markdown("**Enterprise Value**")
    st.caption("EV, Multiples & 52-Week Ranges")
    if st.button("Launch Beginner Tool", use_container_width=True, type="primary"):
        st.switch_page("pages/beginner_ev.py")

with col2:
    st.markdown("### 🏢")
    st.markdown("**Comps Analysis**")
    st.caption("Peer Multiples & Valuation")
    if st.button("Launch Comps Tool", use_container_width=True, type="primary"):
        st.switch_page("pages/intermediate_comps.py")

with col3:
    st.markdown("### 📈")
    st.markdown("**DCF Model**")
    st.caption("Discounted Cash Flow")
    if st.button("Launch Advanced Tool", use_container_width=True, type="primary"):
        st.switch_page("pages/advanced_dcf.py")

st.markdown("---")
st.info("💡 **Tip:** Each tool is standalone. You can run them independently or use the Football Field to combine results.")

st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>Built with Streamlit • Complete Valuation Suite</p>
</div>
""", unsafe_allow_html=True)