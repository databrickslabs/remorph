-- snowflake sql:

    select *
       from (
             select *
                from t1 join t2
                   on t1.a = t2.i
            ) sample (1);
                ;

-- databricks sql:
SELECT * FROM (
  SELECT * FROM t1 JOIN t2 ON t1.a = t2.i
) TABLESAMPLE (1 PERCENT);
