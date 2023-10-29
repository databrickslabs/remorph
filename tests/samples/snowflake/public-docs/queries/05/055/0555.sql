-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

CREATE TABLE varia (float1 FLOAT, v VARIANT, float2 FLOAT);
INSERT INTO varia (float1, v, float2) VALUES (1.23, NULL, NULL);