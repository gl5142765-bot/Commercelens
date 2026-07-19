

Goal: Run generated SQL safely and return a rich response.

Task 1 – SQL validation (planned)
- Designed a validate_sql(sql) idea to enforce:
  - Query must start with SELECT.
  - Block dangerous keywords like DROP, DELETE, UPDATE, INSERT, TRUNCATE.
  - Later: restrict to known tables (orders, order_items).
- This will be called before any SQL execution.

Task 2 – SQL execution (deferred)
- Decided to add run_sql_query(sql) later.
- For now, execution is skipped so focus stays on wiring the pipeline and response shape.
- Reminder: run_sql_query should eventually return (columns, rows) from the local database/CSV.

Task 3 – Rich JSON response (implemented)
- Added POST /ask in app/main.py that:
  - Takes a question in the request body.
  - Uses generate_sql_from_question to get model output.
  - Cleans the output to remove ```sql fences, returning just the SQL string.
  - Currently returns JSON with:
    - sql: cleaned SQL.
    - columns: [] (placeholder for now).
    - rows: [] (placeholder for now).
    - display_type: "table".
    - note: "Result for question: <original question>".

Task 4 – End-to-end testing (partial)
- Tested several gold questions via POST /ask in FastAPI docs.
- Confirmed:
  - Questions are accepted.
  - LLM generates sensible SQL.
  - SQL is cleaned and returned in the JSON.
  - Endpoint responds with HTTP 200 and the expected fields.

Current status:
- Backend supports a full question → SQL → rich JSON flow.
- Actual data execution via run_sql_query and full validation will be added in a later step.