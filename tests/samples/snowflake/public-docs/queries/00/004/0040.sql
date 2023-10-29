-- see https://docs.snowflake.com/en/sql-reference/identifiers-syntax

-- Set the default behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = false;

-- Create a table with a double-quoted identifier
CREATE TABLE "One" (i int);  -- stored as "One"

-- Create a table with an unquoted identifier
CREATE TABLE TWO(j int);     -- stored as "TWO"

-- These queries work
SELECT * FROM "One";         -- searches for "One"
SELECT * FROM two;           -- searched for "TWO"
SELECT * FROM "TWO";         -- searches for "TWO"

-- These queries do not work
SELECT * FROM One;           -- searches for "ONE"
SELECT * FROM "Two";         -- searches for "Two"

-- Change to the all-uppercase behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = true;

-- Create another table with a double-quoted identifier
CREATE TABLE "Three"(k int); -- stored as "THREE"

-- These queries work
SELECT * FROM "Two";         -- searches for "TWO"
SELECT * FROM two;           -- searched for "TWO"
SELECT * FROM "TWO";         -- searches for "TWO"
SELECT * FROM "Three";       -- searches for "THREE"
SELECT * FROM three;         -- searches for "THREE"

-- This query does not work now - "One" is not retrievable
SELECT * FROM "One";         -- searches for "ONE"