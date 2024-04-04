
-- snowflake sql:
select STRTOK('a_b_c'), STRTOK(tbl.col123, '.', 3) FROM table tbl;

-- databricks sql:
SELECT SPLIT_PART('a_b_c', ' ', 1), SPLIT_PART(tbl.col123, '.', 3) FROM table AS tbl;
