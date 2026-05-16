import os
import json
import re
from typing import Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def _get_llm():
    """Return an LLM — prefers Groq (free), falls back to OpenAI."""
    groq_key = os.getenv("GROQ_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")

    if groq_key:
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=groq_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.4,
        )
    elif openai_key:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            api_key=openai_key,
            model_name="gpt-3.5-turbo",
            temperature=0.4,
        )
    else:
        raise EnvironmentError(
            "No API key found. Set GROQ_API_KEY or OPENAI_API_KEY in your .env file."
        )


# ─── Prompt templates ──────────────────────────────────────────────────────

MCQ_PROMPT = PromptTemplate.from_template(
    """You are an expert educational quiz creator.

Based on the following educational content, generate exactly {num_questions} multiple-choice questions at {difficulty} difficulty level.

Content:
\"\"\"
{content}
\"\"\"

Return ONLY a valid JSON array (no markdown, no extra text) like this:
[
  {{
    "question": "What is ...?",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A) ...",
    "explanation": "Brief explanation why A is correct."
  }}
]

Rules:
- Each question must have exactly 4 options labeled A) B) C) D)
- The answer must be one of the options verbatim
- Vary question types (definition, application, comparison)
- Difficulty: {difficulty} (easy=factual recall, medium=comprehension, hard=analysis/synthesis)
- Do NOT include any text before or after the JSON array
"""
)

TF_PROMPT = PromptTemplate.from_template(
    """You are an expert educational quiz creator.

Based on the content below, generate exactly {num_questions} True/False questions at {difficulty} difficulty.

Content:
\"\"\"
{content}
\"\"\"

Return ONLY a valid JSON array:
[
  {{
    "question": "Statement that is true or false...",
    "answer": "True",
    "explanation": "Brief explanation."
  }}
]

- Roughly half should be True, half False
- Difficulty: {difficulty}
- Do NOT include any text before or after the JSON array
"""
)

FIB_PROMPT = PromptTemplate.from_template(
    """You are an expert educational quiz creator.

Based on the content below, generate exactly {num_questions} fill-in-the-blank questions at {difficulty} difficulty.

Content:
\"\"\"
{content}
\"\"\"

Return ONLY a valid JSON array:
[
  {{
    "question": "The _____ is responsible for...",
    "answer": "exact word or phrase",
    "hint": "Optional short hint",
    "explanation": "Brief explanation."
  }}
]

- Use _____ (5 underscores) for the blank
- The answer should be a specific word or short phrase from the content
- Difficulty: {difficulty}
- Do NOT include any text before or after the JSON array
"""
)


def _clean_json(raw: str) -> str:
    """Strip markdown fences and find the JSON array."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    # Find first [ and last ]
    start = raw.find("[")
    end = raw.rfind("]")
    if start != -1 and end != -1:
        return raw[start : end + 1]
    return raw


def generate_quiz(
    content: str,
    quiz_type: str = "mcq",
    difficulty: str = "medium",
    num_questions: int = 5,
) -> list[dict]:
    """
    Generate quiz questions from educational content.

    Args:
        content: Extracted text from a document
        quiz_type: 'mcq', 'truefalse', or 'fillblanks'
        difficulty: 'easy', 'medium', or 'hard'
        num_questions: Number of questions to generate

    Returns:
        List of question dicts
    """
    if not content or len(content.strip()) < 100:
        raise ValueError("Content is too short to generate meaningful questions. Please upload a longer document.")

    # Trim content to avoid token limits
    max_chars = 4000
    trimmed = content[:max_chars] if len(content) > max_chars else content

    llm = _get_llm()
    parser = StrOutputParser()

    prompt_map = {
        "mcq": MCQ_PROMPT,
        "truefalse": TF_PROMPT,
        "fillblanks": FIB_PROMPT,
    }

    prompt = prompt_map.get(quiz_type, MCQ_PROMPT)
    chain = prompt | llm | parser

    raw = chain.invoke({
        "content": trimmed,
        "difficulty": difficulty,
        "num_questions": num_questions,
    })

    cleaned = _clean_json(raw)

    try:
        questions = json.loads(cleaned)
        if not isinstance(questions, list):
            raise ValueError("Response was not a JSON array.")
        return questions
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse AI response as JSON: {e}\n\nRaw response:\n{raw[:500]}")
