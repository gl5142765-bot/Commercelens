import sqlite3
import pandas as pd
from src.config import DATA_DIR, DB_PATH
import re

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        orders_df = pd.read_csv(DATA_DIR / "orders.csv")
        orders_df.to_sql("orders", conn, if_exists="replace", index=False)

        order_items_df = pd.read_csv(DATA_DIR / "order_items.csv")
        order_items_df.to_sql("order_items", conn, if_exists="replace", index=False)
    finally:
        conn.close()

def run_sql_query(sql: str, limit: int = 100) -> dict:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        clean_sql = sql.strip().rstrip(";")
        if not clean_sql:
            raise ValueError("Empty SQL query.")

        has_limit = bool(re.search(r"\bLIMIT\b", clean_sql, flags=re.IGNORECASE))
        sql_to_execute = clean_sql if has_limit else f"{clean_sql} LIMIT {limit}"

        cursor.execute(sql_to_execute)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        result_rows = [dict(row) for row in rows]

        return {
            "columns": columns,
            "rows": result_rows,
            "sql_executed": sql_to_execute,
            "row_count": len(result_rows),
        }
    finally:
        conn.close()
