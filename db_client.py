import pandas as pd
from src.config import ORDERS_CSV


def get_orders_df():
    return pd.read_csv(ORDERS_CSV)


def answer_question(question: str):
    # 1. Generate SQL from the question
    sql = generate_sql_from_question(question)
    sql = clean_sql(sql)
    validate_sql(sql)

    # 2. Run that SQL
    columns, rows = run_sql_query(sql)

    # 3. Return or render result
    return sql, columns, rows