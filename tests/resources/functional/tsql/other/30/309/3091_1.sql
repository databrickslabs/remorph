-- tsql sql:
CREATE VIEW region_view AS SELECT r_regionkey, r_name, r_comment FROM (VALUES (1, 'North America', 'This is a region'), (2, 'South America', 'This is another region'), (3, 'Europe', 'This is a third region')) AS region (r_regionkey, r_name, r_comment);
