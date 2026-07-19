# CommerceLens
CommerceLens is a domain‑focused Text‑to‑SQL analytics assistant for a known e‑commerce dataset. Its purpose is to let a business user ask questions in plain English about a fixed orders dataset and receive a generated SQL query, result table, chart, and short explanation in return.

## 1. Quick overview 

**What it is**

Text‑to‑SQL means converting natural‑language questions into SQL queries that can be executed on a relational database. SQL (Structured Query Language) is the standard language used to work with relational databases, where data is stored in structured tables made of rows and columns.
For this project, CommerceLens is built on a fixed, domain‑specific schema rather than an open “upload anything” workflow. The system knows the exact tables, columns, and relationships in advance. This decision improves accuracy, prompting clarity, validation, and explainability because every question is asked against a known business dataset.
A helpful way to think about this is the restaurant owner and chef analogy:

The business stakeholder (restaurant owner) knows the business very well: which products sell, which periods are busiest, and which metrics matter for decisions.
The analyst (chef) knows how to use SQL and the database to answer those questions.
Text‑to‑SQL focuses on the translation step in the middle. It reduces the dependency on manual back‑and‑forth between business questions and database queries, so simple and repeated data access becomes faster.
The goal is not to remove analysts completely. Instead, CommerceLens aims to handle the routine question‑to‑SQL translation so analysts can spend more time on higher‑value analysis, validation, and deeper modelling.


**Dataset used**
CommerceLens works on one known e‑commerce orders dataset. Instead of letting users upload arbitrary files, the project chooses a single domain and learns it deeply.
Source: Kaggle (public dataset).
Domain: e‑commerce orders and order items.
## Data setup

This project does not include the full database in GitHub because it is too large.

Place your local database file inside the `data/` folder before running the app. If you only want to test the app quickly, you can use a small sample database or sample CSV instead.

Example:

```text
commercelens/
├── app/
├── src/
├── tests/
├── data/
│   └── commerce.db
├── assets/
├── notes/
├── README.md
├── requirements.txt
└── config.toml
```

Example tables:

orders: order‑level data such as order id, order date, customer id.
order_items: line‑item data such as product, quantity, and sale price.
The dataset is imported into a local SQLite database (for example, data/orders.db). CommerceLens expects this schema and uses it to:

generate SQL that references the correct tables and columns,

validate queries before running them,
and produce results that are easy to explain back to the business user.
All questions during the first version are framed around this known dataset: trends over time, revenue, order volume, average order value, top products, and similar e‑commerce metrics.

**Stack**

- Backend: FastAPI (Python)
- Frontend: Streamlit
- Data: SQLite database (orders + order_items tables)
- Python libraries: `pandas`, `requests`, `pydantic`

**Main features**

- Generate SQL from a business question.
- Validate and run the SQL against the local SQLite database.
- Show the result as a table and auto-select a basic chart when useful.
- Display a short business note summarising the result.

## 2. Requirements and installation

### 2.1 Python version

- Python 3.11+ (3.10 also works, but the project was tested with 3.11).

### 2.2 requirements.txt

Add this file at the project root:

```text
fastapi
uvicorn
streamlit
pandas
pydantic
requests
python-dotenv
```

If your SQLite database is local, the built‑in `sqlite3` module is enough; no extra dependency is required.

### 2.3 Install dependencies

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Project structure

A clean first version of the repository can look like this:

```text
commercelens/
├── app/
│   └── streamlit.py           # Streamlit frontend
├── backend/
│   ├── main.py                # FastAPI entrypoint
│   ├── src/
│   │   ├── db_client.py       # Load orders dataframe / DB init
│   │   ├── sql_generator.py   # Turn questions into SQL strings
│   │   ├── sql_runner.py      # Run SQL against SQLite
│   │   └── models.py          # Pydantic models (optional)
├── data/
│   └── orders.db              # SQLite database
├── assets/
│   ├── screen1.jpg            # UI screenshots for README/UI
│   ├── screen2.jpg
│   └── screen3.jpg
├── .streamlit/
│   └── config.toml            # Theme (colours, accent)
├── requirements.txt
└── README.md
```

