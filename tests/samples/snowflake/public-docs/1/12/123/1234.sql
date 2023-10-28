SELECT * 
  FROM like_example 
  WHERE subject LIKE ANY ('%Jo%oe%','T%e')
  ORDER BY subject;