SELECT * 
  FROM like_all_example 
  WHERE subject LIKE ALL ('%Jo%oe%','J%e')
  ORDER BY subject;