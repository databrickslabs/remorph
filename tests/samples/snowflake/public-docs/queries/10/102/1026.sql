-- see https://docs.snowflake.com/en/sql-reference/functions/as_decimal-number

SELECT AS_DECIMAL(decimal1, 6, 3) AS "Decimal" FROM multiple_types;