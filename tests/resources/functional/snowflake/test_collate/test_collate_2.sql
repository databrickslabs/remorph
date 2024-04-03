
-- source:
SELECT v, COLLATION(v), COLLATE(v, 'sp-upper'), COLLATION(COLLATE(v, 'sp-upper')) FROM collation1;

-- databricks_sql:
SELECT v, COLLATION(v), COLLATE(v, 'sp-upper'), COLLATION(COLLATE(v, 'sp-upper')) FROM collation1;
