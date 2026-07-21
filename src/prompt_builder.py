PROMPT_TEMPLATE = """
You are an expert SQL assistant for the CommerceLens dataset.

Generate SQL for SQLite only.

Use only the provided schema context to generate SQL queries.
Follow the metric definitions exactly.
Return SQL only.

Schema:
- orders
- order_items

Relationships:
- orders.order_id = order_items.order_id

Metric definitions:
- Total revenue = sum of sale_price
- Order count = total number of orders
- Average order value = total revenue / order count
- Number of items per order = num_of_item from the orders table

Output rules:
- Return SQL only
- Do not add explanations
- Do not guess columns that are not in the schema
- Use the correct joins based on the schema
- Use date filters only when the question asks for a time period

SQLite rules:
- Use SQLite-compatible SQL only
- Never use DATE_TRUNC()
- Never use DATE_FORMAT()
- For month grouping, use strftime('%Y-%m', created_at)
- For year grouping, use strftime('%Y', created_at)
- For date only, use date(created_at)
- Use LIMIT only when needed
- Always use table aliases in joined queries
- Always qualify column names with table aliases when a query uses joins
- Never use bare column names like created_at, id, or order_id in joined queries
- Use o.created_at for orders.created_at
- Use oi.created_at for order_items.created_at
- Use o.order_id for orders.order_id
- Use oi.order_id for order_items.order_id

Example:
Question: Which month had the highest revenue?
SQL:
SELECT
    strftime('%Y-%m', o.created_at) AS month,
    SUM(oi.sale_price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY strftime('%Y-%m', o.created_at)
ORDER BY revenue DESC
LIMIT 1
"""


def build_prompt(user_question: str) -> str:
    return PROMPT_TEMPLATE + "\n\nUser question:\n" + user_question


def normalize_sql_for_sqlite(sql: str) -> str:
    sql = sql.strip()

    sql = sql.replace("DATE_TRUNC('month', order_date)", "strftime('%Y-%m', order_date)")
    sql = sql.replace('DATE_TRUNC("month", order_date)', "strftime('%Y-%m', order_date)")
    sql = sql.replace("DATE_TRUNC('month', created_at)", "strftime('%Y-%m', created_at)")
    sql = sql.replace('DATE_TRUNC("month", created_at)', "strftime('%Y-%m', created_at)")

    sql = sql.replace("DATE_FORMAT(order_date, '%Y-%m')", "strftime('%Y-%m', order_date)")
    sql = sql.replace('DATE_FORMAT(order_date, "%Y-%m")', "strftime('%Y-%m', order_date)")
    sql = sql.replace("DATE_FORMAT(created_at, '%Y-%m')", "strftime('%Y-%m', created_at)")
    sql = sql.replace('DATE_FORMAT(created_at, "%Y-%m")', "strftime('%Y-%m', created_at)")

    return sql
