INSERT INTO emp (id,first_name,last_name,city,postal_code,ph)
  SELECT a.id,a.first_name,a.last_name,a.city,a.postal_code,b.ph
  FROM emp_addr a
  INNER JOIN emp_ph b ON a.id = b.id;