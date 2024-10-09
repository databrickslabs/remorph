--Query type: DDL
WITH customer_data AS (
    SELECT 1 AS id, '123-45-6789' AS credit_card_number
),
credit_card_mask AS (
    SELECT id, 'XXXX-XX-' + RIGHT(credit_card_number, 4) AS credit_card_number
    FROM customer_data
)
SELECT *
FROM credit_card_mask;