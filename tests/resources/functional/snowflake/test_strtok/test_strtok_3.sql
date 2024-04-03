
-- source:
select STRTOK('user@example.com', '@.', 2),
                SPLIT_PART(col123, '.', 1) FROM table tbl;

-- databricks_sql:
SELECT SPLIT_PART('user@example.com', '@.', 2), SPLIT_PART(col123, '.', 1) FROM table AS tbl;
