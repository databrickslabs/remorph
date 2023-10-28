SELECT ... FROM my_table
  INNER JOIN TABLE(FLATTEN(input=>[col_a]))
  ON ... ;