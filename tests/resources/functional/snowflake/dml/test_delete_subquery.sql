

-- snowflake sql:

DELETE FROM table1 AS t1 USING (SELECT c2 FROM table2 WHERE t2.c3 = 'foo') AS t2 WHERE t1.c1 = t2.c2;

-- databricks sql:

merge into  table1 as t1 using (select c2 from table2 where t2.c3 = 'foo') as t2 on t1.c1 = t2.c2 when matched then delete;
