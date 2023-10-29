-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/declare

c1 CURSOR FOR SELECT id, price FROM invoices;