You can adjust module names, but try to keep this separation:

- `backend/` for API and data logic.
- `app/` for everything Streamlit.
- `data/` for the local database.
- `assets/` for screenshots and logos.

## 4. How to run locally (step‑by‑step)

### 4.1 Start the backend (FastAPI)

From the project root:

```bash
uvicorn backend.main:app --reload --port 8000
```

This command starts the FastAPI app on `http://127.0.0.1:8000`. The `/ask` endpoint accepts a JSON payload of the form:

```json
{
  "question": "How has the order count changed over time?"
}
```

The backend returns a JSON object with:

```json
{
  "sql": "SELECT ...",
  "columns": ["month", "order_count"],
  "rows": [
    {"month": "2022-01", "order_count": 120},
    {"month": "2022-02", "order_count": 130}
  ],
  "row_count": 2,
  "display_type": "table",
  "note": "This result shows how order count changes across months."
}
```

### 4.2 Start the frontend (Streamlit)

In a second terminal, still in the project root:

```bash
streamlit run app/streamlit.py
```

Then open the URL that Streamlit prints (usually `http://localhost:8501`).

<img width="1183" height="832" alt="screen1" src="https://github.com/user-attachments/assets/9cab461a-8043-41b2-8b07-5de8f5dbbe00" />
<img width="1787" height="863" alt="screen2" src="https://github.com/user-attachments/assets/4ab3ece1-0878-4426-ba9a-f5b740498fef" />
<img width="1761" height="545" alt="screen3" src="https://github.com/user-attachments/assets/c2b67a7d-33eb-402b-a52e-499d8156d8af" />




### 4.3 Typical flow for a user

1. Open the Streamlit app.
2. Choose an example question or type a custom business question.
3. Click **Ask CommerceLens**.
4. Wait while the backend generates SQL and runs it.
5. View the business note, SQL, data table, and chart.

## 5. Architecture overview (detailed version)

### 5.1 High‑level flow

1. **User question (Streamlit)**  
   The user types a question in the Streamlit UI and clicks the button.

2. **Frontend → Backend call**  
   Streamlit sends `{"question": "..."}` to `POST /ask` on the FastAPI backend using `requests.post`.

3. **SQL generation**  
   `sql_generator.generate_sql_from_question(question)` produces a raw SQL string for the orders dataset.  
   `clean_sql()` and `validate_sql()` ensure the query is safe and usable.

4. **Query execution**  
   `sql_runner.run_sql_query(sql)` runs the SQL against the local SQLite database and returns `columns`, `rows`, and the final SQL.

5. **Business note**  
   `generate_business_note(question, columns, rows)` builds a short, deterministic summary from the result (single value, trend, or comparison).

6. **Backend response**  
   FastAPI returns a JSON payload containing SQL, columns, rows, `display_type`, and `note`.

7. **Frontend rendering**  
   Streamlit:
   - shows the note in the **Result** card,  
   - wraps SQL in an expander,  
   - builds a `pandas.DataFrame` for the table,  
   - auto‑selects either a line chart or bar chart based on the first two columns and the `display_type`.

### 5.2 Key modules

- `db_client.py`  
  - Initialises the SQLite database (if needed).  
  - Provides helper functions like `get_orders_df()`.

- `sql_generator.py`  
  - Contains the logic or prompt that maps natural‑language questions to SQL.  
  - Handles date filters, group‑by, and simple aggregations.

- `sql_runner.py`  
  - Opens a connection to `orders.db`.  
  - Executes SQL safely and returns results as Python structures.

- `backend/main.py`  
  - Defines the FastAPI app, startup hook, and `/ask` endpoint.  
  - Orchestrates generation, validation, execution, and response construction.

- `app/streamlit.py`  
  - Implements the UI layout (two‑column top section, result card below).  
  - Handles example questions, request/response flow, and chart logic.

## 6. Notes for deployment

This first version is designed to run locally, but the repository layout and README are prepared so you can later:

- deploy FastAPI behind a reverse proxy,
- host the Streamlit app or convert it into another frontend stack,
- or switch the SQLite database to a managed database service.
