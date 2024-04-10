
-- snowflake sql:
select to_varchar(-12454.8, '99,999.9S'),
                '>' || to_char(col1, '00000.00') || '<' FROM dummy;

-- databricks sql:
SELECT TO_CHAR(-12454.8, '99,999.9S'), '>' || TO_CHAR(col1, '00000.00') || '<' FROM dummy;
