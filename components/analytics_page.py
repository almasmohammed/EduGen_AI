import streamlit as st
import pandas as pd
from utils.analytics import get_score_trend_df, get_summary_metrics


def render():
    st.markdown("## 📊 Analytics & Progress")
    st.markdown("Track your learning journey and identify areas for improvement.")

    metrics = get_summary_metrics()

    # ── KPI cards ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Documents", metrics["total_docs"])
    with col2:
        st.metric("🧠 Quizzes Taken", metrics["total_quizzes"])
    with col3:
        st.metric("🃏 Flashcards", metrics["total_flashcards"])
    with col4:
        avg = metrics["avg_score"]
        delta_color = "normal" if avg >= 60 else "inverse"
        st.metric("🎯 Avg. Score", f"{avg:.1f}%", delta_color=delta_color)

    st.markdown("---")

    # ── Charts ────────────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📈 Score Trend")
        df = get_score_trend_df()
        if df.empty:
            st.info("Take some quizzes to see your score trend!")
        else:
            df_chart = df[["date", "score_pct"]].copy()
            df_chart.columns = ["Date", "Score (%)"]
            st.line_chart(df_chart.set_index("Date"), use_container_width=True)

    with col_right:
        st.markdown("### 🍩 Quiz Types Distribution")
        topic_data = metrics.get("topic_dist", [])
        if topic_data:
            df_topics = pd.DataFrame(topic_data)
            df_topics.columns = ["Quiz Type", "Count"]
            st.bar_chart(df_topics.set_index("Quiz Type"), use_container_width=True)
        else:
            st.info("Generate quizzes to see distribution.")

    st.markdown("---")

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        st.markdown("### 🎯 Difficulty Distribution")
        diff_data = metrics.get("difficulty_dist", [])
        if diff_data:
            df_diff = pd.DataFrame(diff_data)
            df_diff.columns = ["Difficulty", "Count"]
            colors = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
            for _, row in df_diff.iterrows():
                icon = colors.get(row["Difficulty"], "⚪")
                st.markdown(f"{icon} **{row['Difficulty'].title()}** — {int(row['Count'])} quiz(zes)")
        else:
            st.info("No quiz data yet.")

    with col_r2:
        st.markdown("### 📅 Recent Activity")
        recent = metrics.get("recent_quizzes", [])
        if recent:
            for r in recent[:5]:
                pct = r.get("avg_score", 0)
                badge = "🟢" if pct >= 80 else "🟡" if pct >= 50 else "🔴"
                st.markdown(f"{badge} **{r['day']}** — {int(r['count'])} quiz(zes), avg {pct:.0f}%")
        else:
            st.info("No recent activity.")

    st.markdown("---")
    st.markdown("### 💡 Learning Tips")
    tips = [
        ("📅", "Consistent daily review beats cramming — aim for 20 min/day"),
        ("🔁", "Spaced repetition: revisit hard flashcards more frequently"),
        ("📈", "Target >80% on easy quizzes before moving to harder ones"),
        ("🎯", "Focus on topics where your score is below 60%"),
        ("✍️", "Use Fill-in-the-Blank for deeper recall practice"),
    ]
    for icon, tip in tips:
        st.markdown(f"{icon} {tip}")
