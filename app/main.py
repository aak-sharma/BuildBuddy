from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

try:
    from app.analyzer import analyze_log, gemini_explanation, summarize
except ModuleNotFoundError:
    from analyzer import analyze_log, gemini_explanation, summarize
load_dotenv()

st.set_page_config(
    page_title="BuildBuddy | CI/CD Log Analyzer",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background: #0b1020; }
    [data-testid="stHeader"] { background: rgba(11,16,32,0.85); }
    .block-container { padding-top: 2rem; max-width: 1200px; }
    .hero {
        padding: 1.5rem 1.7rem; border-radius: 18px;
        background: linear-gradient(120deg, #172554 0%, #312e81 55%, #581c87 100%);
        border: 1px solid rgba(167,139,250,.35); margin-bottom: 1.2rem;
    }
    .hero h1 { color: #fff; margin: 0; font-size: 2.2rem; }
    .hero p { color: #dbeafe; margin: .45rem 0 0 0; }
    .metric-card {
        background: #121a2e; border: 1px solid #293653;
        border-radius: 14px; padding: 1rem 1.1rem; min-height: 104px;
    }
    .metric-label { color: #a5b4fc; font-size: .85rem; }
    .metric-value { color: #fff; font-size: 1.8rem; font-weight: 700; margin-top: .2rem; }
    .muted { color: #9ca3af; font-size: .9rem; }
    .finding-card {
        background: #111a2d; border: 1px solid #2b3956;
        border-radius: 14px; padding: 1rem 1.1rem; margin: .6rem 0;
    }
    div.stButton > button[kind="primary"] {
        border-radius: 10px; min-height: 3rem; font-weight: 700;
        background: linear-gradient(90deg, #6366f1, #8b5cf6); border: 0;
    }
    div[data-testid="stFileUploader"] {
        border: 1px dashed #536487; border-radius: 12px; padding: .5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🛠️ BuildBuddy</h1>
  <p>Your lightweight CI/CD troubleshooting assistant. Detect common build errors, understand the cause, and find the next debugging step.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    use_ai = st.toggle("Enable AI explanation", value=False)
    api_key = st.text_input(
        "Gemini API key",
        type="password",
        help="Optional. Basic error detection works without an API key.",
        disabled=not use_ai,
        value=os.getenv("GEMINI_API_KEY", "") if use_ai else "",
    )
    st.divider()
    st.markdown("**Supported log types**")
    st.caption("Python · pytest · Docker · dependency installation · configuration · network")
    st.divider()
    st.caption("Privacy: redact tokens, passwords, private URLs, and customer data before uploading.")
    st.caption("BuildBuddy suggests fixes but never edits your repository or deploys code.")

sample_dir = Path(__file__).resolve().parent.parent / "sample_logs"
sample_options = {
    "Choose a sample log…": None,
    "Missing dependency": sample_dir / "missing_dependency.log",
    "Failed tests": sample_dir / "failed_tests.log",
    "Docker build failure": sample_dir / "docker_failure.log",
}

left, right = st.columns([1.15, .85], gap="large")
with left:
    st.markdown("### 📄 Provide a build log")
    selected_sample = st.selectbox("Try a sample", list(sample_options.keys()))
    uploaded = st.file_uploader("Upload a .log or .txt file", type=["log", "txt"])
    default_text = ""
    if selected_sample != "Choose a sample log…":
        default_text = sample_options[selected_sample].read_text(encoding="utf-8", errors="replace")
    pasted = st.text_area(
        "Or paste your CI/CD output",
        value=default_text,
        height=270,
        placeholder="Paste GitHub Actions, pytest, Docker, or other build output…",
    )
    log_text = uploaded.getvalue().decode("utf-8", errors="replace") if uploaded else pasted
    analyze_clicked = st.button("🔍 Analyze build log", type="primary", use_container_width=True)

with right:
    st.markdown("### 💡 What BuildBuddy checks")
    st.markdown("""
    - **Dependencies:** missing packages and version conflicts
    - **Tests:** failed pytest runs and assertions
    - **Docker:** image and Dockerfile build errors
    - **Syntax:** Python syntax and indentation errors
    - **Configuration:** missing environment variables
    - **Network:** connection and DNS failures
    """)
    st.info("Tip: Start with one of the sample logs to see how the analyzer works.")

if analyze_clicked:
    if not log_text.strip():
        st.warning("Please upload a log, choose a sample, or paste some log text.")
    elif len(log_text) > 500_000:
        st.error("This demo accepts logs up to 500 KB. Please upload a smaller log.")
    else:
        findings = analyze_log(log_text)
        st.session_state["last_log"] = log_text
        st.session_state["last_findings"] = [f.to_dict() for f in findings]
        st.session_state["last_ai"] = None

if "last_findings" in st.session_state:
    findings_data = st.session_state["last_findings"]
    high = sum(f["severity"] == "High" for f in findings_data)
    medium = sum(f["severity"] == "Medium" for f in findings_data)
    categories = len({f["category"] for f in findings_data})

    st.divider()
    st.markdown("## 📊 Analysis overview")
    metrics = st.columns(4)
    metric_values = [
        ("Findings", len(findings_data)),
        ("High severity", high),
        ("Medium severity", medium),
        ("Categories", categories),
    ]
    for col, (label, value) in zip(metrics, metric_values):
        col.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("## 🧩 Detected issues")
    for index, finding in enumerate(findings_data, start=1):
        severity = finding["severity"]
        color = "#fb7185" if severity == "High" else "#fbbf24" if severity == "Medium" else "#93c5fd"
        with st.expander(f'{index}. {finding["title"]}  ·  {severity}', expanded=True):
            st.markdown(
                f'<span style="color:{color};font-weight:700">{severity.upper()}</span>'
                f' &nbsp; · &nbsp; **{finding["category"]}**',
                unsafe_allow_html=True,
            )
            st.markdown("**Matched log evidence**")
            st.code(finding["evidence"], language="text")
            st.markdown("**What it means**")
            st.write(finding["explanation"])
            st.markdown("**Suggested next steps**")
            st.write(finding["suggested_fix"])

    if use_ai:
        if not api_key.strip():
            st.info("Enter your Gemini API key in the sidebar to request an AI explanation.")
        else:
            if st.button("✨ Generate AI explanation"):
                with st.spinner("Reviewing the log…"):
                    st.session_state["last_ai"] = gemini_explanation(
                        st.session_state["last_log"],
                        [type("FindingProxy", (), item)() for item in findings_data],
                        api_key.strip(),
                    )
            if st.session_state.get("last_ai"):
                st.markdown("## ✨ AI-assisted explanation")
                st.write(st.session_state["last_ai"])

    st.download_button(
        "⬇️ Download findings as JSON",
        data=__import__("json").dumps(findings_data, indent=2),
        file_name="buildbuddy_analysis.json",
        mime="application/json",
    )

st.divider()
st.markdown(
    '<p class="muted">BuildBuddy uses explainable pattern matching for common errors. '
    'Optional AI explanations provide additional guidance and may be inaccurate. '
    'Always validate suggestions against your code and original build logs.</p>',
    unsafe_allow_html=True,
)
