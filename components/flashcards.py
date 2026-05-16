import streamlit as st
from database.db import (
    get_all_documents, get_document_content,
    save_flashcards, get_flashcards, update_flashcard_review, delete_flashcard
)
from utils.flashcard_generator import generate_flashcards


def render():
    st.markdown("## 🃏 Flashcard Generator")
    st.markdown("Transform your study materials into interactive flashcards for effective memorization.")

    tab1, tab2 = st.tabs(["✨ Generate Flashcards", "📖 Review Flashcards"])

    with tab1:
        _generate_tab()

    with tab2:
        _review_tab()


def _generate_tab():
    docs = get_all_documents()
    if not docs:
        st.warning("⚠️ No documents uploaded. Go to **Upload** first.")
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        doc_options = {f"{d['filename']} ({d['word_count']:,} words)": d["id"] for d in docs}
        selected_label = st.selectbox("📄 Select Document", list(doc_options.keys()))
        selected_id = doc_options[selected_label]
    with col2:
        num_cards = st.slider("🃏 Number of cards", 5, 20, 10)

    if st.button("✨ Generate Flashcards", type="primary", use_container_width=True):
        content = get_document_content(selected_id)
        if not content:
            st.error("❌ Document content not found.")
            return

        with st.spinner("🤖 Creating flashcards..."):
            try:
                cards = generate_flashcards(content, num_cards)
                save_flashcards(selected_id, cards)
                st.success(f"✅ Generated **{len(cards)}** flashcards!")
                st.session_state["generated_cards"] = cards
            except Exception as e:
                st.error(f"❌ Error: {e}")
                return

    # Preview generated cards
    if "generated_cards" in st.session_state and st.session_state["generated_cards"]:
        cards = st.session_state["generated_cards"]
        st.markdown(f"### 👀 Preview — {len(cards)} Cards Generated")

        cols = st.columns(2)
        for i, card in enumerate(cards):
            with cols[i % 2]:
                diff_color = {"easy": "#22c55e", "medium": "#f59e0b", "hard": "#ef4444"}.get(card.get("difficulty", "medium"), "#6b7280")
                st.markdown(f"""
                <div style="border:1px solid #e5e7eb; border-radius:12px; padding:16px; margin-bottom:12px;
                            background:linear-gradient(135deg, #f8faff 0%, #eff6ff 100%);">
                    <div style="font-size:11px; color:{diff_color}; font-weight:700; text-transform:uppercase;
                                letter-spacing:0.05em; margin-bottom:8px;">
                        {card.get('topic','General')} · {card.get('difficulty','medium')}
                    </div>
                    <div style="font-weight:600; color:#1e293b; margin-bottom:10px; font-size:15px;">
                        Q: {card['front']}
                    </div>
                    <div style="color:#475569; font-size:14px; border-top:1px solid #e2e8f0; padding-top:10px;">
                        A: {card['back']}
                    </div>
                </div>
                """, unsafe_allow_html=True)


def _review_tab():
    all_cards = get_flashcards()

    if not all_cards:
        st.info("📭 No flashcards yet. Generate some from the first tab!")
        return

    st.markdown(f"**{len(all_cards)} flashcards** in your deck")

    # Filter by topic
    topics = list(set(c.get("topic", "General") for c in all_cards))
    topic_filter = st.selectbox("🏷️ Filter by topic", ["All"] + sorted(topics))

    if topic_filter != "All":
        all_cards = [c for c in all_cards if c.get("topic") == topic_filter]

    if "card_index" not in st.session_state:
        st.session_state["card_index"] = 0
    if "show_answer" not in st.session_state:
        st.session_state["show_answer"] = False

    if not all_cards:
        st.info("No cards match this filter.")
        return

    # Clamp index
    idx = st.session_state["card_index"] % len(all_cards)
    card = all_cards[idx]

    # ── Flashcard UI ───────────────────────────────────────────────────────
    st.markdown(f"**Card {idx + 1} of {len(all_cards)}**")

    diff_color = {"easy": "#22c55e", "medium": "#f59e0b", "hard": "#ef4444"}.get(card.get("difficulty", "medium"), "#6b7280")

    if not st.session_state["show_answer"]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
            border-radius: 20px; padding: 50px 40px; text-align: center;
            min-height: 220px; display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            box-shadow: 0 20px 60px rgba(37,99,235,0.3);
        ">
            <div style="font-size:13px; color:#93c5fd; font-weight:600; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:20px;">
                {card.get('topic', 'General')} · QUESTION
            </div>
            <div style="font-size:22px; font-weight:700; color:white; line-height:1.4;">
                {card['front_text']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #064e3b 0%, #059669 100%);
            border-radius: 20px; padding: 50px 40px; text-align: center;
            min-height: 220px; display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            box-shadow: 0 20px 60px rgba(5,150,105,0.3);
        ">
            <div style="font-size:13px; color:#6ee7b7; font-weight:600; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:20px;">
                {card.get('topic', 'General')} · ANSWER
            </div>
            <div style="font-size:20px; font-weight:600; color:white; line-height:1.5;">
                {card['back_text']}
            </div>
            <div style="margin-top:16px; font-size:12px; color:{diff_color}; font-weight:700;
                        background:rgba(255,255,255,0.15); padding:4px 12px; border-radius:20px;">
                {card.get('difficulty','medium').upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⬅️ Prev", use_container_width=True):
            st.session_state["card_index"] = (idx - 1) % len(all_cards)
            st.session_state["show_answer"] = False
            st.rerun()
    with col2:
        if st.button("🔄 Flip", use_container_width=True, type="primary"):
            st.session_state["show_answer"] = not st.session_state["show_answer"]
            if st.session_state["show_answer"]:
                update_flashcard_review(card["id"])
            st.rerun()
    with col3:
        if st.button("➡️ Next", use_container_width=True):
            st.session_state["card_index"] = (idx + 1) % len(all_cards)
            st.session_state["show_answer"] = False
            st.rerun()
    with col4:
        st.metric("Reviews", card.get("review_count", 0))
    with col5:
        if st.button("🗑️ Delete", use_container_width=True):
            delete_flashcard(card["id"])
            st.session_state["card_index"] = 0
            st.session_state["show_answer"] = False
            st.rerun()

    # Progress bar
    st.progress((idx + 1) / len(all_cards))
