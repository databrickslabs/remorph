
-- source:
SELECT OBJECT_CONSTRUCT(*) FROM VALUES(1,'x'), (2,'y');

-- databricks_sql:
SELECT STRUCT(*) FROM VALUES (1, 'x'), (2, 'y');
