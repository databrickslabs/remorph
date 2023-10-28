SELECT ... FROM my_table
  LEFT JOIN TABLE(my_js_udtf(a))
  ON ... ;