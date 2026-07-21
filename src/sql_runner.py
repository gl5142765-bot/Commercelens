import sqlite3
import pandas as pd
import re

from src.config import ORDERS_CSV, ORDER_ITEMS_CSV, PRODUCTS_CSV, USERS_CSV

def _build_connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    if USERS_CSV.exists():
        pd.read_csv(USERS_CSV).to_sql("users", conn, if_exists="replace", index=False)
    if PRODUCTS_CSV.exists():
        pd.read_csv(PRODUCTS_CSV).to_sql("products", conn, if_exists="replace", index=False)
    if ORDERS_CSV.exists():
        pd.read_csv(ORDERS_CSV).to_sql("orders", conn, if_exists="replace", index=False)
    if ORDER_ITEMS_CSV.exists():
        pd.read_csv(ORDER_ITEMS_CSV).to_sql("order_items", conn, if_exists="replace", index=False)

    return conn

def init_db():
    return None

def run_sql_query(sql: str, limit: int = 100) -> dict:
    conn = _build_connection()
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
