SELECT ... FROM my_table
  INNER JOIN TABLE(my_js_udtf(col_a))
  ON ... ;