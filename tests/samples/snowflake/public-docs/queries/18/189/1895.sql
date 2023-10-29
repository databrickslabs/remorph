-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

SHOW TABLES;
-- Show the tables that are more than 21 days old and that are empty
-- (i.e. tables that I might have forgotten about).
SELECT "database_name", "schema_name", "name" as "table_name", "rows", "created_on"
    FROM table(RESULT_SCAN(LAST_QUERY_ID()))
    WHERE "rows" = 0 AND "created_on" < DATEADD(day, -21, CURRENT_TIMESTAMP())
    ORDER BY "created_on";