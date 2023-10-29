-- see https://docs.snowflake.com/en/sql-reference/transactions

begin;
statement W;
statement X;
statement Y;
statement Z;
commit;