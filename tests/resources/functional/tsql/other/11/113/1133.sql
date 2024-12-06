-- tsql sql:
SELECT * FROM (VALUES (1, 'Gear1', 10.99), (2, 'Gear2', 9.99)) AS GearsCTE (p_partkey, p_name, p_retailprice);
