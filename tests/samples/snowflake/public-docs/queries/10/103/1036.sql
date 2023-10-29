-- see https://docs.snowflake.com/en/sql-reference/functions/booland

SELECT BOOLAND(1, -2), BOOLAND(0, 2.35), BOOLAND(0, 0), BOOLAND(0, NULL), BOOLAND(NULL, 3), BOOLAND(NULL, NULL);
