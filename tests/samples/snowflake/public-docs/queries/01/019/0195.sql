-- see https://docs.snowflake.com/en/sql-reference/transactions

BEGIN TRANSACTION;
statement A;
statement B;
COMMIT;

CALL p1();

BEGIN TRANSACTION;
statement G;
statement H;
COMMIT;