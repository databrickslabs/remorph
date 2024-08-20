
-- snowflake sql:
select STRTOK_TO_ARRAY('v_p_n', "_"), STRTOK_TO_ARRAY(col123, ".") FROM table tbl;

-- databricks sql:
SELECT SPLIT('v_p_n','[_]'), SPLIT(col123,'[.]') FROM table AS tbl;
