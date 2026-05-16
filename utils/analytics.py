import pandas as pd
from database.db import get_analytics_summary, get_quiz_history


def get_score_trend_df():
    """Return DataFrame for score trend chart."""
    history = get_quiz_history(limit=30)
    if not history:
        return pd.DataFrame(columns=["date", "score_pct", "quiz_type"])
    rows = []
    for h in history:
        pct = round(h["score"] / max(h["total_questions"], 1) * 100, 1)
        rows.append({
            "date": h["created_at"][:10],
            "score_pct": pct,
            "quiz_type": h["quiz_type"],
            "difficulty": h["difficulty"],
        })
    return pd.DataFrame(rows)


def get_summary_metrics():
    """Return dict of high-level metrics."""
    return get_analytics_summary()
