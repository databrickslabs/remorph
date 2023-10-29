-- see https://docs.snowflake.com/en/sql-reference/sql/create-external-table

SELECT timestamp, col2 FROM et1 WHERE date_part = to_date('08/05/2018');