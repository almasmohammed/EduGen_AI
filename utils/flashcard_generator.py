import os
import json
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def _get_llm():
    groq_key = os.getenv("GROQ_API_KEY", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")

    if groq_key:
        from langchain_groq import ChatGroq
        return ChatGroq(api_key=groq_key, model_name="llama-3.1-8b-instant", temperature=0.3)
    elif openai_key:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(api_key=openai_key, model_name="gpt-3.5-turbo", temperature=0.3)
    else:
        raise EnvironmentError("No API key found. Set GROQ_API_KEY or OPENAI_API_KEY in your .env file.")


FLASHCARD_PROMPT = PromptTemplate.from_template(
    """You are an expert study material creator specializing in flashcards.

Based on the following educational content, generate exactly {num_cards} flashcards for effective studying.

Content:
\"\"\"
{content}
\"\"\"

Return ONLY a valid JSON array (no markdown, no extra text):
[
  {{
    "front": "Clear, concise question or term",
    "back": "Comprehensive answer or definition",
    "difficulty": "easy|medium|hard",
    "topic": "Brief topic label (1-3 words)"
  }}
]

Guidelines:
- Front: A question, term, or concept prompt (keep it short and focused)
- Back: A clear, complete answer or explanation
- Vary difficulty: some easy (definitions), some medium (applications), some hard (analysis)
- Cover different aspects of the content
- Do NOT include any text before or after the JSON array
"""
)


def _clean_json(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    start = raw.find("[")
    end = raw.rfind("]")
    if start != -1 and end != -1:
        return raw[start : end + 1]
    return raw


def generate_flashcards(content: str, num_cards: int = 10) -> list[dict]:
    """
    Generate flashcards from educational content.

    Args:
        content: Extracted document text
        num_cards: Number of flashcards to generate

    Returns:
        List of dicts with front, back, difficulty, topic keys
    """
    if not content or len(content.strip()) < 100:
        raise ValueError("Content too short for flashcard generation.")

    max_chars = 4000
    trimmed = content[:max_chars] if len(content) > max_chars else content

    llm = _get_llm()
    parser = StrOutputParser()
    chain = FLASHCARD_PROMPT | llm | parser

    raw = chain.invoke({"content": trimmed, "num_cards": num_cards})
    cleaned = _clean_json(raw)

    try:
        cards = json.loads(cleaned)
        if not isinstance(cards, list):
            raise ValueError("Response was not a list.")
        # Validate each card has required keys
        valid_cards = []
        for card in cards:
            if "front" in card and "back" in card:
                card.setdefault("difficulty", "medium")
                card.setdefault("topic", "General")
                valid_cards.append(card)
        return valid_cards
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse flashcard response: {e}\n\nRaw:\n{raw[:500]}")
