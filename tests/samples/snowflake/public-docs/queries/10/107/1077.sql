-- see https://docs.snowflake.com/en/sql-reference/functions/count

SELECT COUNT(n.*)
    FROM non_null_counter AS n;