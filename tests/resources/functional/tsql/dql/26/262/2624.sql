-- tsql sql:
SELECT GREATEST('Customer', 'Supplier', 'Part') AS GreatestString FROM (VALUES ('Customer'), ('Supplier'), ('Part')) AS T(StringValue);