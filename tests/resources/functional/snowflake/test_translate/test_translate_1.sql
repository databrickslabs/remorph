
-- source:
SELECT translate('AaBbCc', 'abc', '123') AS translate_col1 FROM tabl;

-- databricks_sql:
SELECT TRANSLATE('AaBbCc', 'abc', '123') AS translate_col1 FROM tabl;
