-- see https://docs.snowflake.com/en/sql-reference/constructs/where

SELECT * FROM invoices
    WHERE amount < (
                   SELECT AVG(amount)
                       FROM invoices
                   )
    ;