import streamlit as st
from database.db import get_all_documents, get_quiz_history, get_flashcards
from utils.helpers import check_api_keys


def render():
    # ── Welcome banner ─────────────────────────────────────────────────────
    keys = check_api_keys()
    api_configured = keys["groq"] or keys["openai"]

    if not api_configured:
        st.warning("""
        ⚠️ **API Key Not Configured**

        EduGen AI needs a Groq (free) or OpenAI API key to generate quizzes and flashcards.

        1. Copy `.env.example` → `.env`
        2. Add your `GROQ_API_KEY` (free at [console.groq.com](https://console.groq.com))
        3. Restart: `streamlit run app.py`
        """)
    else:
        provider = "Groq (Free)" if keys["groq"] else "OpenAI"
        st.success(f"✅ AI Engine connected via **{provider}**")

    st.markdown("---")

    # ── Quick stats ───────────────────────────────────────────────────────
    docs = get_all_documents()
    history = get_quiz_history(limit=50)
    flashcards = get_flashcards()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div style="background:linear-gradient(135deg,#667eea,#764ba2);
            border-radius:16px;padding:20px;text-align:center;color:white;">
            <div style="font-size:36px;font-weight:800;">""" + str(len(docs)) + """</div>
            <div style="font-size:14px;opacity:0.9;margin-top:4px;">📚 Documents</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div style="background:linear-gradient(135deg,#f093fb,#f5576c);
            border-radius:16px;padding:20px;text-align:center;color:white;">
            <div style="font-size:36px;font-weight:800;">""" + str(len(history)) + """</div>
            <div style="font-size:14px;opacity:0.9;margin-top:4px;">🧠 Quizzes Taken</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("""<div style="background:linear-gradient(135deg,#4facfe,#00f2fe);
            border-radius:16px;padding:20px;text-align:center;color:white;">
            <div style="font-size:36px;font-weight:800;">""" + str(len(flashcards)) + """</div>
            <div style="font-size:14px;opacity:0.9;margin-top:4px;">🃏 Flashcards</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        if history:
            avg = sum(h["score"] / max(h["total_questions"], 1) * 100 for h in history) / len(history)
            avg_str = f"{avg:.0f}%"
        else:
            avg_str = "—"
        st.markdown("""<div style="background:linear-gradient(135deg,#43e97b,#38f9d7);
            border-radius:16px;padding:20px;text-align:center;color:white;">
            <div style="font-size:36px;font-weight:800;">""" + avg_str + """</div>
            <div style="font-size:14px;opacity:0.9;margin-top:4px;">🎯 Avg Score</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # ── Quick start ───────────────────────────────────────────────────────
    st.markdown("### 🚀 Quick Start")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        **Step 1: Upload** 📤
        Upload your lecture notes, textbooks, or any educational PDF/DOCX/TXT.
        """)
    with c2:
        st.markdown("""
        **Step 2: Generate** ⚡
        Create quizzes (MCQ, True/False, Fill-in-the-Blank) or flashcards with AI.
        """)
    with c3:
        st.markdown("""
        **Step 3: Study** 📖
        Take quizzes, flip flashcards, and track your progress in Analytics.
        """)

    # ── Recent activity ───────────────────────────────────────────────────
    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 📜 Recent Quizzes")
        if history:
            for h in history[:5]:
                pct = h["score"] / max(h["total_questions"], 1) * 100
                badge = "🟢" if pct >= 80 else "🟡" if pct >= 50 else "🔴"
                fname = h.get("filename", "Unknown") or "Unknown"
                st.markdown(f"{badge} **{fname[:30]}** · {h['quiz_type']} · {pct:.0f}%")
                st.caption(h["created_at"][:16])
        else:
            st.info("No quizzes taken yet. Head to the Quiz section!")

    with col_b:
        st.markdown("### 🃏 Recent Flashcards")
        if flashcards:
            for card in flashcards[:5]:
                st.markdown(f"📌 **{card['front_text'][:60]}...**")
                st.caption(f"Reviews: {card['review_count']} · {card.get('difficulty','medium').title()}")
        else:
            st.info("No flashcards yet. Generate some from your documents!")
