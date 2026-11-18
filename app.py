import streamlit as st
import pandas as pd

st.set_page_config(page_title="BANKMIND AI", page_icon="🏦", layout="wide")

st.title("🏦 BANKMIND AI")
st.caption("AI-powered Banking Intelligence | Independent educational prototype")

CUSTOMERS = {
    "Apex Multispeciality Hospital": {
        "segment": "Healthcare Banking",
        "turnover": 48.5,
        "ebitda": 7.2,
        "debt": 18.0,
        "current_assets": 12.0,
        "current_liabilities": 8.0,
        "notes": "Fictional hospital group exploring equipment finance and working capital."
    },
    "Orion Components Pvt Ltd": {
        "segment": "SME Banking",
        "turnover": 32.0,
        "ebitda": 4.1,
        "debt": 11.5,
        "current_assets": 9.0,
        "current_liabilities": 6.0,
        "notes": "Fictional manufacturing borrower with potential capex requirements."
    },
    "Cedar Retail Group": {
        "segment": "Corporate Banking",
        "turnover": 76.0,
        "ebitda": 8.8,
        "debt": 20.0,
        "current_assets": 16.0,
        "current_liabilities": 10.0,
        "notes": "Fictional multi-location retailer with collections and payments needs."
    },
    "Northstar Wealth Client": {
        "segment": "Wealth Management",
        "turnover": 0.0,
        "ebitda": 0.0,
        "debt": 0.0,
        "current_assets": 0.0,
        "current_liabilities": 0.0,
        "notes": "Fictional wealth relationship profile for demonstration only."
    },
}

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Relationship Coach", "Credit Intelligence", "About & Safeguards"]
)

if page == "Overview":
    st.subheader("Banking intelligence workspace")
    c1, c2, c3 = st.columns(3)
    c1.metric("Demo relationships", "4")
    c2.metric("Banking segments", "5")
    c3.metric("Prototype status", "v0.1")
    st.markdown("### Modules")
    st.write("- **AI Relationship Coach:** meeting preparation and relationship insights.")
    st.write("- **Credit Intelligence:** indicative financial ratios and risk prompts.")
    st.write("- **Financial Analyst:** planned financial statement analysis.")
    st.write("- **Banking Opportunity AI:** planned cross-sell opportunity identification.")
    st.write("- **Compliance Assistant:** planned search across approved sample policies.")
    st.write("- **Management Dashboard:** planned portfolio and business KPIs.")
    st.info("This first version uses fictional data and transparent rules. It does not connect to a bank or an AI model.")

elif page == "Relationship Coach":
    st.subheader("AI Relationship Coach")
    customer = st.selectbox("Select a fictional customer", list(CUSTOMERS.keys()))
    data = CUSTOMERS[customer]
    st.write(f"**Segment:** {data['segment']}")
    st.write(f"**Profile:** {data['notes']}")
    st.markdown("### Suggested meeting agenda")
    st.write("1. Understand business performance and near-term priorities.")
    st.write("2. Review collections, payments and cash-management requirements.")
    st.write("3. Discuss funding needs, repayment capacity and documentation.")
    st.write("4. Agree on actions, owners and timelines.")
    st.caption("Suggestions are rule-based demonstration content, not AI-generated advice.")

elif page == "Credit Intelligence":
    st.subheader("Credit Intelligence")
    customer = st.selectbox("Choose a fictional borrower", list(CUSTOMERS.keys()))
    d = CUSTOMERS[customer]
    if d["turnover"] == 0:
        st.warning("Financial ratios are not available for this wealth-client demo profile.")
    else:
        net_debt_ebitda = d["debt"] / d["ebitda"] if d["ebitda"] else 0
        current_ratio = d["current_assets"] / d["current_liabilities"] if d["current_liabilities"] else 0
        ebitda_margin = d["ebitda"] / d["turnover"] * 100
        a, b, c = st.columns(3)
        a.metric("EBITDA margin", f"{ebitda_margin:.1f}%")
        b.metric("Net debt / EBITDA*", f"{net_debt_ebitda:.2f}x")
        c.metric("Current ratio", f"{current_ratio:.2f}x")
        st.markdown("### Input snapshot (₹ crore)")
        st.dataframe(pd.DataFrame({
            "Metric": ["Annual turnover", "EBITDA", "Debt", "Current assets", "Current liabilities"],
            "Value": [d["turnover"], d["ebitda"], d["debt"], d["current_assets"], d["current_liabilities"]]
        }), use_container_width=True, hide_index=True)
        st.caption("*Debt is used as a simplified proxy for net debt in this demo. Verify cash, debt definitions and audited statements before any real analysis.")
        st.markdown("### Review prompts")
        st.write("- Validate revenue quality, margins and cash-flow conversion.")
        st.write("- Review debt maturity, interest burden and repayment capacity.")
        st.write("- Examine receivables ageing, payables and working-capital cycle.")
        st.write("- Compare ratios with sector peers and historical performance.")

else:
    st.subheader("About BANKMIND AI")
    st.write("BANKMIND AI is an independent educational and career-portfolio prototype exploring how digital tools can support banking analysis and relationship management.")
    st.warning("Not affiliated with, endorsed by, or connected to ICICI Bank, JPMorgan Chase or any other financial institution.")
    st.write("Use only synthetic or properly authorized data. Never upload confidential customer information, internal bank documents, credentials or personal financial records.")
    st.write("Outputs are illustrative only—not credit approvals, investment recommendations, compliance determinations or regulatory advice. Human review is essential.")
