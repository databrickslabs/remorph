-- see https://docs.snowflake.com/en/sql-reference/functions/to_date

SELECT TO_DATE('2012.07.23', 'YYYY.MM.DD'), DATE('2012.07.23', 'YYYY.MM.DD');