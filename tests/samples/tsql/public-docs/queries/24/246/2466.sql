-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/concat-ws-transact-sql?view=sql-server-ver16

SELECT CONCAT_WS(',', '1 Microsoft Way', NULL, NULL, 'Redmond', 'WA', 98052) AS Address;