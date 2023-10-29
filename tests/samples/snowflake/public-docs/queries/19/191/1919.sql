-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

UPDATE varia SET v = TO_VARIANT(float1);  -- converts FROM a float TO a variant.
UPDATE varia SET float2 = v::FLOAT;       -- converts FROM a variant TO a float.