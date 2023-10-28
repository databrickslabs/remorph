SELECT ... FROM my_table
  LEFT JOIN TABLE(FLATTEN(input=>[a]))
  ON ... ;