-- see https://docs.snowflake.com/en/sql-reference/functions/boolor

SELECT BOOLOR(1, 2), BOOLOR(-1.35, 0), BOOLOR(3, NULL), BOOLOR(0, 0), BOOLOR(NULL, 0), BOOLOR(NULL, NULL);
