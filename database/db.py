import sqlite3
import os
import json
from datetime import datetime, date
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "edugen.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection():
    """Get SQLite connection with row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Initialize database from schema."""
    conn = get_connection()
    try:
        with open(SCHEMA_PATH, "r") as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
    except Exception as e:
        print(f"DB init error: {e}")
    finally:
        conn.close()


# ─── Documents ───────────────────────────────────────────────────────────────

def save_document(filename: str, file_type: str, content: str) -> int:
    conn = get_connection()
    try:
        preview = content[:500] if content else ""
        word_count = len(content.split()) if content else 0
        cur = conn.execute(
            """INSERT INTO uploaded_documents
               (user_id, filename, file_type, content_preview, full_content, word_count)
               VALUES (1, ?, ?, ?, ?, ?)""",
            (filename, file_type, preview, content, word_count),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_all_documents():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, filename, file_type, word_count, upload_time FROM uploaded_documents ORDER BY upload_time DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_document_content(doc_id: int) -> str:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT full_content FROM uploaded_documents WHERE id=?", (doc_id,)
        ).fetchone()
        return row["full_content"] if row else ""
    finally:
        conn.close()


def delete_document(doc_id: int):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM uploaded_documents WHERE id=?", (doc_id,))
        conn.commit()
    finally:
        conn.close()


# ─── Quiz ────────────────────────────────────────────────────────────────────

def save_quiz(doc_id, quiz_type, difficulty, questions, score, total, topic=""):
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO quiz_history
               (user_id, document_id, quiz_type, difficulty, questions_json, score, total_questions, topic)
               VALUES (1, ?, ?, ?, ?, ?, ?, ?)""",
            (doc_id, quiz_type, difficulty, json.dumps(questions), score, total, topic),
        )
        conn.commit()
        _update_progress(conn, quizzes=1, avg_score=score / max(total, 1) * 100)
    finally:
        conn.close()


def get_quiz_history(limit=20):
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT qh.*, ud.filename FROM quiz_history qh
               LEFT JOIN uploaded_documents ud ON qh.document_id = ud.id
               ORDER BY qh.created_at DESC LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ─── Flashcards ──────────────────────────────────────────────────────────────

def save_flashcards(doc_id, cards: list, topic=""):
    conn = get_connection()
    try:
        for card in cards:
            conn.execute(
                """INSERT INTO flashcards
                   (user_id, document_id, front_text, back_text, topic, difficulty)
                   VALUES (1, ?, ?, ?, ?, ?)""",
                (doc_id, card["front"], card["back"], topic, card.get("difficulty", "medium")),
            )
        conn.commit()
    finally:
        conn.close()


def get_flashcards(doc_id=None):
    conn = get_connection()
    try:
        if doc_id:
            rows = conn.execute(
                "SELECT * FROM flashcards WHERE document_id=? ORDER BY created_at DESC", (doc_id,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM flashcards ORDER BY created_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_flashcard_review(card_id: int):
    conn = get_connection()
    try:
        conn.execute(
            "UPDATE flashcards SET review_count=review_count+1, last_reviewed=? WHERE id=?",
            (datetime.now(), card_id),
        )
        conn.commit()
        _update_progress(conn, flashcards=1)
    finally:
        conn.close()


def delete_flashcard(card_id: int):
    conn = get_connection()
    try:
        conn.execute("DELETE FROM flashcards WHERE id=?", (card_id,))
        conn.commit()
    finally:
        conn.close()


# ─── Analytics ───────────────────────────────────────────────────────────────

def get_analytics_summary():
    conn = get_connection()
    try:
        docs = conn.execute("SELECT COUNT(*) as c FROM uploaded_documents").fetchone()["c"]
        quizzes = conn.execute("SELECT COUNT(*) as c FROM quiz_history").fetchone()["c"]
        cards = conn.execute("SELECT COUNT(*) as c FROM flashcards").fetchone()["c"]
        avg_score_row = conn.execute(
            "SELECT AVG(CAST(score AS REAL)/NULLIF(total_questions,0)*100) as avg FROM quiz_history"
        ).fetchone()
        avg_score = round(avg_score_row["avg"] or 0, 1)

        recent_quizzes = conn.execute(
            """SELECT date(created_at) as day, AVG(CAST(score AS REAL)/NULLIF(total_questions,0)*100) as avg_score,
               COUNT(*) as count FROM quiz_history GROUP BY day ORDER BY day DESC LIMIT 7"""
        ).fetchall()

        topic_dist = conn.execute(
            "SELECT quiz_type, COUNT(*) as count FROM quiz_history GROUP BY quiz_type"
        ).fetchall()

        difficulty_dist = conn.execute(
            "SELECT difficulty, COUNT(*) as count FROM quiz_history GROUP BY difficulty"
        ).fetchall()

        return {
            "total_docs": docs,
            "total_quizzes": quizzes,
            "total_flashcards": cards,
            "avg_score": avg_score,
            "recent_quizzes": [dict(r) for r in recent_quizzes],
            "topic_dist": [dict(r) for r in topic_dist],
            "difficulty_dist": [dict(r) for r in difficulty_dist],
        }
    finally:
        conn.close()


def _update_progress(conn, quizzes=0, flashcards=0, avg_score=0.0):
    today = date.today().isoformat()
    existing = conn.execute(
        "SELECT * FROM progress_tracking WHERE user_id=1 AND date=?", (today,)
    ).fetchone()
    if existing:
        conn.execute(
            """UPDATE progress_tracking SET
               quizzes_taken=quizzes_taken+?,
               flashcards_reviewed=flashcards_reviewed+?,
               avg_score=(avg_score+?)/2
               WHERE user_id=1 AND date=?""",
            (quizzes, flashcards, avg_score, today),
        )
    else:
        conn.execute(
            """INSERT INTO progress_tracking (user_id, date, quizzes_taken, flashcards_reviewed, avg_score)
               VALUES (1, ?, ?, ?, ?)""",
            (today, quizzes, flashcards, avg_score),
        )
    conn.commit()
