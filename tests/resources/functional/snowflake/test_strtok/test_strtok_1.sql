
-- source:
select STRTOK('my text is divided');

-- databricks_sql:
SELECT SPLIT_PART('my text is divided', ' ', 1);
