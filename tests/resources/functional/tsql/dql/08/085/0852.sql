--Query type: DQL
WITH patterns AS (
    SELECT pattern
    FROM (
        VALUES ('%Jo%oe%'), ('J%n')
    ) AS p (pattern)
)
SELECT c.customer_name
FROM (
    VALUES ('John Joe', 1), ('Jane Doe', 2), ('Joe Johnson', 3), ('Jenifer Jn', 4)
) AS c (customer_name, customer_id)
WHERE EXISTS (
    SELECT 1
    FROM patterns p
    WHERE c.customer_name LIKE p.pattern
)
ORDER BY c.customer_name;
