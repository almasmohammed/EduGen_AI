# 🎓 EduGen AI — Educational Content Generator

> An AI-powered study companion that transforms your documents into quizzes, flashcards, and learning insights.

![EduGen AI](https://via.placeholder.com/800x400/1e3a5f/60a5fa?text=EduGen+AI+Screenshot)

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📤 Document Upload | PDF, DOCX, TXT, Markdown |
| 🧠 Quiz Generator | MCQ, True/False, Fill-in-the-Blank · Easy/Medium/Hard |
| 🃏 Flashcards | AI-generated with interactive flip UI |
| 📊 Analytics | Score trends, topic distribution, progress charts |
| 💾 SQLite Database | Persistent storage for all study data |

---

## 🚀 Quick Start

### 1. Clone or extract the project

```bash
cd EduGen-AI
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
# Copy the example env file
cp .env.example .env
```

Open `.env` and add your API key:

```env
# Get a FREE key at https://console.groq.com
GROQ_API_KEY=gsk_your_actual_key_here
```

> **Groq is completely free** and much faster than OpenAI for this use case. Sign up at [console.groq.com](https://console.groq.com) and create an API key in seconds.

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** 🎉

---

## 📁 Project Structure

```
EduGen-AI/
│
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
├── edugen.db                 # SQLite database (auto-created)
│
├── database/
│   ├── db.py                 # All DB operations
│   └── schema.sql            # Database schema
│
├── utils/
│   ├── pdf_parser.py         # PDF text extraction
│   ├── docx_parser.py        # DOCX text extraction
│   ├── quiz_generator.py     # AI quiz generation via LangChain
│   ├── flashcard_generator.py # AI flashcard generation
│   ├── analytics.py          # Analytics data helpers
│   └── helpers.py            # Shared utilities
│
├── pages/
│   ├── dashboard.py          # Home dashboard
│   ├── upload.py             # Document upload & library
│   ├── quiz.py               # Quiz generation & taking
│   ├── flashcards.py         # Flashcard generation & review
│   └── analytics_page.py     # Progress analytics
│
├── assets/                   # Static assets
└── sample_docs/
    └── sample_ml_notes.txt   # Sample document to try
```

---

## 🔑 API Key Setup

### Option A: Groq (Recommended — Free)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)
5. Paste in your `.env` file as `GROQ_API_KEY=gsk_...`

### Option B: OpenAI (Paid)

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create an API key
3. Paste in your `.env` file as `OPENAI_API_KEY=sk-...`

---

## 📖 How to Use

### Step 1: Upload a Document
- Click **Upload** in the sidebar
- Choose a PDF, DOCX, or TXT file
- Click **Save to Library**

### Step 2: Generate a Quiz
- Click **Quiz** in the sidebar
- Select your document, quiz type, difficulty, and question count
- Click **Generate Quiz** and answer the questions

### Step 3: Generate Flashcards
- Click **Flashcards** in the sidebar
- Select a document and number of cards
- Click **Generate Flashcards**
- Go to **Review Flashcards** to flip through them

### Step 4: Track Progress
- Click **Analytics** to see your score trends and study habits

---

## 🛠 VS Code Setup

1. Open the `EduGen-AI` folder in VS Code
2. Install the **Python** extension
3. Select the virtual environment interpreter (`venv/`)
4. Open the integrated terminal: `Ctrl+` ` `
5. Run: `streamlit run app.py`

---

## 🚀 Deployment (Streamlit Cloud)

1. Push the project to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path**: `app.py`
5. Add secrets in **Settings → Secrets**:
   ```
   GROQ_API_KEY = "your_key_here"
   ```

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| `No API key found` | Check your `.env` file has `GROQ_API_KEY=...` |
| `PDF has no extractable text` | Try a text-based PDF (not scanned images) |
| `ImportError: PyPDF2` | Run `pip install -r requirements.txt` again |
| `streamlit: command not found` | Activate your venv first |
| JSON parse error from AI | Retry — LLM occasionally returns malformed output |

---

## 👨‍💻 Tech Stack

- **Frontend**: Streamlit with custom CSS
- **AI/LLM**: LangChain + Groq (Llama 3.1) / OpenAI (GPT-3.5)
- **Document Processing**: PyPDF2, python-docx
- **Database**: SQLite (via Python's built-in `sqlite3`)
- **Data**: Pandas

---

## 📝 Academic Context

Built for **EduGen AI** project (Week 1-2 milestone) — Track A of the Educational Content Generator AI Agent Development Project.

**Covers:**
- ✅ Document-to-quiz chatbot
- ✅ Multiple quiz formats (MCQ, True/False, Fill-in-the-Blank)
- ✅ Difficulty levels (Easy, Medium, Hard)
- ✅ Flashcard generation and review
- ✅ SQLite study materials database (users, documents, quiz_history, flashcards, progress_tracking)
- ✅ Streamlit dashboard with sidebar navigation
- ✅ Progress analytics and charts
- ✅ Deployed and runnable with `streamlit run app.py`
