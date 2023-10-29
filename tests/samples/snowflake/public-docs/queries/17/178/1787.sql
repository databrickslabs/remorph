-- see https://docs.snowflake.com/en/sql-reference/operators-query

SELECT v FROM t1    -- VARCHAR
UNION
SELECT i FROM t2    -- INTEGER
;