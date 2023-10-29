-- see https://docs.snowflake.com/en/sql-reference/transactions

BEGIN TRANSACTION;
statement A;
statement B;
COMMIT;

BEGIN TRANSACTION;
statement C;
statement D;
COMMIT;

BEGIN TRANSACTION;
statement E;
statement F;
COMMIT;

BEGIN TRANSACTION;
statement G;
statement H;
COMMIT;