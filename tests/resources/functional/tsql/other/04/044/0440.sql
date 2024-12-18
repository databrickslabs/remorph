-- tsql sql:
CREATE VIEW Regions AS SELECT * FROM (VALUES ('North', 10), ('South', 20)) AS Region_1 (Region, Sales) UNION ALL SELECT * FROM (VALUES ('East', 30), ('West', 40)) AS Region_2 (Region, Sales) UNION ALL SELECT * FROM (VALUES ('Central', 50), ('NorthEast', 60)) AS Region_3 (Region, Sales);
