-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table?view=sql-server-ver16

SELECT *
FROM dbo.Customers AS c WITH (SNAPSHOT)
LEFT JOIN dbo.[Order History] AS oh
    ON c.customer_id=oh.customer_id;