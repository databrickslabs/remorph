SELECT * 
  FROM like_all_example 
  WHERE subject LIKE ALL ('%Jo%oe%','J%n')
  ORDER BY subject;