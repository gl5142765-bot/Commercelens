# CommerceLens

CommerceLens is a domain‑focused Text‑to‑SQL analytics assistant for a known e‑commerce dataset.  
It lets a business user ask questions in plain English about a fixed orders dataset and returns a generated SQL query, result table, chart, and short explanation.

---

## 1. Quick overview

### 1.1 What Text‑to‑SQL means

Text‑to‑SQL means converting natural‑language questions into SQL queries that can be executed on a relational database.  
SQL (Structured Query Language) is the standard language for working with relational databases, where data is stored in structured tables made of rows and columns [web:670][web:679].

CommerceLens is built on a **fixed, domain‑specific schema** instead of an open “upload anything” workflow:

- The system knows the exact tables, columns, and relationships in advance.
- Every question is asked against this known business dataset.
- This improves accuracy, validation, and explainability, because the model is always operating inside a defined schema [web:670][web:681].

The goal is not to remove analysts. Instead, CommerceLens handles routine question‑to‑SQL translation so analysts can spend more time on deeper analysis and interpretation.

### 1.2 Dataset used

CommerceLens works on a single public e‑commerce orders dataset:

- Source: Kaggle (public dataset)
- Domain: orders, order items, and basic customer and product information
- Tables used in this version:
  - `orders` – order‑level facts such as order id, order date, customer id, and order status
  - `order_items` – line‑item details such as product id, quantity, and sale price

The dataset is imported into a local SQLite database or CSVs, and all questions in v1 are framed around core metrics such as:

- revenue and order volume over time
- average order value
- top products or categories
- simple cohort‑style views (by month, by status, etc.)

---

## 2. Data setup

### 2.1 Files required

This repo includes four CSV files under `data/`:

```text
data/
├── orders.csv
├── order_items.csv
├── products.csv
└── users.csv
```

These are the inputs used to build the internal SQLite database at runtime.  
The backend expects these files to be present before the app starts.

If you want to plug in your own data:

1. Keep the same column names and structure where possible.
2. Replace the CSVs in `data/`.
3. Restart the backend so it reloads the data into SQLite.

### 2.2 Example project layout

```text
commercelens/
├── app/
│   └── streamlit.py         # Streamlit frontend
├── src/
│   ├── config.py            # App configuration
│   ├── db_client.py         # Load CSVs / DB init
│   ├── prompt_builder.py    # System + user prompt templates
│   ├── sql_generator.py     # Turn questions into SQL strings
│   ├── sql_runner.py        # Run SQL against SQLite
│   └── ...
├── data/
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   └── users.csv
├── assets/
│   ├── screen1.jpg          # UI screenshots
│   ├── screen2.jpg
│   └── screen3.jpg
├── tests/
├── .streamlit/
│   └── config.toml          # Streamlit theme
├── requirements.txt
└── README.md
```

---

## 3. Stack and features

### 3.1 Tech stack

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Data**: SQLite database built from the CSVs in `data/`
- **Python libraries**: `pandas`, `requests`, `pydantic`, `python-dotenv`, plus standard `sqlite3` [web:671][web:684]

### 3.2 Main features

- Generate SQL from a natural‑language business question
- Validate and run SQL against the local SQLite database
- Return:
  - the generated SQL,
  - the result table,
  - an auto‑selected chart (line or bar),
  - and a short, deterministic business note describing the result
- Provide example questions for “one‑click” exploration

---

## 4. Requirements and installation

### 4.1 Python version

- Python 3.11+ (tested primarily on 3.11)

### 4.2 Dependencies

`requirements.txt` at the repo root:

```text
fastapi
uvicorn
streamlit
pandas
pydantic
requests
python-dotenv
```

Install these from the project root:

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

---

## 5. Running the app locally

### 5.1 Start the backend (FastAPI)

From the project root:

```bash
uvicorn src.main:app --reload --port 8000
```

- The app listens on `http://127.0.0.1:8000`.
- The main endpoint is `POST /ask`.

Example request body:

```json
{
  "question": "How has revenue changed over time?"
}
```

Example response shape:

```json
{
  "sql": "SELECT ...",
  "columns": ["month", "revenue"],
  "rows": [
    {"month": "2022-01", "revenue": 162029.34}
  ],
  "row_count": 12,
  "display_type": "line",
  "note": "This shows monthly revenue over the selected period."
}
```

### 5.2 Start the frontend (Streamlit)

In a second terminal, again from the project root:

```bash
streamlit run app/streamlit.py
```

Open the URL printed in the terminal (usually `http://localhost:8501`).

The UI allows you to:

- Pick an example question or type your own.
- Send it to the backend.
- View the generated SQL, result table, and chart.
- Read a short business‑friendly interpretation.

Screenshots:

> include the three `assets/screen*.jpg` screenshots here as images in the README if you like.

### 5.3 Typical user flow

1. Open the Streamlit app.
2. Choose a sample question (e.g., “How has revenue changed over time?”).
3. Click **Ask CommerceLens**.
4. Wait while the backend generates SQL and runs it.
5. Inspect:
   - the business note,
   - the SQL (in the expander),
   - the table and chart.

---

## 6. Architecture overview

### 6.1 High‑level flow

1. **User question (Streamlit)**  
   The user submits a question through the Streamlit UI.

2. **Frontend → Backend call**  
   Streamlit calls `POST /ask` on the FastAPI backend with a JSON payload containing the question.

3. **SQL generation**  
   `sql_generator` turns the question into a SQL string for the known orders schema.  
   `prompt_builder` helps constrain the model and keep SQL on the allowed tables and columns.

4. **Query execution**  
   `sql_runner` runs the SQL against the SQLite database built from the CSVs and returns:
   - `columns`
   - `rows`
   - `row_count`
   - `display_type` suggestions

5. **Business note**  
   A summariser builds a short, deterministic note describing trends or comparisons.

6. **Backend response**  
   FastAPI returns a JSON object containing SQL, data, and presentation hints.

7. **Frontend rendering**  
   Streamlit:
   - shows the note in a result card,
   - wraps SQL in a “View SQL” expander,
   - converts data to a `pandas.DataFrame`,
   - chooses a line or bar chart based on the result structure.

### 6.2 Key modules

- `src/db_client.py` – loads CSVs and initialises SQLite.
- `src/sql_generator.py` – maps questions to SQL.
- `src/sql_runner.py` – executes SQL against SQLite and returns rows.
- `src/config.py` and `src/prompt_builder.py` – configuration and prompt logic.
- `src/main.py` – FastAPI entrypoint and `/ask` endpoint orchestration.
- `app/streamlit.py` – Streamlit UI and HTTP calls to the backend.

---

## 7. Deployment

This project has been deployed with:

- **Backend**: FastAPI on Render (or similar PaaS)
- **Frontend**: Streamlit on Render, configured to call the hosted backend

You can add your live URLs here:

- Frontend: `https://<your-frontend>.onrender.com`
- Backend: `https://<your-backend>.onrender.com`

The repo layout and configuration are kept simple so you can later:

- put FastAPI behind a reverse proxy,
- swap Streamlit for another frontend stack,
- or move from SQLite to a managed relational database service [web:671][web:684].
