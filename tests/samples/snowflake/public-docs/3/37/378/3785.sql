SELECT ... FROM my_table
  FULL JOIN TABLE(FLATTEN(input=>[a]))
  ON ... ;