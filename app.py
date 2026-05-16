import streamlit as st
import sys
import os

# ── Path setup ───────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from database.db import init_db

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduGen AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialize DB ─────────────────────────────────────────────────────────────
init_db()

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background: linear-gradient(160deg, #0f172a 0%, #1e293b 40%, #0f172a 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

/* ── Main header area ── */
.main-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #1e40af 50%, #312e81 100%);
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 24px;
    border: 1px solid rgba(99,102,241,0.3);
    box-shadow: 0 20px 60px rgba(30,64,175,0.25);
}

.main-header h1 {
    font-size: 2rem;
    font-weight: 800;
    color: white !important;
    margin: 0;
    letter-spacing: -0.02em;
}

.main-header p {
    color: #93c5fd;
    margin: 6px 0 0 0;
    font-size: 15px;
}

/* ── Cards ── */
.card {
    background: rgba(30,41,59,0.8);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(10px);
}

/* ── Metric boxes ── */
[data-testid="metric-container"] {
    background: rgba(30,41,59,0.8) !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

[data-testid="metric-container"] label {
    color: #94a3b8 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(37,99,235,0.35) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(37,99,235,0.45) !important;
}

/* ── Input fields ── */
.stTextInput input, .stSelectbox select, .stTextArea textarea {
    background: #1e293b !important;
    border: 1px solid #475569 !important;
    color: #f1f5f9 !important;
    border-radius: 8px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.5) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: white !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: rgba(30,41,59,0.6) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    background: rgba(30,41,59,0.5) !important;
    border: 2px dashed #475569 !important;
    border-radius: 12px !important;
    color: #94a3b8 !important;
}

/* ── Alerts ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* ── Code ── */
code {
    font-family: 'JetBrains Mono', monospace !important;
    background: rgba(15,23,42,0.8) !important;
    color: #60a5fa !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
}

/* ── Charts ── */
[data-testid="stVegaLiteChart"] {
    background: transparent !important;
}

/* ── Divider ── */
hr {
    border-color: #334155 !important;
    margin: 24px 0 !important;
}

/* ── Sidebar radio nav ── */
.stRadio > label {
    font-weight: 600 !important;
    color: #94a3b8 !important;
    font-size: 12px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
    border-radius: 10px !important;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] {
    margin-top: 8px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f172a; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 12px 0 24px;">
        <div style="font-size:48px;">🎓</div>
        <div style="font-size:22px; font-weight:800; color:#f1f5f9; letter-spacing:-0.02em;">
            EduGen <span style="color:#60a5fa;">AI</span>
        </div>
        <div style="font-size:11px; color:#64748b; margin-top:4px; text-transform:uppercase; letter-spacing:0.1em;">
            Educational Content Generator
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**NAVIGATION**")

    page = st.radio(
        "Go to",
        ["🏠 Dashboard", "📤 Upload", "🧠 Quiz", "🃏 Flashcards", "📊 Analytics"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("**QUICK TIPS**")
    st.caption("• Use Groq API for free AI generation")
    st.caption("• Upload PDF, DOCX, or TXT files")
    st.caption("• Review flashcards daily for best retention")

    st.markdown("---")
    from utils.helpers import check_api_keys
    keys = check_api_keys()
    if keys["groq"]:
        st.success("⚡ Groq API connected")
    elif keys["openai"]:
        st.success("🤖 OpenAI API connected")
    else:
        st.error("🔑 No API key found")
        st.caption("Add GROQ_API_KEY to .env")


# ── Page headers ─────────────────────────────────────────────────────────────
page_meta = {
    "🏠 Dashboard": ("🏠 Dashboard", "Your learning overview and recent activity"),
    "📤 Upload": ("📤 Upload Documents", "Add study materials to your library"),
    "🧠 Quiz": ("🧠 Quiz Generator", "Test your knowledge with AI-generated questions"),
    "🃏 Flashcards": ("🃏 Flashcard Studio", "Create and review interactive flashcards"),
    "📊 Analytics": ("📊 Learning Analytics", "Track your progress and identify gaps"),
}

title, subtitle = page_meta.get(page, ("EduGen AI", ""))
st.markdown(f"""
<div class="main-header">
    <h1>{title}</h1>
    <p>{subtitle}</p>
</div>
""", unsafe_allow_html=True)


# ── Route to page ─────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    from components.dashboard import render
    render()

elif page == "📤 Upload":
    from components.upload import render
    render()

elif page == "🧠 Quiz":
    from components.quiz import render
    render()

elif page == "🃏 Flashcards":
    from components.flashcards import render
    render()

elif page == "📊 Analytics":
    from components.analytics_page import render
    render()
