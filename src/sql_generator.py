import os
import re
import requests
from src.prompt_builder import build_prompt, normalize_sql_for_sqlite

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1/chat/completions")

ALLOWED_TABLES = ["orders", "order_items"]
FORBIDDEN_KEYWORDS = ["drop", "truncate", "alter", "delete", "update", "insert"]

def call_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": LLM_MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
    }

    response = requests.post(LLM_BASE_URL, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

def clean_sql(raw_text: str) -> str:
    cleaned = raw_text.strip()
    cleaned = cleaned.replace("```sql", "")
    cleaned = cleaned.replace("```", "")
    return cleaned.strip()

def validate_sql(sql: str) -> bool:
    cleaned = sql.strip().lower()

    if not cleaned.startswith("select"):
        return False

    if any(word in cleaned for word in FORBIDDEN_KEYWORDS):
        return False

    return True

def generate_sql_from_question(user_question: str) -> str:
    prompt = build_prompt(user_question)
    raw_text = call_llm(prompt)
    cleaned_sql = clean_sql(raw_text)
    normalized_sql = normalize_sql_for_sqlite(cleaned_sql)
    return normalized_sql
