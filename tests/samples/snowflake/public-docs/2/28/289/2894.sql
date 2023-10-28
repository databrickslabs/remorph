INSERT OVERWRITE INTO sf_employees
  SELECT * FROM employees
  WHERE city = 'San Francisco';