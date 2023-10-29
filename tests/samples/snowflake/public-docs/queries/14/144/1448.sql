-- see https://docs.snowflake.com/en/sql-reference/references

SELECT SYSTEM$REFERENCE('TABLE', 't1', 'CALL', 'SELECT');