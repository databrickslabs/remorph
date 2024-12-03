--Query type: DML
DECLARE @sql nvarchar(max) = 'WITH profit AS (SELECT CAST(110.0 - 100.0 AS decimal(38, 2)) AS result) SELECT result FROM profit'; EXECUTE sp_executesql @sql;
