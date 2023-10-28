SELECT *
FROM dbo.Customers AS c WITH (SNAPSHOT)
LEFT JOIN dbo.[Order History] AS oh
    ON c.customer_id=oh.customer_id;