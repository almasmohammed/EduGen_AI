-- EduGen AI Database Schema

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS uploaded_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 1,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    content_preview TEXT,
    full_content TEXT,
    word_count INTEGER DEFAULT 0,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS quiz_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 1,
    document_id INTEGER,
    quiz_type TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    questions_json TEXT NOT NULL,
    score INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    time_taken INTEGER DEFAULT 0,
    topic TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (document_id) REFERENCES uploaded_documents(id)
);

CREATE TABLE IF NOT EXISTS flashcards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 1,
    document_id INTEGER,
    front_text TEXT NOT NULL,
    back_text TEXT NOT NULL,
    topic TEXT,
    difficulty TEXT DEFAULT 'medium',
    review_count INTEGER DEFAULT 0,
    last_reviewed TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (document_id) REFERENCES uploaded_documents(id)
);

CREATE TABLE IF NOT EXISTS progress_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 1,
    date DATE DEFAULT (date('now')),
    quizzes_taken INTEGER DEFAULT 0,
    flashcards_reviewed INTEGER DEFAULT 0,
    avg_score REAL DEFAULT 0.0,
    study_time_mins INTEGER DEFAULT 0,
    topics_covered TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Default user
INSERT OR IGNORE INTO users (id, username, email) VALUES (1, 'student', 'student@edugen.ai');
