
-- snowflake sql:
select to_char(column1, '">"$99.0"<"') as D2_1,
                to_char(column1, '">"B9,999.0"<"') as D4_1 FROM table;

-- databricks sql:
SELECT TO_CHAR(column1, '">"$99.0"<"') AS D2_1, TO_CHAR(column1, '">"B9,999.0"<"') AS D4_1 FROM table;
