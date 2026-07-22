# Future work – CommerceLens

This version of CommerceLens focuses on a single e‑commerce dataset, a fixed schema, and a simple question → SQL → chart flow.  
Below are a few ideas for where the project could go next [web:672][web:681].

## 1. Authentication and user accounts

- Add sign‑in (email, OAuth, or single‑tenant auth) so each user sees only their own saved questions.
- Restrict access to certain datasets or tables based on roles (e.g., finance vs. operations).

## 2. Saved query history and dashboards

- Store past questions, generated SQL, and results per user.
- Allow users to “pin” queries into a simple dashboard view.
- Let users re‑run past questions with updated data.

## 3. Smarter chart selection and layouts

- Use heuristics or a small rules engine to choose between:
  - line charts for time series,
  - bar charts for category comparisons,
  - tables for small result sets.
- Add support for multiple series and side‑by‑side comparisons.

## 4. Stronger SQL guardrails

- Add a stricter validation layer to block:
  - cross‑joins without filters,
  - queries returning too many rows,
  - unsupported functions or subqueries.
- Maintain an explicit whitelist of allowed tables, columns, and aggregate patterns.

## 5. Richer business summaries

- Move from one‑sentence notes to richer summaries that:
  - call out trends, peaks, and anomalies,
  - compare periods (e.g., month‑over‑month, year‑over‑year),
  - include suggested follow‑up questions.

These ideas keep the project focused on explainable, safe analytics while making CommerceLens more useful for real business users over time.
