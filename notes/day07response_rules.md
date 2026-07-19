Day 7 



##### ***Default Result Behaviour***



1\. Table:

&#x20;  - Always allowed.

&#x20;  - Default when the query returns few rows or when users need exact values.



2\. Chart:

&#x20;  - Only used when:

&#x20;    - There is at least one numeric metric.

&#x20;    - There is a clear dimension (time or category) to compare.

&#x20;    - The result has multiple rows (not just one).  



3\. Both (table + chart):

&#x20;  - Used when:

&#x20;    - The result is chartable (time or category + number).

&#x20;    - The table adds value for reading exact numbers or multiple metrics, 

&#x20;      While the chart shows the pattern or trend.



##### 

##### ***Chart ability Logic***



1\. Time-series results (date/month + number):

&#x20;  - If there is a column like date, day, month, year, AND

&#x20;    at least one numeric metric column (SUM, COUNT, AVG, etc.) AND

&#x20;    more than one row:

&#x20;    → Use a line chart or bar chart over time.

&#x20;  - Example: Questions 5, 6, 7, 8.



2\. Category results (category + number):

&#x20;  - If there is a categorical column (product, customer, country, status, etc.)

&#x20;    AND at least one numeric metric

&#x20;    AND a small/medium number of categories:

&#x20;    → Use a bar chart (horizontal or vertical).



3\. Single-row results:

&#x20;  - If the query returns only 1 row (e.g., “Which month had the highest X?” or “total revenue for period”):

&#x20;    → Table/KPI only.

&#x20;    → No chart, unless we expand the query to show all rows, not just the max.



4\. Many detailed columns:

&#x20;  - If the result has many non-numeric columns or many metrics where the visual pattern is not clear:

&#x20;    → Table only.

&#x20;    → Chart might be confusing.



Summary:

\- date + number + many rows → line/bar chart.  

\- category + number + many rows → bar chart.  

\- single row or many detailed columns → table only.





##### ***Result Summary Note Templates***



1\. Time-series metrics (like Q5–8):

&#x20;  - Template:

&#x20;    "This result shows how \[metric] changes over \[time period]. Peaks indicate the strongest periods, and dips show weaker performance."

&#x20;  - Examples:

&#x20;    - "This result shows how total revenue changes over months. Peaks indicate the strongest sales months, and dips show weaker revenue."

&#x20;    - "This result shows how average order value changes over months. Peaks indicate higher customer spend per order."



2\. Single summary metrics (like Q1–4):

&#x20;  - Template:

&#x20;    "\[Metric] for the selected period is \[value]. This represents overall performance without breaking it down by time or category."

&#x20;  - Example:

&#x20;    - "Total revenue for the selected period is X. This represents overall sales without breaking it down by month."



3\. Highest-month questions (like Q9–12):

&#x20;  - Template:

&#x20;    "The highest \[metric] was recorded in \[month]. This period stands out compared to other months in the selected range."

&#x20;  - Example:

&#x20;    - "The highest monthly revenue was recorded in 2023-11. This period stands out compared to other months in the selected range."













