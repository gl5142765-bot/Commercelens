\# Day 01 Scope



\## Final project title

&#x20;CommerceLens



\## Subtitle

Natural Language E-commerce Analytics Assistant



\##Business use case

CommerceLens is a natural-language analytics project for e-commerce data. The goal is to let a user ask business questions in plain English, convert that question into SQL, run it on the selected e-commerce dataset, and return a clear result with a short business conclusion.



The project is being built as a beginner-friendly but portfolio-ready product. It is focused on helping users understand sales, products, orders, and performance metrics without needing to write SQL manually.



\## Target users

\- Non-technical business users.

\- Beginner analysts who want faster access to insights.

\- Founders, managers, or e-commerce stakeholders who want quick answers from data.

\- Portfolio reviewers or interviewers evaluating an end-to-end analytics project.



\## Chosen stack

\- Dataset: theLook eCommerce dataset on Google BigQuery.

\- Backend: FastAPI.

\- Frontend: Streamlit.

\- Language: Python.

\- Database querying: SQL through BigQuery.

\- Deployment: Render.

\- Project workflow:\*\* local development first, then deployment after testing.



\## Final output behaviour

\- The default response format will be a table.

\- Every answer should include a short \*\*note or conclusion\*\* in simple language.

\- If the result supports visualisation, the app can also show a chart.

\- If both the chart and table are useful, the app can show both.

\- The user does not need to choose output mode manually.

\- The system should automatically decide the most suitable format based on the returned result.

\- If charting is not suitable, the app should safely show the table only with the short note.



\## First-version scope note

The first version of Commerce Lens should stay focused and practical. It should prioritise correct SQL generation, reliable tabular answers, simple business summaries, and a clean local-to-deployment workflow, rather than too many advanced features at the outset.







**## First-version scope**

**- Fixed e-commerce schema:** *Use only the core tables needed for the first version.*

**- Table-first response:** *Always show the result in table form first.*

**- Chart only when suitable:** *Add a chart only if the data clearly supports it.*

**- Short business note:** *Give a short conclusion with the result in simple words.*



