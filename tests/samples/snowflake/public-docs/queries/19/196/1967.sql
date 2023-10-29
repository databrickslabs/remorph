-- see https://docs.snowflake.com/en/sql-reference/transactions

begin transaction;
call update_data();
rollback;