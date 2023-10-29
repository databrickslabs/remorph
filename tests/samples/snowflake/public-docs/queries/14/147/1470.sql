-- see https://docs.snowflake.com/en/sql-reference/account-usage/tables

SELECT TABLE_SCHEMA,SUM(BYTES)
    FROM snowflake.account_usage.tables
    WHERE DELETED IS NULL
    GROUP BY TABLE_SCHEMA;