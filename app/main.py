from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from src.sql_runner import run_sql_query
from src.sql_generator import generate_sql_from_question, clean_sql, validate_sql

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

class QuestionPayload(BaseModel):
    question: str

def generate_business_note(question: str, columns: list[str], rows: list[dict]) -> str:
    if not rows:
        return "No results were found for this question."

    if len(rows) == 1:
        row = rows[0]
        if isinstance(row, dict):
            parts = [f"{k}: {v}" for k, v in row.items()]
            return "The query returns a single result - " + ", ".join(parts) + "."
        return "The query returns a single result."

    if len(columns) >= 2:
        first_col = columns[0].lower()
        second_col = columns[1].lower()

        if first_col in ["month", "year", "date"]:
            return f"This result shows how {second_col.replace('_', ' ')} changes across {first_col}."

        return f"This result compares {first_col.replace('_', ' ')} against {second_col.replace('_', ' ')}."

    return "The query returned multiple rows of results."

def answer_question(question: str):
    logger.info(f"Question received: {question}")

    raw_sql = generate_sql_from_question(question)
    logger.info(f"Raw SQL: {raw_sql}")

    sql = clean_sql(raw_sql)
    logger.info(f"Clean SQL: {sql}")

    if not validate_sql(sql):
        logger.error("SQL validation failed")
        raise HTTPException(status_code=400, detail="Generated SQL failed validation.")

    query_result = run_sql_query(sql)
    logger.info(f"Query result keys: {list(query_result.keys())}")

    columns = query_result.get("columns", [])
    rows = query_result.get("rows", [])
    logger.info(f"Columns: {columns}")
    logger.info(f"Row count: {len(rows)}")

    note = generate_business_note(question, columns, rows)
    logger.info(f"Business note: {note}")

    return {
        "sql": query_result.get("sql_executed", sql),
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "display_type": "table",
        "note": note,
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/generate-sql")
def generate_sql_endpoint(payload: QuestionPayload):
    raw_sql = generate_sql_from_question(payload.question)
    sql = clean_sql(raw_sql)

    if not validate_sql(sql):
        raise HTTPException(status_code=400, detail="Generated SQL failed validation.")

    return {"sql": sql}

@app.post("/ask")
def ask_endpoint(payload: QuestionPayload):
    return answer_question(payload.question)
