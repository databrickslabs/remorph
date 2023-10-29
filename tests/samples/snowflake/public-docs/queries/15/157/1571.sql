-- see https://docs.snowflake.com/en/sql-reference/sql/create-external-table

SELECT col1, col2, col3 FROM et1 WHERE col1 = TO_DATE('2022-01-24') AND col2 = 'a' ORDER BY METADATA$FILE_ROW_NUMBER;