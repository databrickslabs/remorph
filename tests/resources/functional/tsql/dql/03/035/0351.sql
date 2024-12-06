-- tsql sql:
SELECT c_customerkey, c_lastname FROM (VALUES (1, 'Smith'), (2, 'Godfrey'), (3, 'Johnson')) AS Customer (c_customerkey, c_lastname) WHERE c_lastname IN ('Smith', 'Godfrey', 'Johnson');
