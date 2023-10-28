SELECT ... FROM my_table
  JOIN TABLE(my_js_udtf(col_a))
  ON ... ;