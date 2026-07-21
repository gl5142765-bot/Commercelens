import streamlit as st
import requests
import pandas as pd
from pathlib import Path

BACKEND_URL = "https://commercelens-backend-1.onrender.com"

st.set_page_config(page_title="CommerceLens", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Urbanist', sans-serif;
}
</style>
""", unsafe_allow_html=True)

if "question_text" not in st.session_state:
    st.session_state["question_text"] = ""


def show_preview_images():
    image_paths = [
        Path("assets/screen2.jpg"),
    ]

    shown_any = False
    for img_path in image_paths:
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
            shown_any = True

    if not shown_any:
        st.info("Add screenshots inside the assets folder as screen1.jpg.")


def render_chart(df: pd.DataFrame, display_type: str):
    if df.shape[1] < 2 or len(df) <= 1:
        st.info("Chart is available only for results with at least 2 columns and more than 1 row.")
        return

    chart_df = df.iloc[:, :2].copy()
    x_col = chart_df.columns[0]
    y_col = chart_df.columns[1]

    chart_df[y_col] = pd.to_numeric(chart_df[y_col], errors="coerce")
    chart_df = chart_df.dropna(subset=[y_col])

    if chart_df.empty:
        st.info("Chart could not be rendered because the second column is not numeric.")
        return

    x_values = chart_df[x_col].astype(str)

    if (
        display_type == "line_chart"
        or x_col.lower() in ["date", "month", "year"]
        or any("-" in val for val in x_values)
    ):
        st.line_chart(chart_df.set_index(x_col), use_container_width=True)
    else:
        st.bar_chart(chart_df.set_index(x_col), use_container_width=True)


def main():
    st.title("CommerceLens")
    st.caption("Ask questions about your commerce data in plain English.")

    top_box = st.container(border=True)
    with top_box:
        left, right = st.columns([2, 1], gap="large")

        with left:
            st.subheader("Ask a question")
            st.write(
                "Type a business question and CommerceLens will generate SQL, "
                "run it, and show the results."
            )

            st.write("Try an example:")
            ex_col1, ex_col2 = st.columns(2)

            if ex_col1.button("Average order value"):
                st.session_state["question_text"] = "What is the average order value?"
                st.rerun()

            if ex_col2.button("revenue change over time"):
                st.session_state["question_text"] = "How has revenue changed over time?"
                st.rerun()

            question = st.text_input(
                "Enter your question:",
                value=st.session_state["question_text"],
                key="question_text",
            )

            ask_clicked = st.button("Ask CommerceLens")

        with right:
            preview_box = st.container(border=True)
            with preview_box:
                st.subheader("What you can expect")
                st.caption("Examples of CommerceLens results")
                show_preview_images()

    sql = ""
    columns = []
    rows = []
    display_type = "table"
    note = ""

    if ask_clicked:
        if not question or not question.strip():
            st.warning("Please enter a question before submitting.")
        else:
            with st.spinner("Thinking..."):
                try:
                    payload = {"question": question}
                    response = requests.post(BACKEND_URL, json=payload)

                    if response.status_code != 200:
                        st.error(f"Backend error: {response.status_code}")
                    else:
                        data = response.json()
                        sql = data.get("sql", "")
                        columns = data.get("columns", [])
                        rows = data.get("rows", [])
                        display_type = data.get("display_type", "table")
                        note = data.get("note", "")
                except Exception as e:
                    st.error(f"Failed to call backend: {e}")

    st.divider()

    result_box = st.container(border=True)
    with result_box:
        st.subheader("Result")

        if note:
            st.markdown("**Business note**")
            st.write(note)
            st.divider()

        if sql:
            st.markdown("**Generated SQL**")
            with st.expander("View SQL"):
                st.code(sql, language="sql")
            st.divider()

        if rows:
            st.markdown("**Data**")

            df = pd.DataFrame(rows)
            if columns and len(columns) == df.shape[1]:
                df.columns = columns

            st.dataframe(df, use_container_width=True)

            st.divider()

            st.markdown("**Chart**")
            render_chart(df, display_type)
        else:
            st.info("No results yet. Ask a question to see data and charts.")


if __name__ == "__main__":
    main()
