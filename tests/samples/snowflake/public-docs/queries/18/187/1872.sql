-- see https://docs.snowflake.com/en/sql-reference/functions/system_abort_transaction

SHOW LOCKS IN ACCOUNT;


SELECT SYSTEM$ABORT_TRANSACTION(1442254688149);
