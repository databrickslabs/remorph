
-- snowflake sql:
select STRTOK_TO_ARRAY('a@b.i', '.@');

-- databricks sql:
SELECT SPLIT('a@b.i','[.@]');
