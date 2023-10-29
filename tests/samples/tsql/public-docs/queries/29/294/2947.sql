-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-query?view=sql-server-ver16

SELECT q.query_id, qt.query_sql_text
FROM sys.query_store_query_text qt
INNER JOIN sys.query_store_query q ON
    qt.query_text_id = q.query_text_id
WHERE query_sql_text like N'%ORDER BY ListingPrice DESC%'
  AND query_sql_text not like N'%query_store%';
GO