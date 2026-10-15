-- Revenue by region
SELECT region, ROUND(SUM(amount), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;
-- Top 3 customers by spend
SELECT customer, ROUND(SUM(amount), 2) AS spend
FROM sales GROUP BY customer ORDER BY spend DESC LIMIT 3;
