-- tsql sql:
SELECT c_customerkey, c_lastname FROM (VALUES ('1', 'Smith'), ('2', 'Johnson')) AS CustomerCTE (c_customerkey, c_lastname) WHERE c_lastname = 'Smith';
