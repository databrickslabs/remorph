SELECT ... FROM my_table,
  TABLE(FLATTEN(input=>[col_a]))
  ON ... ;