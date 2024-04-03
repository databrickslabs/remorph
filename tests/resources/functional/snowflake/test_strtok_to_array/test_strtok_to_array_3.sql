
-- source:
select STRTOK_TO_ARRAY('a@b.c', ".@");

-- databricks_sql:
SELECT SPLIT('a@b.c','[.@]');
