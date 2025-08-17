-- Top 5 banks by transaction volume in the last 7 days
SELECT 
    bank_id,
    SUM(total_amount) AS total_volume
FROM daily_transactions
WHERE date >= CURDATE() - INTERVAL 7 DAY
GROUP BY bank_id
ORDER BY total_volume DESC
LIMIT 5;

-- Average transaction value per customer for a given month
-- Replace '2025-08' with the desired YYYY-MM
SELECT 
    customer_id,
    AVG(amount) AS avg_transaction_value
FROM transactions
WHERE DATE_FORMAT(date, '%Y-%m') = '2025-08'
GROUP BY customer_id;
