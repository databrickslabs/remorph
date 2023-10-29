-- see https://docs.snowflake.com/en/sql-reference/constructs/from

SELECT *
    FROM sales AT(OFFSET => -86400);
SELECT *
    FROM sales AT(TIMESTAMP => '2018-07-27 12:00:00'::TIMESTAMP);