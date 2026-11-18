import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="BANKMIND AI", page_icon="🏦", layout="wide")

BASE_DIR = Path(__file__).parent
HOSPITAL_FILE = BASE_DIR / "BANKMIND_Telangana_Batch_01.csv"

st.title("🏦 BANKMIND AI")
st.caption("AI-powered Banking Intelligence | Independent educational prototype")

CUSTOMERS = {
    "Apex Multispeciality Hospital": {
        "segment": "Healthcare Banking", "turnover": 48.5, "ebitda": 7.2,
        "debt": 18.0, "current_assets": 12.0, "current_liabilities": 8.0,
        "notes": "Fictional hospital group exploring equipment finance and working capital."
    },
    "Orion Components Pvt Ltd": {
        "segment": "SME Banking", "turnover": 32.0, "ebitda": 4.1,
        "debt": 11.5, "current_assets": 9.0, "current_liabilities": 6.0,
        "notes": "Fictional manufacturing borrower with potential capex requirements."
    },
    "Cedar Retail Group": {
        "segment": "Corporate Banking", "turnover": 76.0, "ebitda": 8.8,
        "debt": 20.0, "current_assets": 16.0, "current_liabilities": 10.0,
        "notes": "Fictional multi-location retailer with collections and payments needs."
    },
    "Northstar Wealth Client": {
        "segment": "Wealth Management", "turnover": 0.0, "ebitda": 0.0,
        "debt": 0.0, "current_assets": 0.0, "current_liabilities": 0.0,
        "notes": "Fictional wealth relationship profile for demonstration only."
    },
}

@st.cache_data
def load_hospitals():
    if not HOSPITAL_FILE.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(HOSPITAL_FILE, dtype=str).fillna("")
    except Exception as exc:
        st.error(f"Could not read the hospital CSV: {exc}")
        return pd.DataFrame()

hospitals = load_hospitals()

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Hospital Directory", "Relationship Coach",
     "Credit Intelligence", "About & Safeguards"]
)

if page == "Overview":
    st.subheader("Banking intelligence workspace")
    c1, c2, c3 = st.columns(3)
    c1.metric("Demo relationships", "4")
    c2.metric("Banking segments", "5")
    c3.metric("Hospital records loaded", f"{len(hospitals):,}")
    st.markdown("### Modules")
    st.write("- **Hospital Directory:** search and filter Telangana healthcare facilities.")
    st.write("- **AI Relationship Coach:** meeting preparation and relationship insights.")
    st.write("- **Credit Intelligence:** indicative financial ratios and risk prompts.")
    st.write("- **Financial Analyst:** planned financial statement analysis.")
    st.write("- **Banking Opportunity AI:** planned cross-sell opportunity identification.")
    st.write("- **Compliance Assistant:** planned search across approved sample policies.")
    st.write("- **Management Dashboard:** planned portfolio and business KPIs.")
    st.info("This version uses a small source-listed hospital sample and fictional customer data. It does not connect to a bank or an AI model.")

elif page == "Hospital Directory":
    st.subheader("🏥 Telangana Hospital Directory")
    st.write("Search the currently imported facility records. This is an initial batch, not a complete directory of all hospitals in Telangana.")
    if hospitals.empty:
        st.warning("Hospital data was not found. Upload 'BANKMIND_Telangana_Batch_01.csv' to the same repository folder as app.py, then restart the app.")
    else:
        expected = [
            "facility_name", "facility_type", "district", "mandal_or_city",
            "locality", "full_address", "phone_public", "website",
            "specialities", "bed_count_public", "source_name",
            "valid_from", "valid_to", "verification_status"
        ]
        for col in expected:
            if col not in hospitals.columns:
                hospitals[col] = ""

        search_text = st.text_input(
            "Search by hospital name, location, speciality or address",
            placeholder="e.g. AIG, Hyderabad, oncology, Kukatpally"
        )
        districts = sorted(x for x in hospitals["district"].str.strip().unique() if x)
        types = sorted(x for x in hospitals["facility_type"].str.strip().unique() if x)

        f1, f2 = st.columns(2)
        district = f1.selectbox("Filter by district", ["All districts"] + districts)
        facility_type = f2.selectbox("Filter by facility type", ["All facility types"] + types)

        filtered = hospitals.copy()
        if district != "All districts":
            filtered = filtered[filtered["district"] == district]
        if facility_type != "All facility types":
            filtered = filtered[filtered["facility_type"] == facility_type]
        if search_text.strip():
            searchable = ["facility_name", "facility_type", "district",
                          "mandal_or_city", "locality", "full_address", "specialities"]
            searchable = [c for c in searchable if c in filtered.columns]
            combined = filtered[searchable].astype(str).agg(" ".join, axis=1)
            filtered = filtered[combined.str.contains(search_text.strip(), case=False, na=False, regex=False)]

        st.metric("Matching facilities", f"{len(filtered):,}")
        display_cols = [
            "facility_name", "facility_type", "district", "mandal_or_city",
            "full_address", "phone_public", "specialities", "verification_status"
        ]
        display_cols = [c for c in display_cols if c in filtered.columns]
        st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

        if not filtered.empty:
            st.markdown("### Facility profile")
            selected = st.selectbox("Choose a facility to view its details",
                                    filtered["facility_name"].tolist())
            facility = filtered[filtered["facility_name"] == selected].iloc[0]
            left, right = st.columns(2)
            with left:
                st.write(f"**Facility type:** {facility.get('facility_type', '') or 'Not listed'}")
                st.write(f"**District:** {facility.get('district', '') or 'Not listed'}")
                st.write(f"**City / mandal:** {facility.get('mandal_or_city', '') or 'Not listed'}")
                st.write(f"**Locality:** {facility.get('locality', '') or 'Not listed'}")
                st.write(f"**Address:** {facility.get('full_address', '') or 'Not listed'}")
            with right:
                st.write(f"**Public phone:** {facility.get('phone_public', '') or 'Not listed'}")
                st.write(f"**Website:** {facility.get('website', '') or 'Not listed'}")
                st.write(f"**Specialities:** {facility.get('specialities', '') or 'Not listed'}")
                st.write(f"**Beds:** {facility.get('bed_count_public', '') or 'Not listed'}")
                st.write(f"**Verification:** {facility.get('verification_status', '') or 'Not listed'}")
            st.caption(
                f"Source: {facility.get('source_name', '')}. Validity dates where available: "
                f"{facility.get('valid_from', '')} to {facility.get('valid_to', '')}. "
                "Verify details with the relevant authority or facility before relying on them."
            )

        st.download_button(
            "Download filtered results as CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="BANKMIND_Telangana_Hospital_Search.csv",
            mime="text/csv"
        )

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
        leverage = d["debt"] / d["ebitda"] if d["ebitda"] else 0
        current_ratio = d["current_assets"] / d["current_liabilities"] if d["current_liabilities"] else 0
        margin = d["ebitda"] / d["turnover"] * 100
        a, b, c = st.columns(3)
        a.metric("EBITDA margin", f"{margin:.1f}%")
        b.metric("Debt / EBITDA*", f"{leverage:.2f}x")
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
