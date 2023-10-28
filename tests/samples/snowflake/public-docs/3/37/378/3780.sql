SELECT ... FROM my_table
  JOIN TABLE(FLATTEN(input=>[col_a]))
  ON ... ;