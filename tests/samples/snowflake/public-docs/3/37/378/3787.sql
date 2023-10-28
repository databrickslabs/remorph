SELECT ... FROM my_table
  FULL JOIN TABLE(my_js_udtf(a))
  ON ... ;