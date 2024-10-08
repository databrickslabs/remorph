
-- snowflake sql:
select STRTOK_TO_ARRAY('a@b.c', '.@');

-- databricks sql:
SELECT SPLIT('a@b.c','[.@]');
