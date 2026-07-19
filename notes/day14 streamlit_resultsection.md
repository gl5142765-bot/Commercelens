## Day 14 – Result Rendering and Data Flow

Goal: Show answers clearly in the UI and connect the backend data to the frontend.

Summary:
Today I completed the result rendering flow for CommerceLens and added a basic data execution layer.

First, I implemented a temporary run_sql_query(sql) function in src/db_client.py. It reads the orders CSV via get_orders_df(), limits the DataFrame to a small sample for performance, replaces any NaN values with None for JSON compatibility, and returns (columns, rows) as a list of column names and a list of row dictionaries. This gives the FastAPI backend real data to send back with each question.

Next, I updated the /ask endpoint in app/main.py to use run_sql_query. After generating and cleaning the SQL from the user’s question, the endpoint calls run_sql_query(sql) and includes columns, rows, display_type, and a short note in the JSON response alongside the SQL string.

On the frontend, I extended the Streamlit app (app/streamlit.py) to render the results neatly. The app shows a “Result” section with a short note describing the question. The generated SQL is displayed inside a collapsible “Generated SQL” expander for users who want to inspect the query. Below that, the app builds a pandas DataFrame from rows and columns and shows it with st.dataframe as a clean “Data” table. This completes the basic answer flow: question in natural language, generated SQL visible on demand, and a table of data shown in the UI.

Status:
CommerceLens now supports a full local flow from question → SQL → table + note. Real SQL execution and smarter charting based on display_type can be added later as the next step.