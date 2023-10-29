-- see https://docs.snowflake.com/en/sql-reference/sql-format-models

-- All of the following convert the input to the number 12,345.67.
SELECT TO_NUMBER('012,345.67', '999,999.99', 8, 2);
SELECT TO_NUMBER('12,345.67', '999,999.99', 8, 2);
SELECT TO_NUMBER(' 12,345.67', '999,999.99', 8, 2);
-- The first of the following works, but the others will not convert.
-- (They are not supposed to convert, so "failure" is correct.)
SELECT TO_NUMBER('012,345.67', '000,000.00', 8, 2);
SELECT TO_NUMBER('12,345.67', '000,000.00', 8, 2);
SELECT TO_NUMBER(' 12,345.67', '000,000.00', 8, 2);