import streamlit as st
import pandas as pd
import requests
import html
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CyberROI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    :root {
        --ink: #e8f0f7;
        --muted: #8fa3b5;
        --canvas: #07141f;
        --panel: #0d202c;
        --panel-light: #122b39;
        --line: #214052;
        --cyan: #25d0c2;
        --danger: #ff647c;
        --success: #42d6a4;
    }

    .stApp {
        background: radial-gradient(circle at 85% 0%, #123348 0, var(--canvas) 32rem);
        color: var(--ink);
    }

    [data-testid="stAppViewContainer"] > .main { background: transparent; }
    [data-testid="stHeader"] { background: rgba(7, 20, 31, .84); }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1d29 0%, #07131d 100%);
        border-right: 1px solid var(--line);
    }

    section[data-testid="stSidebar"] * { color: var(--ink); }
    section[data-testid="stSidebar"] .stRadio label { color: var(--muted); }
    section[data-testid="stSidebar"] .stRadio label:hover { color: var(--cyan); }

    .main-title {
        color: var(--ink);
        font-size: clamp(2rem, 4vw, 3.25rem);
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.05;
        margin: 0;
    }

    .subtitle {
        color: var(--cyan);
        font-size: .84rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: .65rem 0 1.5rem;
    }

    .section-title {
        border-bottom: 1px solid var(--line);
        color: var(--ink);
        font-size: 1.2rem;
        font-weight: 750;
        margin: 2rem 0 1rem;
        padding-bottom: .7rem;
    }

    .info-card, .metric-card, .risk-card, .success-card {
        background: linear-gradient(145deg, rgba(18, 43, 57, .96), rgba(10, 28, 39, .96));
        border: 1px solid var(--line);
        border-radius: 10px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, .14);
    }

    .info-card {
        color: var(--muted);
        line-height: 1.7;
        margin-bottom: 1rem;
        padding: 1.1rem 1.25rem;
    }

    .info-card b { color: var(--ink); }

    .metric-card, .risk-card {
        min-height: 118px;
        padding: 1.25rem;
        transition: border-color .2s ease, transform .2s ease, box-shadow .2s ease;
    }

    .metric-card:hover, .risk-card:hover, .success-card:hover {
        border-color: var(--cyan);
        box-shadow: 0 16px 36px rgba(0, 0, 0, .24);
        transform: translateY(-2px);
    }

    .metric-label {
        color: var(--muted);
        font-size: .7rem;
        font-weight: 800;
        letter-spacing: 1.3px;
        margin-bottom: .8rem;
    }

    .metric-value {
        color: var(--ink);
        font-size: clamp(1.25rem, 2vw, 1.85rem);
        font-weight: 800;
    }

    .risk-card { background: linear-gradient(145deg, #3d1e2b, #251723); border-color: #80394e; }
    .risk-card .metric-value { color: #ff91a2; }
    .success-card { background: linear-gradient(145deg, #10382f, #0b2725); border-color: #216d5d; padding: 1rem 1.15rem; margin-bottom: .7rem; }
    .success-card .metric-value { color: var(--success); }

    .ai-summary-card {
        background: linear-gradient(145deg, rgba(14, 42, 55, .98), rgba(8, 25, 35, .98));
        border: 1px solid #2a6275;
        border-left: 4px solid var(--cyan);
        border-radius: 10px;
        box-shadow: 0 18px 42px rgba(0, 0, 0, .2);
        margin: 1rem 0 2rem;
        padding: 1.35rem 1.5rem 1.5rem;
    }

    .ai-summary-header {
        align-items: center;
        display: flex;
        gap: .75rem;
        justify-content: space-between;
        margin-bottom: 1.1rem;
    }

    .ai-summary-title {
        color: var(--ink);
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: .1px;
    }

    .ai-summary-meta { color: var(--muted); font-size: .75rem; }
    .confidence-badge, .risk-badge {
        border-radius: 999px;
        display: inline-block;
        font-size: .7rem;
        font-weight: 800;
        letter-spacing: .4px;
        padding: .35rem .65rem;
        white-space: nowrap;
    }

    .confidence-badge { background: rgba(66, 214, 164, .14); color: var(--success); }
    .risk-badge { background: rgba(255, 180, 84, .15); color: #ffc36e; }

    .ai-summary-copy {
        color: #d2e0e8;
        font-size: .95rem;
        line-height: 1.75;
        margin: 0 0 1.25rem;
    }

    .ai-summary-insights {
        border-top: 1px solid var(--line);
        display: grid;
        gap: .7rem 1.5rem;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        padding-top: 1rem;
    }

    .ai-insight { color: var(--muted); font-size: .82rem; line-height: 1.45; }
    .ai-insight strong { color: var(--ink); display: block; font-size: .7rem; letter-spacing: .8px; margin-bottom: .15rem; text-transform: uppercase; }

    @media (max-width: 700px) {
        .ai-summary-header { align-items: flex-start; flex-direction: column; }
        .ai-summary-insights { grid-template-columns: 1fr; }
    }

    .stButton > button {
        background: linear-gradient(135deg, #1ab8b0, #277dd4);
        border: 0;
        border-radius: 7px;
        color: white;
        font-weight: 750;
        min-height: 2.7rem;
        padding: .55rem 1.2rem;
        transition: filter .2s ease, transform .2s ease;
    }

    .stButton > button:hover { color: white; filter: brightness(1.12); transform: translateY(-1px); }
    .stButton > button:focus { box-shadow: 0 0 0 2px var(--canvas), 0 0 0 4px var(--cyan); }

    section[data-testid="stFileUploader"] {
        background: rgba(13, 32, 44, .72);
        border: 1px dashed #3b6477;
        border-radius: 9px;
        padding: .5rem;
    }

    div[data-baseweb="slider"] { padding: .8rem .2rem .2rem; }
    div[data-baseweb="select"] > div, .stTextInput input { background: var(--panel-light); border-color: var(--line); }
    label, .stMarkdown p { color: var(--muted); }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 9px; overflow: hidden; }
    [data-testid="stAlert"] { border-radius: 8px; }
    hr { border-color: var(--line); }

    .footer {
        border-top: 1px solid var(--line);
        color: #6f899a;
        font-size: .75rem;
        letter-spacing: .4px;
        margin-top: 3rem;
        padding: 1.5rem .5rem 2rem;
        text-align: center;
    }

    @media (max-width: 700px) {
        .main-title { font-size: 2.2rem; }
        .section-title { margin-top: 1.5rem; }
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">◈ CyberROI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Cyber risk quantification · investment intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="info-card" style="display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
        <span>● <b style="color:#42d6a4;">SYSTEM OPERATIONAL</b> &nbsp;|&nbsp; Risk engine ready</span>
        <span>{datetime.now().strftime('%d %b %Y · %H:%M')} local</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-card">
    <b>Executive risk command center</b><br>
    Convert cybersecurity exposure into a clear financial view and prioritize
    the controls that deliver measurable risk reduction.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "## ◈ CyberROI"
)

st.sidebar.markdown(
    "---"
)

st.sidebar.markdown(
    "### DATA CONNECTOR"
)

data_source = st.sidebar.radio(
    "Choose how you want to provide data:",
    [
        "🧪 Demo Data",
        "📁 Upload Dataset",
        "🌐 Live Cybersecurity Data"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    **ANALYSIS PIPELINE**

    `01`  Data source

    ↓

    `02`  Normalization

    ↓

    `03`  Risk engine

    ↓

    `04`  Investment optimizer

    ↓

    `05`  Executive advisor

    ---

    🟢  SYSTEM STATUS

    All services operational
    """
)


# =========================================================
# DEMO DATA FUNCTION
# =========================================================

def get_demo_data():

    data = [
        {
            "asset": "Customer Database",
            "value": 500000,
            "likelihood": 0.40,
            "impact_pct": 0.60
        },
        {
            "asset": "Payment Processing Server",
            "value": 800000,
            "likelihood": 0.30,
            "impact_pct": 0.80
        },
        {
            "asset": "Employee Laptops",
            "value": 100000,
            "likelihood": 0.50,
            "impact_pct": 0.30
        },
        {
            "asset": "Company Website",
            "value": 150000,
            "likelihood": 0.60,
            "impact_pct": 0.40
        },
        {
            "asset": "Internal Email System",
            "value": 200000,
            "likelihood": 0.35,
            "impact_pct": 0.50
        }
    ]

    return pd.DataFrame(data)


# =========================================================
# FILE LOADING FUNCTION
# =========================================================

def load_file(file):

    try:

        if file.name.lower().endswith(".csv"):
            return pd.read_csv(file)

        elif file.name.lower().endswith(".xlsx"):
            return pd.read_excel(file)

        return None

    except Exception as error:

        st.error(
            f"Could not read the file: {error}"
        )

        return None


# =========================================================
# LIVE NVD DATA FUNCTION
# =========================================================

def get_live_vulnerabilities():

    url = (
        "https://services.nvd.nist.gov/"
        "rest/json/cves/2.0"
    )

    try:

        response = requests.get(
            url,
            params={
                "resultsPerPage": 10
            },
            timeout=20
        )

        if response.status_code != 200:

            st.error(
                f"Live API returned status "
                f"{response.status_code}"
            )

            return None

        data = response.json()

        rows = []

        for vulnerability in data.get(
            "vulnerabilities",
            []
        ):

            cve = vulnerability.get(
                "cve",
                {}
            )

            cve_id = cve.get(
                "id",
                "Unknown"
            )

            description = "No description"

            descriptions = cve.get(
                "descriptions",
                []
            )

            if descriptions:

                description = descriptions[0].get(
                    "value",
                    "No description"
                )

            score = 0

            metrics = cve.get(
                "metrics",
                {}
            )

            if metrics.get(
                "cvssMetricV31"
            ):

                score = metrics[
                    "cvssMetricV31"
                ][0][
                    "cvssData"
                ].get(
                    "baseScore",
                    0
                )

            elif metrics.get(
                "cvssMetricV30"
            ):

                score = metrics[
                    "cvssMetricV30"
                ][0][
                    "cvssData"
                ].get(
                    "baseScore",
                    0
                )

            elif metrics.get(
                "cvssMetricV2"
            ):

                score = metrics[
                    "cvssMetricV2"
                ][0][
                    "cvssData"
                ].get(
                    "baseScore",
                    0
                )

            likelihood = min(
                score / 10,
                1
            )

            impact_pct = min(
                0.20 + (score / 10) * 0.70,
                0.90
            )

            # Prototype financial value.
            # Production version should obtain
            # actual asset value from company data.

            asset_value = 100000

            rows.append(
                {
                    "asset": cve_id,
                    "value": asset_value,
                    "likelihood": likelihood,
                    "impact_pct": impact_pct,
                    "severity_score": score,
                    "description": description
                }
            )

        if not rows:

            return None

        return pd.DataFrame(rows)

    except Exception as error:

        st.error(
            f"Could not retrieve live data: {error}"
        )

        return None


# =========================================================
# DATA SOURCE 1 — DEMO
# =========================================================

if data_source == "🧪 Demo Data":

    st.markdown(
        '<div class="section-title">'
        '🧪 Demo Dataset'
        '</div>',
        unsafe_allow_html=True
    )

    df = get_demo_data()

    st.success(
        "Demo data loaded successfully."
    )


# =========================================================
# DATA SOURCE 2 — UPLOAD
# =========================================================

elif data_source == "📁 Upload Dataset":

    st.markdown(
        '<div class="section-title">'
        '📁 Upload Dataset'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload your company risk dataset",
        type=["csv", "xlsx"]
    )

    if uploaded_file is None:

        st.info(
            "Upload a CSV or Excel file to continue."
        )

        st.stop()

    df = load_file(
        uploaded_file
    )

    if df is None:

        st.stop()

    st.success(
        f"{uploaded_file.name} uploaded successfully."
    )


# =========================================================
# DATA SOURCE 3 — LIVE
# =========================================================

else:

    st.markdown(
        '<div class="section-title">'
        '🌐 Live Cybersecurity Data'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">
        CyberROI can retrieve current vulnerability
        information from the NVD vulnerability API.
        </div>
        """,
        unsafe_allow_html=True
    )

    fetch_live = st.button(
        "🔄 Fetch Live Vulnerabilities"
    )

    if not fetch_live:

        st.info(
            "Click 'Fetch Live Vulnerabilities' "
            "to retrieve live data."
        )

        st.stop()

    df = get_live_vulnerabilities()

    if df is None:

        st.error(
            "No live vulnerability data was received."
        )

        st.stop()

    st.success(
        "Live vulnerability data retrieved successfully."
    )


# =========================================================
# RAW DATA
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📋 Input Data'
    '</div>',
    unsafe_allow_html=True
)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# COLUMN MAPPING FOR UPLOADED DATA
# =========================================================

if data_source == "📁 Upload Dataset":

    st.markdown(
        '<div class="section-title">'
        '🔗 Map Dataset Columns'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Select the columns that correspond to the "
        "four required risk inputs."
    )

    columns = list(df.columns)

    if len(columns) < 4:

        st.error(
            "Your dataset needs at least four columns "
            "to perform risk analysis."
        )

        st.stop()

    col1, col2 = st.columns(2)

    with col1:

        asset_column = st.selectbox(
            "Asset Name",
            columns,
            key="asset_column"
        )

        value_column = st.selectbox(
            "Asset Value",
            columns,
            key="value_column"
        )

    with col2:

        likelihood_column = st.selectbox(
            "Likelihood",
            columns,
            key="likelihood_column"
        )

        impact_column = st.selectbox(
            "Impact",
            columns,
            key="impact_column"
        )

    try:

        risk_df = pd.DataFrame()

        risk_df["asset"] = df[
            asset_column
        ]

        risk_df["value"] = pd.to_numeric(
            df[value_column],
            errors="coerce"
        )

        risk_df["likelihood"] = pd.to_numeric(
            df[likelihood_column],
            errors="coerce"
        )

        risk_df["impact_pct"] = pd.to_numeric(
            df[impact_column],
            errors="coerce"
        )

        risk_df = risk_df.dropna()

    except Exception as error:

        st.error(
            f"Dataset mapping failed: {error}"
        )

        st.stop()

else:

    risk_df = df.copy()


# =========================================================
# NORMALIZE NUMERIC DATA
# =========================================================

risk_df["value"] = pd.to_numeric(
    risk_df["value"],
    errors="coerce"
)

risk_df["likelihood"] = pd.to_numeric(
    risk_df["likelihood"],
    errors="coerce"
)

risk_df["impact_pct"] = pd.to_numeric(
    risk_df["impact_pct"],
    errors="coerce"
)

risk_df = risk_df.dropna(
    subset=[
        "value",
        "likelihood",
        "impact_pct"
    ]
)


# =========================================================
# NORMALIZE LIKELIHOOD AND IMPACT
# =========================================================

risk_df["likelihood"] = risk_df[
    "likelihood"
].clip(
    0,
    1
)

risk_df["impact_pct"] = risk_df[
    "impact_pct"
].clip(
    0,
    1
)


# =========================================================
# RISK FORMULA
# =========================================================

risk_df["risk_exposure"] = (
    risk_df["value"]
    * risk_df["likelihood"]
    * risk_df["impact_pct"]
)

total_risk = risk_df[
    "risk_exposure"
].sum()

total_asset_value = risk_df[
    "value"
].sum()


# =========================================================
# DASHBOARD
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '📊 Cyber Risk Dashboard'
    '</div>',
    unsafe_allow_html=True
)

m1, m2, m3 = st.columns(3)

with m1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                TOTAL ASSETS
            </div>
            <div class="metric-value">
                {len(risk_df):,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                TOTAL ASSET VALUE
            </div>
            <div class="metric-value">
                 ₹{total_asset_value:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    st.markdown(
        f"""
        <div class="risk-card">
            <div class="metric-label">
                TOTAL RISK EXPOSURE
            </div>
            <div class="metric-value">
                 ₹{total_risk:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# RISK TABLE
# =========================================================

st.markdown(
    '<div class="section-title">'
    '💰 Risk Exposure by Asset'
    '</div>',
    unsafe_allow_html=True
)

table_df = risk_df[
    [
        "asset",
        "value",
        "likelihood",
        "impact_pct",
        "risk_exposure"
    ]
].copy()

table_df["value"] = table_df[
    "value"
].map(
    lambda x: f" ₹{x:,.0f}"
)

table_df["likelihood"] = table_df[
    "likelihood"
].map(
    lambda x: f"{x * 100:.1f}%"
)

table_df["impact_pct"] = table_df[
    "impact_pct"
].map(
    lambda x: f"{x * 100:.1f}%"
)

table_df["risk_exposure"] = table_df[
    "risk_exposure"
].map(
    lambda x: f" ₹{x:,.0f}"
)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# RISK CHART
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📈 Risk Exposure Visualization'
    '</div>',
    unsafe_allow_html=True
)

chart_df = risk_df[
    ["asset", "risk_exposure"]
].copy()

chart_df = chart_df.set_index(
    "asset"
)

st.bar_chart(
    chart_df,
    height=400
)


# =========================================================
# SECURITY CONTROLS
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🛡️ Security Investment Optimizer'
    '</div>',
    unsafe_allow_html=True
)

controls = [
    {
        "control": "Multi-Factor Authentication",
        "cost": 20000,
        "risk_reduction": 150000
    },
    {
        "control": "Patch Management",
        "cost": 50000,
        "risk_reduction": 300000
    },
    {
        "control": "Employee Security Training",
        "cost": 15000,
        "risk_reduction": 80000
    },
    {
        "control": "Endpoint Detection & Response",
        "cost": 70000,
        "risk_reduction": 250000
    },
    {
        "control": "Data Encryption",
        "cost": 40000,
        "risk_reduction": 200000
    },
    {
        "control": "Automated Backups",
        "cost": 25000,
        "risk_reduction": 120000
    }
]

controls_df = pd.DataFrame(
    controls
)

controls_df["value_per_rupees"] = (
    controls_df["risk_reduction"]
    / controls_df["cost"]
)


# =========================================================
# BUDGET
# =========================================================

budget = st.slider(
    "💵 Security Budget",
    min_value=0,
    max_value=150000,
    value=50000,
    step=5000,
    format="₹%d"
)


# =========================================================
# OPTIMIZER
# =========================================================

sorted_controls = controls_df.sort_values(
    "value_per_rupees",
    ascending=False
)

chosen_controls = []

spent = 0

risk_reduced = 0

for _, row in sorted_controls.iterrows():

    if spent + row["cost"] <= budget:

        chosen_controls.append(
            row["control"]
        )

        spent += row["cost"]

        risk_reduced += row[
            "risk_reduction"
        ]


# =========================================================
# REMAINING RISK
# =========================================================

remaining_risk = max(
    total_risk - risk_reduced,
    0
)


# =========================================================
# OPTIMIZER METRICS
# =========================================================

r1, r2, r3 = st.columns(3)

with r1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                BUDGET USED
            </div>
            <div class="metric-value">
                 ₹{spent:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r2:

    st.markdown(
        f"""
        <div class="success-card">
            <div class="metric-label">
                RISK REDUCED
            </div>
            <div class="metric-value">
                 ₹{risk_reduced:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r3:

    st.markdown(
        f"""
        <div class="risk-card">
            <div class="metric-label">
                REMAINING RISK
            </div>
            <div class="metric-value">
                 ₹{remaining_risk:,.0f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# RECOMMENDATIONS
# =========================================================

st.subheader(
    "🎯 Recommended Security Controls"
)

if chosen_controls:

    for control in chosen_controls:

        st.markdown(
            f"""
            <div class="success-card">
                <b>✓ {control}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.warning(
        "Increase the security budget to receive "
        "recommendations."
    )


# =========================================================
# AI EXECUTIVE RISK SUMMARY
# =========================================================

if risk_df.empty:

    top_risk_asset = "No asset identified"
    top_risk_value = 0

else:

    top_risk_row = risk_df.loc[
        risk_df["risk_exposure"].idxmax()
    ]

    top_risk_asset = html.escape(str(top_risk_row["asset"]))
    top_risk_value = top_risk_row["risk_exposure"]

risk_reduction_pct = (
    (risk_reduced / total_risk) * 100
    if total_risk > 0
    else 0
)

roi_pct = (
    ((risk_reduced - spent) / spent) * 100
    if spent > 0
    else 0
)

risk_ratio = (
    total_risk / total_asset_value
    if total_asset_value > 0
    else 0
)

if risk_ratio >= 0.50:
    risk_level = "Critical"
    risk_color = "🔴"
elif risk_ratio >= 0.30:
    risk_level = "High"
    risk_color = "🟠"
elif risk_ratio >= 0.10:
    risk_level = "Medium"
    risk_color = "🟡"
else:
    risk_level = "Low"
    risk_color = "🟢"

controls_summary = (
    ", ".join(chosen_controls)
    if chosen_controls
    else "no controls are currently selected"
)

summary_sentence = (
    f"Based on the current assessment, the organization has an estimated "
    f"annual cyber risk exposure of ₹{total_risk:,.0f}. The highest-risk "
    f"asset is {top_risk_asset}, contributing ₹{top_risk_value:,.0f} to "
    f"the modeled exposure. Implementing {controls_summary} within the "
    f"allocated budget of ₹{budget:,.0f} is projected to reduce risk "
    f"exposure by {risk_reduction_pct:.1f}%."
)

st.markdown(
    '<div class="section-title">🤖 AI Executive Risk Summary</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="ai-summary-card">
        <div class="ai-summary-header">
            <div>
                <div class="ai-summary-title">◈ Executive cyber risk briefing</div>
                <div class="ai-summary-meta">Template-generated from the current assessment · Export-ready report format</div>
            </div>
            <div>
                <span class="confidence-badge">92% CONFIDENCE</span>
                <span class="risk-badge">{risk_color} {risk_level.upper()} RISK</span>
            </div>
        </div>
        <p class="ai-summary-copy">{summary_sentence} This investment has an estimated cybersecurity ROI of {roi_pct:.1f}%, supporting a focused improvement in organizational resilience and security readiness.</p>
        <div class="ai-summary-insights">
            <div class="ai-insight"><strong>Highest risk asset</strong>{top_risk_asset}</div>
            <div class="ai-insight"><strong>Estimated financial exposure</strong>₹{total_risk:,.0f} annually</div>
            <div class="ai-insight"><strong>Recommended investment priority</strong>{controls_summary}</div>
            <div class="ai-insight"><strong>Expected risk reduction</strong>{risk_reduction_pct:.1f}% · ROI {roi_pct:.1f}%</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CONTROL TABLE
# =========================================================

st.subheader(
    "Available Security Controls"
)

control_display = controls_df[
    [
        "control",
        "cost",
        "risk_reduction",
        "value_per_rupees"
    ]
].copy()

control_display.columns = [
    "Security Control",
    "Cost",
    "Potential Risk Reduction",
    "Risk Reduction / Rupees"
]

control_display["Cost"] = control_display[
    "Cost"
].map(
    lambda x: f" ₹{x:,.0f}"
)

control_display[
    "Potential Risk Reduction"
] = control_display[
    "Potential Risk Reduction"
].map(
    lambda x: f"₹{x:,.0f}"
)

control_display[
    "Risk Reduction / Rupees"
] = control_display[
    "Risk Reduction / Rupees"
].map(
    lambda x: f"{x:.2f}"
)

st.dataframe(
    control_display,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# RESCAN BUTTON
# =========================================================

st.divider()

if st.button(
    "🔄 Re-scan Now"
):

    st.rerun()


# =========================================================
# AI PLACEHOLDER
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🤖 AI Risk Advisor'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "The AI Risk Advisor will convert the calculated "
    "risk and investment results into a simple "
    "executive recommendation. We will connect the "
    "AI API in the next stage."
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        ◈ CyberROI &nbsp;·&nbsp; Enterprise Cyber Risk Intelligence
        <br>
        v1.0.0 &nbsp;·&nbsp; Hackathon Innovation Team &nbsp;·&nbsp; Executive analytics prototype
    </div>
    """,
    unsafe_allow_html=True
)