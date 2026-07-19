# Day 5 – Manual Gold SQL Summary

On Day 5, the goal was to build confidence with the e‑commerce schema by writing and validating manual SQL queries before involving any LLM assistance.

Work completed:

- Wrote a set of manual SQL queries (more than the target 5–8) against the core tables such as `orders` and `order_items`, focusing on common business questions like monthly revenue, order counts, and average order value.
- Executed each query in BigQuery / notebook environment and verified the results manually using table outputs to check:
  - Correct joins and filters
  - Correct use of aggregate functions (SUM, COUNT, AVG)
  - Correct grouping by time (month/day) and other dimensions
- Confirmed that each query returns logically consistent results with the dataset, making them reliable “gold” examples for later use.
- Identified these manually written and validated queries as the initial gold SQL set that will be reused for prompting and evaluation in later days.

Outcome:

Day 5 produced a trusted base of manually validated SQL queries on the e‑commerce schema. These examples capture key business metrics (revenue, orders, average order value, etc.) and will serve as reference queries when designing and testing the text‑to‑SQL app in upcoming days.