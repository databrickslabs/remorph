-- see https://docs.snowflake.com/en/sql-reference/sql/create-view

CREATE VIEW employee_hierarchy (title, employee_ID, manager_ID, "MGR_EMP_ID (SHOULD BE SAME)", "MGR TITLE") AS (
   WITH RECURSIVE employee_hierarchy_cte (title, employee_ID, manager_ID, "MGR_EMP_ID (SHOULD BE SAME)", "MGR TITLE") AS (
      -- Start at the top of the hierarchy ...
      SELECT title, employee_ID, manager_ID, NULL AS "MGR_EMP_ID (SHOULD BE SAME)", 'President' AS "MGR TITLE"
        FROM employees
        WHERE title = 'President'
      UNION ALL
      -- ... and work our way down one level at a time.
      SELECT employees.title, 
             employees.employee_ID, 
             employees.manager_ID, 
             employee_hierarchy_cte.employee_id AS "MGR_EMP_ID (SHOULD BE SAME)", 
             employee_hierarchy_cte.title AS "MGR TITLE"
        FROM employees INNER JOIN employee_hierarchy_cte
       WHERE employee_hierarchy_cte.employee_ID = employees.manager_ID
   )
   SELECT * 
      FROM employee_hierarchy_cte
);