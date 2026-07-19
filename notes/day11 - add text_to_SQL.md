
Tasks completed

1. Task 1 – Understand text-to-SQL flow  
   - Clarified the pipeline: user asks a question in natural language, the backend builds a prompt using the database schema and rules, sends it to the LLM, and receives a SQL query as text.  
   - Identified the main functions involved: `build_prompt`, `call_llm`, and a helper that connects them.

2. Task 2 – Implement `generate_sql_from_question`  
   - Added a function `generate_sql_from_question(user_question: str) -> str` in `src/sql_generator.py`.  
   - This function takes the user’s question, builds the prompt, calls `call_llm`, and returns the raw LLM response containing SQL.

3. Task 3 – FastAPI route to return SQL (without executing it)  
   - Created a Pydantic model `QuestionPayload` with a single field `question: str`.  
   - Added a `POST /generate-sql` route in `app/main.py` that reads the question from the request body, calls `generate_sql_from_question`, and returns a JSON response with the SQL text.  
   - Verified through the FastAPI docs UI that the route responds correctly.

4. Task 4 – Test on gold questions  
   - Sent all the defined gold questions (such as monthly revenue and orders between specific years) to the `/generate-sql` endpoint.  
   - Checked the generated SQL for reasonable structure: correct table joins, grouping by month, use of aggregate functions like SUM and COUNT, and date filters in the WHERE clause.

Challenges and how they were solved

1. 401 Unauthorised error from the OpenAI API  
   - Problem: The app was calling the OpenAI endpoint but receiving a “401 Unauthorised” error.  
   - Cause: Incorrect or badly formatted environment variables in the `.env` file and issues with the API key.  
   - Fix: Cleaned up the `.env` file so each line uses the format `KEY=value` with no extra spaces or characters, then added a new valid `OPENAI_API_KEY`. Confirmed the key is loaded correctly using a small test script (`test_llm.py`), which successfully called `call_llm`.

2. Confusion about where to place functions and routes  
   - Problem: Uncertainty about where `generate_sql_from_question` and the FastAPI route should live.  
   - Fix: Kept all LLM-related logic (`call_llm`, `generate_sql_from_question`) inside `src/sql_generator.py`, and kept API routes (like `POST /generate-sql`) inside `app/main.py`. This separation made the structure clearer.

3. Limited SQL knowledge  
   - Problem: Only basic SQL knowledge, not familiar with terms like DISTINCT, DATE_TRUNC, and more complex WHERE clauses.  
   - Fix: Used the generated SQL as a learning tool, breaking down each query to understand what JOIN, GROUP BY, WHERE, DISTINCT, and DATE_TRUNC are doing. This improved comfort with reading and judging the model’s SQL.