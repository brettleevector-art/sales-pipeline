-- Revenue by region
SELECT region, ROUND(SUM(amount), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;
