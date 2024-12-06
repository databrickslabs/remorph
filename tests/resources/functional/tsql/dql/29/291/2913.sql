-- tsql sql:
SELECT name, 'was created on ', create_date, CHAR(13), name, 'is currently ', state_desc FROM (VALUES ('Customer', '2022-01-01', 'Active'), ('Order', '2022-01-02', 'Inactive'), ('Lineitem', '2022-01-03', 'Active')) AS temp_result (name, create_date, state_desc);
