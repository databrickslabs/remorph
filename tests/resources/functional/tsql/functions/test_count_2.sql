## COUNT

The TSQl COUNT function and the DataBricks COUNT function are equivalent.

-- tsql sql:

SELECT COUNT(DISTINCT col1) FROM t1;

-- databricks sql:

SELECT COUNT(DISTINCT col1) FROM t1;
