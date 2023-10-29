-- see https://docs.snowflake.com/en/sql-reference/sql/update

UPDATE t1
  SET number_column = t1.number_column + t2.number_column, t1.text_column = 'ASDF'
  FROM t2
  WHERE t1.key_column = t2.t1_key and t1.number_column < 10;