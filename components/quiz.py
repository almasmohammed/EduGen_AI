import streamlit as st
import time
from database.db import get_all_documents, get_document_content, save_quiz, get_quiz_history
from utils.quiz_generator import generate_quiz
from utils.helpers import format_score_badge


def render():
    st.markdown("## 🧠 Quiz Generator")
    st.markdown("Generate intelligent quizzes from your uploaded study materials.")

    # ── Configuration ─────────────────────────────────────────────────────
    docs = get_all_documents()

    if not docs:
        st.warning("⚠️ No documents uploaded yet. Go to **Upload** to add study materials first.")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        doc_options = {f"{d['filename']} ({d['word_count']:,} words)": d["id"] for d in docs}
        selected_doc_label = st.selectbox("📄 Select Document", list(doc_options.keys()))
        selected_doc_id = doc_options[selected_doc_label]

    with col2:
        quiz_type = st.selectbox(
            "📝 Quiz Type",
            ["mcq", "truefalse", "fillblanks"],
            format_func=lambda x: {"mcq": "🔤 Multiple Choice", "truefalse": "✅ True / False", "fillblanks": "✏️ Fill in the Blanks"}[x],
        )

    with col3:
        difficulty = st.selectbox(
            "🎯 Difficulty",
            ["easy", "medium", "hard"],
            index=1,
            format_func=lambda x: {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}[x],
        )

    with col4:
        num_q = st.slider("❓ Questions", min_value=3, max_value=15, value=5)

    # ── Generate button ───────────────────────────────────────────────────
    if st.button("⚡ Generate Quiz", type="primary", use_container_width=True):
        content = get_document_content(selected_doc_id)
        if not content:
            st.error("❌ Document content not found.")
            return

        with st.spinner("🤖 AI is crafting your quiz..."):
            try:
                questions = generate_quiz(content, quiz_type, difficulty, num_q)
                st.session_state["current_quiz"] = {
                    "questions": questions,
                    "quiz_type": quiz_type,
                    "difficulty": difficulty,
                    "doc_id": selected_doc_id,
                    "answers": {},
                    "submitted": False,
                    "start_time": time.time(),
                }
                st.success(f"✅ Generated **{len(questions)}** questions!")
            except Exception as e:
                st.error(f"❌ Error generating quiz: {e}")
                st.info("💡 Check your API key in .env file. Get a free key at console.groq.com")
                return

    # ── Quiz display ──────────────────────────────────────────────────────
    if "current_quiz" not in st.session_state or not st.session_state["current_quiz"]:
        _show_quiz_history()
        return

    quiz = st.session_state["current_quiz"]
    questions = quiz["questions"]
    quiz_type = quiz["quiz_type"]

    if not quiz["submitted"]:
        _render_quiz_questions(quiz, questions, quiz_type)
    else:
        _render_quiz_results(quiz, questions, quiz_type)


def _render_quiz_questions(quiz, questions, quiz_type):
    st.markdown("---")
    st.markdown(f"### 📋 Quiz — {len(questions)} Questions · {quiz['difficulty'].title()} Difficulty")

    for i, q in enumerate(questions):
        with st.container():
            st.markdown(f"**Q{i+1}. {q['question']}**")

            if quiz_type == "mcq":
                options = q.get("options", [])
                answer = st.radio(
                    f"Select answer for Q{i+1}",
                    options,
                    key=f"q_{i}",
                    label_visibility="collapsed",
                )
                quiz["answers"][i] = answer

            elif quiz_type == "truefalse":
                answer = st.radio(
                    f"Select answer for Q{i+1}",
                    ["True", "False"],
                    key=f"q_{i}",
                    label_visibility="collapsed",
                )
                quiz["answers"][i] = answer

            elif quiz_type == "fillblanks":
                hint = q.get("hint", "")
                placeholder = f"Hint: {hint}" if hint else "Type your answer..."
                answer = st.text_input(
                    f"Answer for Q{i+1}",
                    key=f"q_{i}",
                    placeholder=placeholder,
                    label_visibility="collapsed",
                )
                quiz["answers"][i] = answer

            st.markdown("")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📤 Submit Quiz", type="primary", use_container_width=True):
            quiz["submitted"] = True
            quiz["end_time"] = time.time()
            st.rerun()
    with col2:
        if st.button("🔄 New Quiz", use_container_width=True):
            del st.session_state["current_quiz"]
            st.rerun()


def _render_quiz_results(quiz, questions, quiz_type):
    st.markdown("---")

    answers = quiz.get("answers", {})
    score = 0
    time_taken = int(quiz.get("end_time", 0) - quiz.get("start_time", 0))

    # Calculate score
    for i, q in enumerate(questions):
        user_ans = str(answers.get(i, "")).strip().lower()
        correct_ans = str(q.get("answer", "")).strip().lower()
        if quiz_type == "mcq":
            if user_ans == correct_ans:
                score += 1
        elif quiz_type == "truefalse":
            if user_ans == correct_ans:
                score += 1
        elif quiz_type == "fillblanks":
            if user_ans and (user_ans in correct_ans or correct_ans in user_ans):
                score += 1

    pct = score / max(len(questions), 1) * 100

    # Save to DB
    save_quiz(
        quiz["doc_id"], quiz_type, quiz["difficulty"],
        questions, score, len(questions)
    )

    # Results header
    st.markdown("## 🏆 Quiz Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", format_score_badge(score, len(questions)))
    with col2:
        st.metric("Percentage", f"{pct:.0f}%")
    with col3:
        st.metric("Time", f"{time_taken}s")

    if pct >= 80:
        st.success("🌟 Excellent work! You've mastered this material!")
    elif pct >= 60:
        st.info("👍 Good effort! Review the incorrect answers below.")
    else:
        st.warning("📚 Keep studying! Focus on the explanations below.")

    # Detailed review
    st.markdown("### 📝 Question Review")
    for i, q in enumerate(questions):
        user_ans = str(answers.get(i, "")).strip()
        correct_ans = str(q.get("answer", "")).strip()

        is_correct = False
        if quiz_type in ("mcq", "truefalse"):
            is_correct = user_ans.lower() == correct_ans.lower()
        elif quiz_type == "fillblanks":
            is_correct = bool(user_ans) and (user_ans.lower() in correct_ans.lower() or correct_ans.lower() in user_ans.lower())

        icon = "✅" if is_correct else "❌"
        with st.expander(f"{icon} Q{i+1}: {q['question'][:80]}...", expanded=not is_correct):
            if not is_correct:
                st.markdown(f"**Your answer:** {user_ans or '*(no answer)*'}")
            st.markdown(f"**Correct answer:** {correct_ans}")
            if q.get("explanation"):
                st.info(f"💡 {q['explanation']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Take Another Quiz", type="primary", use_container_width=True):
            del st.session_state["current_quiz"]
            st.rerun()


def _show_quiz_history():
    st.markdown("---")
    st.markdown("### 📜 Recent Quiz History")
    history = get_quiz_history(limit=10)
    if not history:
        st.info("No quizzes taken yet. Generate your first quiz above!")
        return

    for h in history[:5]:
        pct = h["score"] / max(h["total_questions"], 1) * 100
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.markdown(f"📄 {h.get('filename', 'Unknown doc')}")
            st.caption(h["created_at"][:16])
        with col2:
            st.caption(h["quiz_type"].upper())
        with col3:
            st.caption(h["difficulty"].title())
        with col4:
            badge = "🟢" if pct >= 80 else "🟡" if pct >= 50 else "🔴"
            st.markdown(f"{badge} {h['score']}/{h['total_questions']}")
        st.divider()
