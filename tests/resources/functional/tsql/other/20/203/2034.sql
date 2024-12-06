-- tsql sql:
SELECT l_orderkey, l_extendedprice, IIF(l_extendedprice > l_discount, 'greater', 'lesser') AS comparison_result, TRY_CAST(l_orderkey AS VARCHAR(10)) AS l_orderkey_casted, TRY_CONVERT(VARCHAR(10), l_extendedprice) AS l_extendedprice_casted, TRY_PARSE('2022-01-01' AS DATE) AS date_parsed, TRY_CAST(NULL AS INT) AS null_casted, IIF(TRY_CAST(NULL AS INT) IS NULL, 'null', 'not null') AS null_check FROM (VALUES (1, 2, 3), (4, 5, 6), (7, 8, 9)) AS temp_result(l_orderkey, l_extendedprice, l_discount);
