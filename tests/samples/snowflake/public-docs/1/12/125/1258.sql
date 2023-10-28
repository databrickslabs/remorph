SELECT * 
  FROM ilike_example 
  WHERE subject ILIKE ANY ('jane%', '%SMITH')
  ORDER BY subject;