-- ##COLLATIONPROPERTY
--
-- The COLLATIONPROPERTY function is unsupported in Databricks SQL as collation
-- tends to be a function of the underlying system.
--
-- tsql sql:
SELECT COLLATIONPROPERTY('somelocale', 'someproperty');

-- databricks sql:
SELECT COLLATIONPROPERTY('somelocale', 'someproperty');
