-- tsql sql:
SELECT n_name, r_name FROM (VALUES ('nation1', 'region1'), ('nation2', 'region2')) AS TempResult (n_name, r_name) GROUP BY n_name, r_name;
