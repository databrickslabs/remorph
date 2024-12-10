-- tsql sql:
SELECT r_regionkey, r_name INTO t_region FROM (VALUES (1, 'North'), (2, 'South')) AS temp (r_regionkey, r_name); SELECT * FROM t_region; -- REMORPH CLEANUP: DROP TABLE t_region;
