SELECT 
employee_ID, manager_ID, title,
CONNECT_BY_ROOT title AS root_title
  FROM employees
    START WITH title = 'President'
    CONNECT BY
      manager_ID = PRIOR employee_id
  ORDER BY employee_ID;