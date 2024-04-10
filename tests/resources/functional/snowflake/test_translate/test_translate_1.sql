
-- snowflake sql:
SELECT translate('AaBbCc', 'abc', '123') AS translate_col1 FROM tabl;

-- databricks sql:
SELECT TRANSLATE('AaBbCc', 'abc', '123') AS translate_col1 FROM tabl;
